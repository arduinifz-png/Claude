#!/bin/bash

echo "🚀 Claude Lead Agent Setup"
echo "=========================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ Created .env (edit with your ANTHROPIC_API_KEY)"
else
    echo "✓ .env file already exists"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "=========================="
echo "✅ Setup complete!"
echo ""
echo "📌 Next steps:"
echo "1. Edit .env and add your ANTHROPIC_API_KEY"
echo "2. Prepare your CSV file with lead data"
echo "3. Run: python lead_agent.py <your_file.csv>"
echo ""
echo "📚 Example: python lead_agent.py example_leads.csv results.json"
