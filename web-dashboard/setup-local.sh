#!/bin/bash

echo "🚀 Lead Dashboard Local Setup"
echo "============================="
echo ""

# Check Python
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"

# Check Node
node_version=$(node --version 2>&1)
echo "✓ Node $node_version detected"

# Create .env
if [ ! -f api/.env ]; then
    echo ""
    echo "📝 Creating api/.env..."
    cp api/.env.example api/.env
    echo "✓ Created api/.env (edit with your API keys)"
else
    echo "✓ api/.env already exists"
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
cd api
pip install -q -r requirements.txt
cd ..
echo "✓ Python dependencies installed"

# Install Node dependencies (optional, for Cloudflare Workers)
if [ -d "cloudflare-worker" ]; then
    echo ""
    echo "📦 Installing Node dependencies for Cloudflare..."
    cd cloudflare-worker
    npm install -q
    cd ..
    echo "✓ Node dependencies installed"
fi

echo ""
echo "============================="
echo "✅ Setup complete!"
echo ""
echo "📌 Next steps:"
echo "1. Edit api/.env with your ANTHROPIC_API_KEY"
echo "2. (Optional) Add UPSTASH_REDIS_URL for cloud storage"
echo "3. Start API: cd api && python app.py"
echo "4. In another terminal, serve dashboard: cd public && python -m http.server 8080"
echo "5. Open browser to http://localhost:8080"
echo ""
echo "📚 For deployment: see DEPLOYMENT.md"
