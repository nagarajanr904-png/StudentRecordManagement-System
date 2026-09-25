#!/usr/bin/env bash
# ==============================================================================
# ScholarPulse - Automated GitHub Repository Push Script
# Usage: ./push_to_github.sh <YOUR_GITHUB_REPO_URL>
# Example: ./push_to_github.sh https://github.com/yourusername/scholarpulse-srm.git
# ==============================================================================

set -e

REPO_URL="$1"

if [ -z "$REPO_URL" ]; then
    echo "======================================================================"
    echo "  ScholarPulse - GitHub Repository Setup & Push"
    echo "======================================================================"
    echo ""
    echo "Please provide your GitHub repository URL:"
    echo "  Example: ./push_to_github.sh https://github.com/yourname/scholarpulse.git"
    echo ""
    echo "Steps to create your free GitHub repository:"
    echo "1. Go to https://github.com/new"
    echo "2. Set Repository Name (e.g. 'scholarpulse-srm')"
    echo "3. Choose 'Public' or 'Private'"
    echo "4. DO NOT initialize with README (already provided)"
    echo "5. Click 'Create repository' and copy the URL"
    echo ""
    read -p "Enter your GitHub repository URL: " REPO_URL
fi

if [ -z "$REPO_URL" ]; then
    echo "❌ No repository URL provided. Aborting."
    exit 1
fi

echo "🚀 Configuring Git remote origin: $REPO_URL..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

echo "📦 Ensuring all files are tracked and committed..."
git add -A
git commit -m "feat: ScholarPulse Academic Records & Free Online MySQL System" --allow-empty

echo "🌿 Setting default branch to main..."
git branch -M main

echo "⬆️ Pushing to GitHub (origin main)..."
git push -u origin main

echo ""
echo "🎉 Successfully pushed to GitHub: $REPO_URL"
echo "🌐 Your repository is live on GitHub!"
echo "✨ Free GitHub Pages deployment will automatically run via .github/workflows/deploy.yml"
echo ""
