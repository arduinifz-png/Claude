# Claude Lead Qualification & Website Generation Agent

An AI-powered agent that processes CSV files of leads, identifies those without websites, and generates SEO-optimized website specifications using Claude AI.

## Features

- **CSV Lead Processing**: Upload and parse lead data files
- **Lead Qualification**: Automatically identify leads without existing websites
- **AI-Powered Specifications**: Claude generates detailed, SEO-optimized website specifications
- **Smart Content**: Includes target keywords, content architecture, design recommendations, and CTA strategies

## Setup

### Prerequisites
- Python 3.8+
- Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

### Quick Start

```bash
# Run automated setup
bash setup.sh
```

Then edit `.env` and add your `ANTHROPIC_API_KEY`.

### Manual Installation

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
```

2. Prepare your CSV file with lead data. Required columns:
   - `name`: Lead/business name
   - `email`: Contact email
   - `website`: Existing website URL (leave blank for unqualified leads)
   - Additional columns: `phone`, `industry`, etc.

## Usage

### Step 1: Qualify Leads & Generate Specifications

```bash
python lead_agent.py <csv_file> [output_file.json]
```

**Example:**
```bash
python lead_agent.py example_leads.csv results.json
```

This will:
1. Load all leads from your CSV
2. Identify leads without websites
3. Use Claude to generate detailed website specifications
4. Save results to `results.json`

### Step 2: Generate HTML Websites (Optional)

```bash
python website_generator.py <results_json_file> [output_directory]
```

**Example:**
```bash
python website_generator.py results.json generated_websites/
```

This will:
1. Read the specifications from Step 1
2. Generate professional HTML websites
3. Apply design recommendations
4. Save individual HTML files for each lead

## Output

The agent generates a JSON file with:
- Total and unqualified lead counts
- Detailed website specifications for each lead including:
  - Website purpose and value proposition
  - SEO strategy with target keywords
  - Content architecture
  - Visual design recommendations
  - Core features needed
  - Call-to-action strategy
  - Technical SEO requirements

## Example CSV Format

```csv
name,email,phone,industry,website
John's Plumbing,john@plumbing.local,555-0101,Plumbing,
Sarah's Cleaning Service,sarah@cleaning.local,555-0102,Cleaning,
Mike's Auto Repair,mike@autorepair.local,555-0103,Auto Repair,https://mikesautorepair.com
```

## How It Works

1. **CSV Reading**: Parses the CSV file into lead records
2. **Lead Filtering**: Identifies leads with missing or empty website fields
3. **Claude Processing**: For each unqualified lead, sends detailed context to Claude to generate:
   - Industry-specific SEO strategy
   - Professional design recommendations
   - Content structure optimized for conversions
   - Technical implementation guidance
4. **Result Aggregation**: Combines all specifications into a comprehensive JSON report

## Model

Uses Claude Opus 4.7 (latest) for superior reasoning and comprehensive website specification generation.

## Complete Workflow Example

```bash
# 1. Setup
bash setup.sh

# 2. Edit .env with your API key

# 3. Run the lead qualification agent
python lead_agent.py your_leads.csv results.json

# 4. (Optional) Generate HTML websites
python website_generator.py results.json generated_websites/

# 5. Review generated specifications and HTML files
# - results.json contains the detailed specifications
# - generated_websites/ contains ready-to-use HTML files
```

## Outputs

### results.json
Comprehensive JSON file containing:
```json
{
  "total_leads": 10,
  "unqualified_leads": 6,
  "website_specs": [
    {
      "lead": { /* original lead data */ },
      "website_spec": {
        "purpose": "...",
        "seo_strategy": { /* keywords, meta descriptions */ },
        "content_architecture": { /* pages and sections */ },
        "visual_design": { /* colors, fonts */ },
        "core_features": [ /* required functionality */ ],
        "cta_strategy": { /* conversion optimization */ },
        "technical_seo": { /* performance, structure */ }
      }
    }
  ]
}
```

### generated_websites/
HTML files ready for:
- Publishing directly
- Integrating with static site builders
- Hosting on any web server
- Further customization

## Tips for Best Results

1. **CSV Data Quality**: Include relevant fields like industry, company type, location
2. **Website Column**: Leave blank or use "none"/"N/A" for leads without websites
3. **Email Contact**: Ensure valid email addresses for lead contact
4. **Industry Specificity**: The agent tailors suggestions based on industry

## Troubleshooting

**API Key Error?**
```bash
# Verify .env has your API key
cat .env | grep ANTHROPIC_API_KEY

# Or set as environment variable
export ANTHROPIC_API_KEY="sk-ant-..."
python lead_agent.py leads.csv
```

**CSV Format Error?**
- Ensure first row is header with column names
- Use "name", "email", "website" as column names
- Check for encoding issues (should be UTF-8)
