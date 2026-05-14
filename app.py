#!/usr/bin/env python3
"""
Flask API server for Lead Qualification & Website Generation
Handles CSV uploads and coordinates with lead_agent and website_generator
"""

import os
import json
from io import StringIO
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import anthropic
from lead_agent import qualify_leads, generate_website_spec
from website_generator import generate_full_html
import redis

load_dotenv()

DASHBOARD_DIR = os.path.join(os.path.dirname(__file__), 'web-dashboard', 'public')

app = Flask(__name__, static_folder=DASHBOARD_DIR, static_url_path='')

# Initialize Redis client for storing generated websites
try:
    redis_url = os.environ.get("UPSTASH_REDIS_URL")
    if redis_url:
        redis_client = redis.from_url(redis_url)
    else:
        redis_client = None
except:
    redis_client = None

@app.route('/')
def index():
    return send_from_directory(DASHBOARD_DIR, 'index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/api/process-csv', methods=['POST'])
def process_csv():
    """
    Process CSV file and generate websites for leads without websites
    Expected JSON: {"csv_content": "name,email,phone,industry,website\\n..."}
    """
    try:
        data = request.get_json()
        if not data or 'csv_content' not in data:
            return jsonify({"error": "Missing csv_content"}), 400

        csv_content = data['csv_content']

        # Parse CSV
        lines = csv_content.strip().split('\n')
        if len(lines) < 2:
            return jsonify({"error": "CSV must have headers and at least one row"}), 400

        # Parse headers and rows
        headers = [h.strip() for h in lines[0].split(',')]
        leads = []
        for line in lines[1:]:
            if not line.strip():
                continue
            values = [v.strip() for v in line.split(',')]
            lead = dict(zip(headers, values))
            leads.append(lead)

        total_leads = len(leads)

        # Qualify leads (find those without websites)
        unqualified_leads = qualify_leads(leads)

        # Generate websites for unqualified leads
        shareable_links = []
        generated_count = 0

        for lead in unqualified_leads:
            try:
                # Generate website spec using Claude (with extended timeout)
                spec_data = generate_website_spec(lead)
                website_spec = spec_data['website_spec']

                # Generate HTML
                website_html = generate_full_html(lead, website_spec)

                # Store in Redis if available, otherwise use placeholder ID
                if redis_client:
                    website_id = f"website_{hash(lead.get('email', '')) % 1000000}"
                    redis_client.set(f"website:{website_id}", website_html)
                else:
                    # For local testing without Redis, use a simple ID
                    website_id = f"website_{len(shareable_links) + 1}"

                shareable_links.append({
                    "lead_name": lead.get('name', 'Unknown'),
                    "website_id": website_id,
                    "email": lead.get('email', '')
                })
                generated_count += 1

            except Exception as e:
                # If generation fails for one lead, add error entry
                shareable_links.append({
                    "lead_name": lead.get('name', 'Unknown'),
                    "error": str(e)
                })

        return jsonify({
            "message": f"Processed {total_leads} leads, generated {generated_count} websites",
            "total_leads": total_leads,
            "unqualified_leads": len(unqualified_leads),
            "website_count": generated_count,
            "shareable_links": shareable_links
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/website/<website_id>', methods=['GET'])
def get_website(website_id):
    """Retrieve generated website HTML"""
    try:
        if redis_client:
            html_content = redis_client.get(f"website:{website_id}")
            if html_content:
                return html_content.decode() if isinstance(html_content, bytes) else html_content

        # For demo/testing without Redis
        return f"""
        <html>
        <head>
            <title>Generated Website</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 2rem; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Website Preview</h1>
                <p>Website ID: {website_id}</p>
                <p>This is a placeholder. The generated website HTML will be displayed here.</p>
            </div>
        </body>
        </html>
        """, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
