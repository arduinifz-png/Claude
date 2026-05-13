#!/usr/bin/env python3
"""
Website HTML generator using Claude specifications.

Converts website specifications from the lead agent into
SEO-optimized HTML templates.
"""

import json
from typing import Optional


def generate_html_from_spec(lead: dict, spec: dict) -> str:
    """Generate HTML website from Claude specification."""

    company_name = lead.get('name', 'Business')
    industry = lead.get('industry', 'Services')

    seo = spec.get('seo_strategy', {})
    if isinstance(seo, str):
        meta_desc = seo[:160]
        keywords = "business, services"
    else:
        meta_desc = seo.get('meta_description', f'{company_name} - {industry} Services')[:160]
        keywords = seo.get('keywords', f'{company_name}, {industry}')

    content_arch = spec.get('content_architecture', {})
    if isinstance(content_arch, str):
        sections = []
    else:
        sections = content_arch.get('pages', []) if isinstance(content_arch.get('pages'), list) else []

    visual = spec.get('visual_design', {})
    if isinstance(visual, dict):
        primary_color = visual.get('primary_color', '#0066cc')
        secondary_color = visual.get('secondary_color', '#f0f0f0')
    else:
        primary_color = '#0066cc'
        secondary_color = '#f0f0f0'

    cta = spec.get('cta_strategy', '')
    if isinstance(cta, dict):
        cta_text = cta.get('primary_cta', 'Contact Us Today')
    else:
        cta_text = 'Contact Us Today'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="{keywords}">
    <title>{company_name} - {industry} Services</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }}

        header {{
            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
            color: white;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        nav {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
        }}

        nav ul {{
            display: flex;
            list-style: none;
            gap: 2rem;
        }}

        nav a {{
            color: white;
            text-decoration: none;
            transition: opacity 0.3s;
        }}

        nav a:hover {{
            opacity: 0.8;
        }}

        .hero {{
            background: linear-gradient(135deg, {primary_color} 0%, #0052a3 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
        }}

        .hero-content {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .hero h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}

        .hero p {{
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.95;
        }}

        .cta-button {{
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 1rem 2rem;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.3s;
            cursor: pointer;
        }}

        .cta-button:hover {{
            background: #ff5252;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }}

        .feature {{
            padding: 2rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            text-align: center;
            transition: box-shadow 0.3s;
        }}

        .feature:hover {{
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .feature h3 {{
            color: {primary_color};
            margin: 1rem 0;
        }}

        footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
        }}

        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2rem;
            }}

            nav ul {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">{company_name}</div>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <section class="hero">
        <div class="hero-content">
            <h1>{company_name}</h1>
            <p>{spec.get('purpose', 'Professional ' + industry + ' Services')}</p>
            <a href="#contact" class="cta-button">{cta_text}</a>
        </div>
    </section>

    <main class="container">
        <section id="services">
            <h2>Our Services</h2>
            <div class="features">
                <div class="feature">
                    <h3>Professional Service</h3>
                    <p>High-quality {industry.lower()} services tailored to your needs.</p>
                </div>
                <div class="feature">
                    <h3>Expert Team</h3>
                    <p>Experienced professionals dedicated to your success.</p>
                </div>
                <div class="feature">
                    <h3>24/7 Support</h3>
                    <p>Always here when you need us. Quick response times guaranteed.</p>
                </div>
            </div>
        </section>

        <section id="about">
            <h2>Why Choose {company_name}?</h2>
            <p>We are committed to providing the best {industry.lower()} services in the area.
            With years of experience and a dedicated team, we ensure every project exceeds expectations.</p>
        </section>

        <section id="contact">
            <h2>Get In Touch</h2>
            <p>Ready to work with us? Contact {company_name} today!</p>
            <a href="mailto:{lead.get('email', 'contact@example.com')}" class="cta-button">Send Us an Email</a>
        </section>
    </main>

    <footer>
        <p>&copy; 2024 {company_name}. All rights reserved. | {industry} Services</p>
    </footer>
</body>
</html>"""

    return html


def save_websites_to_html(results: dict, output_dir: str = "generated_websites"):
    """Save HTML files for each lead's website."""
    import os

    os.makedirs(output_dir, exist_ok=True)

    for item in results.get('website_specs', []):
        lead = item['lead']
        spec = item['website_spec']

        filename = lead.get('name', 'website').replace(' ', '_').lower()
        filepath = os.path.join(output_dir, f"{filename}.html")

        html = generate_html_from_spec(lead, spec)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"💾 Generated HTML for {lead.get('name', 'Unknown')}: {filepath}")


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python website_generator.py <results_json_file> [output_directory]")
        sys.exit(1)

    results_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "generated_websites"

    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    print(f"📄 Loading results from {results_file}")
    save_websites_to_html(results, output_dir)
    print(f"✅ Generated {len(results.get('website_specs', []))} HTML files in {output_dir}/")
