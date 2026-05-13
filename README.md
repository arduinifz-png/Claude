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
- Anthropic API key

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file with your API key:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

2. Prepare your CSV file with lead data. Required columns:
   - `name`: Lead/business name
   - `email`: Contact email
   - `website`: Existing website URL (leave blank for unqualified leads)
   - Additional columns: `phone`, `industry`, etc.

## Usage

```bash
python lead_agent.py <csv_file> [output_file.json]
```

### Example

```bash
python lead_agent.py example_leads.csv results.json
```

This will:
1. Load all leads from the CSV
2. Identify leads without websites
3. Generate detailed website specifications for each unqualified lead
4. Save results to `results.json`

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
