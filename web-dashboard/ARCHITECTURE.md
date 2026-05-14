# System Architecture

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER FLOW                                          │
└─────────────────────────────────────────────────────────────────────────────┘

1. USER UPLOADS CSV
   ↓
   ┌─────────────────────────┐
   │  Cloudflare Pages       │  ← Static Dashboard (HTML/JS)
   │  (yourapp.com)          │
   └────────────┬────────────┘
                │ POST /api/process-csv
                ↓
   ┌─────────────────────────┐
   │  Railway API            │  ← Python Flask Backend
   │  (api.yourapp.com)      │
   │                         │
   │  1. Parse CSV           │
   │  2. Qualify leads       │
   │  3. Call Claude API     │
   │  4. Generate websites   │
   │  5. Store in Redis      │
   └────────┬────────────────┘
            │
            ├──────────────────────────────────┐
            ↓                                  ↓
   ┌──────────────────┐        ┌──────────────────────┐
   │  Upstash Redis   │        │ Anthropic Claude API │
   │  (Data Storage)  │        │ (AI Generation)      │
   └──────────────────┘        └──────────────────────┘
            ↑
            │ Store websites
            │
   ┌─────────────────────────────────────────┐
   │  Cloudflare Workers                     │
   │  (website.yourapp.com/website/{id})     │
   │                                         │
   │  - Retrieves HTML from Redis            │
   │  - Serves at edge (CDN cached)          │
   │  - Global distribution                  │
   └──────────────┬──────────────────────────┘
                  │
                  ↓
   User gets shareable links: https://yourapp.com/website/abc123


┌─────────────────────────────────────────────────────────────────────────────┐
│                        TECHNICAL ARCHITECTURE                                │
└─────────────────────────────────────────────────────────────────────────────┘

                              GitHub
                                │
                   ┌────────────┴────────────┐
                   │                        │
                   ↓                        ↓
            ┌─────────────┐        ┌──────────────┐
            │  Railway    │        │  Cloudflare  │
            │  (API)      │        │  (Pages/CDN) │
            └──────┬──────┘        └──────┬───────┘
                   │                      │
                   │ pull from Redis      │ static assets
                   │                      │
            ┌──────┴──────────────────────┴──────┐
            │                                    │
            ↓                                    ↓
        ┌─────────────────┐            ┌──────────────┐
        │  Upstash Redis  │            │  Cloudflare  │
        │  • HTML storage │            │  Workers     │
        │  • Metadata     │            │  • Serve     │
        │  • Sessions     │            │  • Cache     │
        └────────┬────────┘            │  • Edge      │
                 │                     └──────┬───────┘
                 │                           │
                 └───────────┬────────────────┘
                             │
                             ↓
                    Global User Access


┌─────────────────────────────────────────────────────────────────────────────┐
│                         DEPLOYMENT TOPOLOGY                                  │
└─────────────────────────────────────────────────────────────────────────────┘

GitHub Repository
│
├── main branch
│   └── Production deploys
│
└── claude/build-claude-agents-X3gVy (current)
    │
    ├── /api/ → Railway Deployment
    │   ├── Flask app runs on railway.app
    │   ├── Connects to Upstash Redis
    │   ├── Calls Claude API
    │   └── Generates websites
    │
    ├── /public/ → Cloudflare Pages
    │   ├── Static hosting on pages.dev
    │   ├── Dashboard UI
    │   └── Calls Railway API
    │
    └── /cloudflare-worker/ → Cloudflare Workers
        ├── Edge computing
        ├── Serves websites from Redis
        └── Global distribution


┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATA FLOW TIMELINE                                  │
└─────────────────────────────────────────────────────────────────────────────┘

T+0s    User uploads CSV to dashboard (Cloudflare Pages)
        └─→ POST /api/process-csv to Railway

T+1s    Railway receives CSV
        ├─→ Parses CSV content
        ├─→ Qualifies leads (finds ones without websites)
        └─→ For each lead, calls Claude API

T+30s   Claude API returns specifications
        ├─→ Website purpose
        ├─→ SEO strategy
        ├─→ Content architecture
        └─→ etc.

T+35s   Flask generates HTML from specifications
        ├─→ Creates responsive website
        ├─→ Adds modern styling
        └─→ Includes CTAs and contact forms

T+40s   HTML stored in Upstash Redis
        ├─→ Assigned unique website_id (e.g., abc123)
        ├─→ Set TTL to 30 days
        └─→ Indexed by key: website:abc123

T+45s   Results returned to dashboard
        ├─→ Project ID for tracking
        ├─→ Statistics (total, qualified, generated)
        └─→ Shareable links for each website

T+46s   User clicks "Copy Link"
        └─→ Link copied to clipboard
            Example: https://yourapp.com/website/abc123

T+50s   User sends link to client
        └─→ Client opens link

T+51s   Cloudflare Worker intercepts request
        ├─→ Extracts website_id (abc123)
        ├─→ Queries Upstash Redis
        ├─→ Retrieves HTML content
        ├─→ Caches at edge
        └─→ Returns to user

T+52s   Client sees professional website
        └─→ Served from nearest Cloudflare edge
        └─→ <100ms load time globally


┌─────────────────────────────────────────────────────────────────────────────┐
│                       INFRASTRUCTURE DECISIONS                               │
└─────────────────────────────────────────────────────────────────────────────┘

Why Each Component:

┌─ Cloudflare Pages (Dashboard)
│  ✓ Free static hosting
│  ✓ Global CDN included
│  ✓ Auto-deploys from GitHub
│  ✓ HTTPS automatic
│  ✗ Can't run Python
│
├─ Railway (API Backend)
│  ✓ Easy Python deployment
│  ✓ Auto-deploys from GitHub
│  ✓ Free tier ($0-5/month)
│  ✓ Environment variables built-in
│  ✓ Logs and monitoring included
│  ✗ Could be replaced with Workers if using Node
│
├─ Upstash Redis
│  ✓ Serverless (no management)
│  ✓ Works with Cloudflare Workers
│  ✓ Free tier (10K commands/day)
│  ✓ Auto-scaling
│  ✓ REST API for Workers
│  ✗ Data destroyed after 30-day inactivity
│
└─ Cloudflare Workers
   ✓ Edge computing (global)
   ✓ <100ms latency worldwide
   ✓ 100K requests/day free
   ✓ Connects directly to Upstash
   ✓ Excellent caching
   ✗ Limited to JavaScript/WebAssembly


┌─────────────────────────────────────────────────────────────────────────────┐
│                        SCALING CONSIDERATIONS                                │
└─────────────────────────────────────────────────────────────────────────────┘

Current Scale (Free Tier):
├─ ~10 CSV uploads/day
├─ ~100 websites generated/day
├─ ~1000 website views/day
└─ Cost: $0-5/month

At Scale (Paid Tier):
├─ ~1000 CSV uploads/day
├─ ~10K websites generated/day
├─ ~100K website views/day
└─ Cost: $100-500/month

Optimization Points:
├─ Add caching layer between Railway and Claude
├─ Queue system for batch processing (Bull/BullMQ)
├─ CDN caching for website assets
├─ Compression for HTML before Redis storage
├─ Analytics tracking (Cloudflare Analytics Engine)
└─ Database migration (PostgreSQL) if >10K websites


┌─────────────────────────────────────────────────────────────────────────────┐
│                         SECURITY ARCHITECTURE                                │
└─────────────────────────────────────────────────────────────────────────────┘

API Layer (Railway):
├─ Environment variables (no hardcoded secrets)
├─ CORS enabled for domains
├─ Input validation on CSV
├─ Rate limiting on API endpoints
└─ Logs don't contain sensitive data

Edge Layer (Cloudflare Workers):
├─ Runs in isolated context
├─ DDoS protection included
├─ Rate limiting available
├─ No access to API keys
└─ Cache headers prevent leaking

Data Layer (Upstash Redis):
├─ Password in connection string
├─ Encrypted in transit
├─ 30-day auto-expiry (GDPR)
├─ No public access without credentials
└─ IP whitelisting available

Client Layer (Dashboard):
├─ No API keys in frontend code
├─ API endpoint configured via env vars
├─ HTTPS only (Cloudflare enforced)
├─ No sensitive data in localStorage
└─ CORS properly configured
