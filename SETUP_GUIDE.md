# Social Media Agent - Quick Setup Guide

## Current Status: ✅ Ready to Use (with API Key)

Your social media agent is fully functional! The system includes:
- ✅ Rate data fetching with fallback
- ✅ Advanced audience targeting (Gen Z, Millennials, Gen X, Baby Boomers)
- ✅ Platform optimization (Instagram, Facebook, LinkedIn)
- ✅ Fallback content generation when AI is unavailable
- ✅ Comprehensive audience insights and platform guides

## To Enable AI Content Generation

### Step 1: Get Your Anthropic API Key
1. Visit https://console.anthropic.com/
2. Create an account or sign in
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

### Step 2: Configure the Agent
1. Open the `.env` file in the mortgage-rate-agent folder
2. Replace `your_anthropic_api_key_here` with your actual API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ```
3. Save the file

### Step 3: Test the Agent
```bash
cd mortgage-rate-agent
python social_media_agent.py generate -p instagram -a millennials --loan-officer "Leslie Chang" --company "CMG Mortgage"
```

## Working Features Right Now (No API Key Needed)

### 1. Rate Data Analysis
```bash
python social_media_agent.py rates
```

### 2. Audience Targeting Guide
```bash
python social_media_agent.py audiences
```

### 3. Platform Information
```bash
python social_media_agent.py platform-info instagram
python social_media_agent.py platform-info facebook
python social_media_agent.py platform-info linkedin
```

### 4. Basic Content Generation (Fallback Templates)
```bash
# These work without API key using smart templates
python social_media_agent.py generate -p instagram -a millennials --loan-officer "Leslie Chang" --company "CMG Mortgage"
python social_media_agent.py variations -p facebook -a gen_x -n 3
```

## Menu Interface (Double-click to run)
- Windows: Double-click `social_media_agent.bat`
- This gives you an easy menu interface for all functions

## What You Get With AI (After API Key Setup)
- ✨ Intelligent, personalized content for each audience
- ✨ Market-aware content that references current rates
- ✨ Platform-optimized formatting and hashtags
- ✨ Advanced targeting with emotional triggers
- ✨ Professional compliance and safety features
- ✨ Multiple content variations for A/B testing

## Cost Information
- Anthropic Claude API costs ~$0.01-0.03 per social media post
- Very affordable for professional mortgage marketing
- Much cheaper than hiring a content writer

## Your System is Production-Ready!
Everything is configured and working. Just add your API key to unlock the full AI-powered features.

---
**Leslie Chang - CMG Mortgage | Ready to Scale Your Social Media Presence** 🚀