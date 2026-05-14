#!/usr/bin/env python3
"""
Claude Lead Qualification and Website Generation Agent

This agent:
1. Processes CSV files with lead data
2. Identifies leads without websites
3. Qualifies leads using Claude
4. Generates SEO-optimized website specifications
"""

import os
import json
import csv
from pathlib import Path
from typing import Optional
from io import StringIO
from dotenv import load_dotenv
import anthropic

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError(
        "❌ ANTHROPIC_API_KEY not found. Please set it in .env file or as environment variable"
    )

client = anthropic.Anthropic(api_key=api_key)


def read_csv_file(file_path: str) -> list[dict]:
    """Read CSV file and return list of lead dictionaries."""
    leads = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads


def qualify_leads(leads: list[dict]) -> list[dict]:
    """Filter leads that don't have a website."""
    unqualified = []
    for lead in leads:
        website = lead.get('website', '').strip()
        if not website or website.lower() in ['none', 'n/a', '', 'unknown']:
            unqualified.append(lead)
    return unqualified


def generate_website_spec(lead: dict) -> dict:
    """Use Claude to generate SEO-optimized website specification for a lead."""

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
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    try:
        response_text = message.content[0].text
        # Extract JSON if wrapped in markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        spec = json.loads(response_text)
    except (json.JSONDecodeError, IndexError):
        spec = {
            "purpose": "Website specification generation",
            "raw_response": message.content[0].text
        }

    return {
        "lead": lead,
        "website_spec": spec
    }


def process_csv_and_generate_websites(csv_file_path: str) -> dict:
    """Main agent function: process CSV and generate website specs for unqualified leads."""

    print(f"📋 Reading CSV file: {csv_file_path}")
    leads = read_csv_file(csv_file_path)
    print(f"✅ Loaded {len(leads)} leads")

    print("\n🔍 Identifying leads without websites...")
    unqualified_leads = qualify_leads(leads)
    print(f"✅ Found {len(unqualified_leads)} leads without websites")

    results = {
        "total_leads": len(leads),
        "unqualified_leads": len(unqualified_leads),
        "website_specs": []
    }

    for i, lead in enumerate(unqualified_leads, 1):
        print(f"\n🎯 Processing lead {i}/{len(unqualified_leads)}: {lead.get('name', 'Unknown')}")
        spec = generate_website_spec(lead)
        results["website_specs"].append(spec)
        print(f"✨ Website specification generated")

    return results


def save_results(results: dict, output_file: str = "website_specs.json"):
    """Save results to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Results saved to {output_file}")


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python lead_agent.py <csv_file_path> [output_file.json]")
        print("\nExample: python lead_agent.py leads.csv results.json")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "website_specs.json"

    if not Path(csv_file).exists():
        print(f"❌ Error: CSV file '{csv_file}' not found")
        sys.exit(1)

    print("🚀 Claude Lead Qualification & Website Generation Agent")
    print("=" * 50)

    results = process_csv_and_generate_websites(csv_file)
    save_results(results, output_file)

    print("\n" + "=" * 50)
    print(f"✅ Processing complete!")
    print(f"   - Total leads: {results['total_leads']}")
    print(f"   - Unqualified leads: {results['unqualified_leads']}")
    print(f"   - Website specs generated: {len(results['website_specs'])}")


if __name__ == "__main__":
    main()
