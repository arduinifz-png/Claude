# Lead Qualification & Website Generation Dashboard

A complete web application for processing CSV lead files and generating professional, SEO-optimized websites with shareable links.

## Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- Node.js 16+ (for Cloudflare Workers)
- Anthropic API key

### 1. Install Dependencies

```bash
# Install Flask API dependencies
cd api
pip install -r requirements.txt
cd ..

# Install Cloudflare Workers dependencies (optional)
cd cloudflare-worker
npm install
cd ..
```

### 2. Configure Environment

```bash
# Copy and edit .env
cp api/.env.example api/.env

# Add your ANTHROPIC_API_KEY and UPSTASH_REDIS_URL
# (for local testing, Redis is optional)
```

### 3. Run Locally

```bash
# Terminal 1: Start Flask API
cd api
python app.py

# Terminal 2: Serve dashboard
# Option 1: Use Python HTTP server
cd public
python -m http.server 8080

# Option 2: Use a simple HTTP server like http-server
npx http-server public -p 8080
```

### 4. Access Dashboard

Open browser to:
```
http://localhost:8080
```

For local testing without Redis:
- The API will process CSVs but won't store websites
- You can still see the generated specifications

## Project Structure

```
web-dashboard/
├── api/                          # Flask API backend (deploys to Railway)
│   ├── app.py                   # Main Flask application
│   ├── requirements.txt          # Python dependencies
│   └── .env.example             # Environment template
├── cloudflare-worker/            # Edge computing (Cloudflare Workers)
│   ├── src/index.js             # Worker logic for serving websites
│   ├── wrangler.toml            # Cloudflare configuration
│   └── package.json             # Node dependencies
├── public/                       # Dashboard frontend (Cloudflare Pages)
│   └── index.html               # Single-page application
├── DEPLOYMENT.md                # Complete deployment guide
└── README.md                     # This file
```

## Features

### 🚀 CSV Upload
- Drag-and-drop CSV upload
- Support for: name, email, phone, industry, website columns
- Real-time validation

### 🤖 AI Processing
- Uses Claude Opus 4.7 for specifications
- Generates SEO strategies, content architecture, design recommendations
- Industry-specific customization

### 🎨 Website Generation
- Automatic HTML generation from specifications
- Matches professional template design
- Mobile-responsive layouts

### 🔗 Shareable Links
- Unique URL for each generated website
- No file downloads needed
- Works globally with Cloudflare CDN

### 📊 Results Dashboard
- View all generated websites
- Copy shareable links
- Live preview in modal
- Download HTML if needed

## Tech Stack

### Backend
- **Flask** - Python web framework
- **Anthropic SDK** - Claude API integration
- **Redis** - Upstash for data storage

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Flexbox/Grid
- **Vanilla JS** - No dependencies for dashboard

### Deployment
- **Railway** - API hosting
- **Cloudflare Pages** - Static site hosting
- **Cloudflare Workers** - Edge computing
- **Upstash** - Serverless Redis
- **GitHub** - Version control and deployments

## Environment Variables

### Flask API

```env
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx
UPSTASH_REDIS_URL=redis://:password@host:port

# Optional
FLASK_ENV=production
PORT=8000
CORS_ORIGINS=*
```

### Cloudflare Workers

```env
UPSTASH_REDIS_URL=redis://:password@host:port
```

## API Endpoints

### `POST /api/process-csv`
Process a CSV file and generate website specifications.

**Request:**
```json
{
  "csv_content": "name,email,phone,industry,website\n..."
}
```

**Response:**
```json
{
  "project_id": "uuid",
  "total_leads": 10,
  "unqualified_leads": 6,
  "website_count": 6,
  "shareable_links": [
    {
      "lead_name": "Company Name",
      "website_id": "abc123",
      "url": "https://yourapp.com/website/abc123"
    }
  ]
}
```

### `GET /api/project/{project_id}`
Retrieve project results by ID.

### `GET /api/website/{website_id}`
Get website HTML content (called by frontend preview).

### `GET /api/health`
Health check endpoint.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide including:
- Upstash Redis setup
- Railway deployment
- Cloudflare Pages setup
- Cloudflare Workers deployment
- Custom domain configuration

## CSV Format

Your CSV should include these columns:

```csv
name,email,phone,industry,website
John's Plumbing,john@plumbing.local,555-0101,Plumbing,
Swift Electrical,swift@electrical.local,555-0102,Electrical,
Elite HVAC,elite@hvac.local,555-0103,HVAC,https://elite-hvac.com
```

**Column Definitions:**
- **name**: Business/company name
- **email**: Contact email address
- **phone**: Contact phone number
- **industry**: Business industry/type
- **website**: Existing website URL (leave blank for leads to generate)

## Features

### Lead Qualification
- Automatically identifies leads without websites
- Filters out unqualified leads
- Shows statistics on dashboard

### Website Specifications
- AI-generated based on industry and business type
- Includes SEO strategy with keywords
- Content architecture recommendations
- Visual design guidelines
- Technical SEO requirements

### Professional Websites
- Responsive mobile design
- Modern glassmorphism effects
- Trust badges and reviews carousel
- Call-to-action buttons
- Service cards grid
- Contact forms
- Footer with schema markup

### Global Availability
- Cloudflare CDN for fast delivery
- Edge caching for instant loads
- Custom domain support
- SSL/TLS encryption

## Monitoring

### Logs
- **Railway**: `railway logs` command
- **Cloudflare**: Dashboard analytics
- **Upstash**: Redis console monitoring

### Metrics to Track
- API response times
- Website generation success rate
- Redis storage usage
- Cloudflare request counts

## Troubleshooting

### LocalDevelopment Issues

**"Module not found: website_generator"**
- Ensure you're in the correct directory
- Check sys.path in app.py points to parent directory

**"Redis connection refused"**
- Set UPSTASH_REDIS_URL in .env
- Or comment out Redis for local testing

**CORS errors in browser**
- Flask CORS is configured for *
- Check API URL in index.html matches backend URL

### Deployment Issues

See [DEPLOYMENT.md - Troubleshooting](DEPLOYMENT.md#troubleshooting) section.

## Security

- API keys stored in environment variables only
- HTTPS/SSL enforced on all connections
- CORS configured for your domain
- Redis passwords included in URL (keep private)
- No sensitive data in client-side code

## Performance

- API response: ~30-60 seconds per lead (Claude processing time)
- Website serving: <100ms (Cloudflare edge cache)
- Dashboard load: Instant (static Pages)
- Upstash queries: <10ms (Redis at edge)

## Roadmap

- [ ] Batch CSV processing with progress updates
- [ ] Website preview with live editing
- [ ] Download generated HTML as ZIP
- [ ] Custom domain support for generated websites
- [ ] Analytics on website views
- [ ] Email notifications when processing complete
- [ ] Team/org support with API keys
- [ ] Custom branding for generated websites

## Support

For issues or questions:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting)
2. Review API logs: `railway logs`
3. Check Cloudflare dashboard for errors
4. Monitor Upstash console for Redis issues

## License

MIT License - see LICENSE file for details
