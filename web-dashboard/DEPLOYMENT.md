# Deployment Guide: Cloudflare + Upstash + Railway

This guide walks you through deploying the complete system with Cloudflare, Upstash, and Railway.

## Architecture

```
GitHub (Code) → Railway (Python API) + Upstash (Redis DB) + Cloudflare (CDN + Edge)
```

## Prerequisites

1. **Upstash Account** - https://upstash.com (free tier available)
2. **Railway Account** - https://railway.app (free tier available)
3. **Cloudflare Account** - https://cloudflare.com (free tier available)
4. **GitHub Account** - For version control
5. **Anthropic API Key** - From console.anthropic.com

## Step 1: Set up Upstash Redis

1. Go to https://console.upstash.com
2. Create a new Redis database:
   - Name: `lead-websites`
   - Region: Choose closest to your users
3. Copy the **UPSTASH_REDIS_URL** (looks like `redis://:password@host:port`)
4. Keep this safe - you'll need it for Railway and Cloudflare

## Step 2: Deploy to Railway

### 2.1 Create Railway Project

1. Go to https://railway.app
2. Click "Create Project"
3. Select "Deploy from GitHub"
4. Connect your GitHub account
5. Select the `Claude` repository
6. Select the `claude/build-claude-agents-X3gVy` branch
7. Configure the service:
   - **Name**: `lead-qualification-api`
   - **Root Directory**: `web-dashboard`

### 2.2 Set Environment Variables

In Railway project settings, add:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx (your API key)
UPSTASH_REDIS_URL=redis://:password@host:port
FLASK_ENV=production
PORT=8000
```

### 2.3 Deploy

Railway automatically deploys on GitHub push. Once deployed, you'll get a URL like:
```
https://lead-api-production.railway.app
```

Note this URL - you'll need it for the next step.

## Step 3: Deploy Cloudflare Pages

### 3.1 Static Dashboard on Pages

1. Go to https://dash.cloudflare.com
2. Create a new Pages project
3. Select "Upload assets" (for static hosting)
4. Upload files from `web-dashboard/public/`
5. Set environment variables in Pages settings:
   - `RAILWAY_API_URL=https://your-railway-app.railway.app`

### 3.2 Update Dashboard API URL

Edit `public/index.html` and update the API_URL:

```javascript
const API_URL = 'https://your-railway-app.railway.app';
```

Push this change and redeploy Pages.

## Step 4: Deploy Cloudflare Workers

### 4.1 Install Wrangler

```bash
npm install -g wrangler
```

### 4.2 Configure Worker

Edit `cloudflare-worker/wrangler.toml`:

```toml
[env.production]
routes = [
  { pattern = "yourapp.com/website/*", zone_name = "yourapp.com" }
]

[[env.production.env]]
UPSTASH_REDIS_URL = "your-upstash-redis-url"
```

Replace:
- `yourapp.com` with your actual domain
- `your-upstash-redis-url` with your Redis URL from Step 1

### 4.3 Deploy Worker

```bash
cd cloudflare-worker
wrangler deploy --env production
```

### 4.4 Set Up Custom Domain

1. Go to Cloudflare Dashboard
2. Add your domain (if not already there)
3. In Workers section, add route: `yourapp.com/website/*` → Worker
4. Verify DNS is pointing to Cloudflare nameservers

## Step 5: Connect Everything

### 5.1 Update API Endpoints

In `web-dashboard/api/app.py`, update the shareable link format:

```python
"url": f"https://yourapp.com/website/{website_id}"
```

### 5.2 Update Dashboard

In `web-dashboard/public/index.html`:

```javascript
const API_URL = 'https://your-railway-app.railway.app';
// or if using custom domain:
const API_URL = 'https://yourapp.com/api';
```

### 5.3 Test Full Flow

1. Go to `https://pages-project.pages.dev` (or your domain if using Cloudflare Pages with domain)
2. Upload a test CSV
3. Wait for processing
4. Get shareable links
5. Click preview to test website hosting

## Step 6: Custom Domain Setup

### 6.1 Register Domain

1. Register domain at Cloudflare or transfer existing domain
2. Update nameservers to Cloudflare nameservers

### 6.2 Configure DNS

In Cloudflare DNS settings:

```
api.yourapp.com → CNAME → your-railway-app.railway.app
www.yourapp.com → CNAME → pages-project.pages.dev
yourapp.com → CNAME → pages-project.pages.dev
```

### 6.3 Update Routing

Update Railway environment variable:
```
RAILWAY_DOMAIN=api.yourapp.com
```

## Monitoring & Logs

### Railway Logs
```bash
railway logs
```

### Cloudflare Analytics
- Pages: Cloudflare Dashboard → Pages → Analytics
- Workers: Cloudflare Dashboard → Workers → Analytics
- CDN Cache: Real-time cache analytics

### Upstash Metrics
- Dashboard: https://console.upstash.com
- Monitor command count, storage, connections

## Troubleshooting

### "Redis connection failed"
- Verify UPSTASH_REDIS_URL is correct
- Check if Redis instance is active
- Ensure IP whitelist includes Railway IPs (usually auto-added)

### "Website not found" on Worker
- Verify Redis has data (check Upstash console)
- Confirm website was generated in Flask API
- Check Cloudflare Worker logs

### CSV Upload Times Out
- Check Railway logs for API errors
- Verify ANTHROPIC_API_KEY is valid
- Increase Railway timeout settings if needed

### Custom Domain DNS Issues
- Wait 24-48 hours for DNS propagation
- Verify Cloudflare nameservers are set correctly
- Use online DNS checker: mxtoolbox.com

## Security Best Practices

1. **Environment Variables**: Never commit API keys - use Railway/Cloudflare env vars
2. **Redis Security**: Upstash URLs contain passwords - keep them private
3. **Cloudflare Security**: Enable DDoS protection, rate limiting
4. **Railway**: Enable custom branch deployments, add team members for approval
5. **CORS**: Configure CORS properly in Flask app for your domain
6. **HTTPS**: Enable SSL/TLS everywhere (Cloudflare auto-enables)

## Costs

| Service | Free Tier | Notes |
|---------|-----------|-------|
| Upstash | 10,000 commands/day, 1GB storage | Generous free tier |
| Railway | 500 hours/month | ~$5/month if exceeded |
| Cloudflare Pages | 500 builds/month, unlimited requests | Generous free tier |
| Cloudflare Workers | 100,000 requests/day | $0.50 per million after |
| **Total** | **~Free-$5/month** | Very affordable |

## Next Steps

1. Set environment variables in Railway
2. Deploy to Railway first (test API)
3. Deploy Pages with dashboard
4. Deploy Workers for website serving
5. Test end-to-end flow
6. Set up custom domain (optional)
