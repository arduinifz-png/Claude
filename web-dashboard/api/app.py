#!/usr/bin/env python3
"""
Flask API backend for CSV lead processing and website generation.
Integrates with Upstash Redis for storing generated websites.
Designed for Railway deployment.
"""

import os
import json
import csv
import uuid
from io import StringIO
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import redis

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize clients
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")

client = anthropic.Anthropic(api_key=api_key)

# Redis/Upstash connection
redis_url = os.environ.get("UPSTASH_REDIS_URL")
redis_client = None
if redis_url and redis_url != "redis://localhost:6379":
    try:
        redis_client = redis.from_url(redis_url, decode_responses=True, socket_timeout=5)
        redis_client.ping()
    except Exception as e:
        print(f"Warning: Could not connect to Redis at {redis_url}: {e}")
        redis_client = None

# Import website generator
import sys
sys.path.insert(0, '/home/user/Claude')
from website_generator import generate_full_html


def read_csv_content(csv_text: str) -> list[dict]:
    """Parse CSV content from text."""
    reader = csv.DictReader(StringIO(csv_text))
    return list(reader)


def qualify_leads(leads: list[dict]) -> list[dict]:
    """Filter leads without websites."""
    unqualified = []
    for lead in leads:
        website = lead.get('website', '').strip()
        if not website or website.lower() in ['none', 'n/a', '', 'unknown']:
            unqualified.append(lead)
    return unqualified


def generate_website_spec(lead: dict) -> dict:
    """Use Claude to generate website specification."""
    lead_info = json.dumps(lead, indent=2)

    prompt = f"""You are a expert web designer and SEO strategist. Based on this lead information, generate a comprehensive website specification with great SEO.

Lead Information:
{lead_info}

Generate a detailed website specification that includes:
1. **Website Purpose & Key Message**: Clear value proposition
2. **SEO Strategy**: Target keywords, meta descriptions, heading structure
3. **Content Architecture**: Homepage sections, key pages needed
4. **Visual Design**: Color scheme, typography, layout style
5. **Core Features**: Essential functionality and tools
6. **Call-to-Action Strategy**: How to convert visitors
7. **Technical SEO**: Mobile responsiveness, load speed optimization, structured data

Respond in JSON format with these exact keys: purpose, seo_strategy, content_architecture, visual_design, core_features, cta_strategy, technical_seo"""

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        response_text = message.content[0].text
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        spec = json.loads(response_text)
    except (json.JSONDecodeError, IndexError):
        spec = {"purpose": "Website specification generation", "raw_response": message.content[0].text}

    return {"lead": lead, "website_spec": spec}


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "lead-qualification-api"})


@app.route('/api/process-csv', methods=['POST'])
def process_csv():
    """
    Process CSV file and generate website specifications.

    Expected request:
    - csv_content: CSV file content as text

    Returns:
    - project_id: Unique ID for this batch
    - total_leads: Total leads in CSV
    - unqualified_leads: Leads without websites
    - website_specs: Array of generated specifications
    - shareable_links: URLs for each generated website
    """
    try:
        data = request.get_json()
        csv_content = data.get('csv_content', '')

        if not csv_content:
            return jsonify({"error": "No CSV content provided"}), 400

        # Parse CSV
        leads = read_csv_content(csv_content)
        unqualified = qualify_leads(leads)

        if not unqualified:
            return jsonify({
                "total_leads": len(leads),
                "unqualified_leads": 0,
                "message": "All leads have websites"
            }), 200

        # Process leads and generate specifications
        results = {
            "total_leads": len(leads),
            "unqualified_leads": len(unqualified),
            "website_specs": []
        }

        shareable_links = []
        project_id = str(uuid.uuid4())

        for i, lead in enumerate(unqualified, 1):
            print(f"Processing lead {i}/{len(unqualified)}: {lead.get('name')}")
            spec = generate_website_spec(lead)
            results["website_specs"].append(spec)

            # Generate HTML website
            try:
                html_content = generate_full_html(lead, spec.get('website_spec', {}))

                # Store in Redis
                website_id = str(uuid.uuid4())[:8]
                if redis_client:
                    redis_client.setex(
                        f"website:{website_id}",
                        86400 * 30,  # 30 days expiry
                        html_content
                    )

                shareable_links.append({
                    "lead_name": lead.get('name'),
                    "website_id": website_id,
                    "url": f"https://yourapp.com/website/{website_id}"  # Will be replaced with actual domain
                })
            except Exception as e:
                print(f"Error generating HTML for {lead.get('name')}: {e}")
                shareable_links.append({
                    "lead_name": lead.get('name'),
                    "error": str(e)
                })

        # Store project results
        if redis_client:
            redis_client.setex(
                f"project:{project_id}",
                86400 * 30,
                json.dumps(results)
            )

        return jsonify({
            "project_id": project_id,
            "total_leads": results["total_leads"],
            "unqualified_leads": results["unqualified_leads"],
            "website_count": len(shareable_links),
            "shareable_links": shareable_links,
            "message": f"Successfully processed {len(unqualified)} leads"
        }), 200

    except Exception as e:
        print(f"Error processing CSV: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/project/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get project results by ID."""
    if not redis_client:
        return jsonify({"error": "Redis not available"}), 503

    try:
        project_data = redis_client.get(f"project:{project_id}")
        if not project_data:
            return jsonify({"error": "Project not found"}), 404

        return jsonify(json.loads(project_data)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/website/<website_id>', methods=['GET'])
def get_website(website_id):
    """Get website HTML by ID."""
    if not redis_client:
        return jsonify({"error": "Redis not available"}), 503

    try:
        html_content = redis_client.get(f"website:{website_id}")
        if not html_content:
            return jsonify({"error": "Website not found"}), 404

        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
