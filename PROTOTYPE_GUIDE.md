# Mortgage Rate Social Media Agent - Working Prototype

## 🚀 READY TO USE - NO API KEYS REQUIRED!

This is a fully functional prototype of the Mortgage Rate Social Media Agent that works without any API keys or external dependencies. It uses built-in templates and mock data to demonstrate all the core functionality.

## Quick Start

```bash
cd mortgage-rate-agent
python prototype.py --help
```

## Available Commands

### 1. Generate Content
```bash
# Generate Instagram post for millennials
python prototype.py generate -p instagram -a millennials -t educational

# Generate Facebook post for Gen X with personalization
python prototype.py generate -p facebook -a gen_x -t promotional --loan-officer "John Smith" --company "ABC Mortgage"

# Generate LinkedIn post for Baby Boomers
python prototype.py generate -p linkedin -a baby_boomers -t market_update
```

### 2. Get Current Rates
```bash
python prototype.py rates
```

### 3. Generate Multiple Variations
```bash
# Create 3 different versions for A/B testing
python prototype.py variations -p instagram -a millennials -n 3
```

### 4. View Information
```bash
# See all audience segments
python prototype.py audiences

# View platform specifications
python prototype.py platform-info facebook
python prototype.py platform-info instagram
python prototype.py platform-info linkedin
```

### 5. Save Content
```bash
# Save generated content to JSON file
python prototype.py generate -p instagram -a millennials --save my_content.json
```

## Sample Outputs

### Rate Display
```
CURRENT MORTGAGE RATE DATA
==================================================
30-Year Fixed Rate: 7.41%
Previous Rate: 7.42%
Weekly Change: -0.01% (DECREASED)
Date: 2025-08-26
Source: Mock Rate Data
Year Ago Rate: 5.96%
Trend: Decreasing
```

### Content Generation
```
GENERATED CONTENT:
----------------------------------------
Rate update: 6.68% for 30-year fixed loans. Pre-approval helps you shop with confidence. 
Your dream home might be more affordable than you think! Let's run some numbers together.

#FirstTimeBuyer #Homeownership #MortgageRates #RealEstate #HomeBuying #MortgageProfessional

CONTENT STATS:
  - Character Count: 343
  - Hashtag Count: 11
  - Platform: Instagram
  - Audience: Millennials
  - Content Type: Educational

VISUAL SUGGESTIONS:
  - Primary: Bright, colorful rate infographic with clean design
  - Secondary: Behind-the-scenes story of rate research process
  - Style Notes: Use trending colors, modern fonts, mobile-first design

POSTING TIPS:
  - Post between 11 AM-1 PM for maximum reach
  - Use Stories for behind-the-scenes content
  - Engage with followers' content to build relationships
```

## Features Demonstrated

### ✅ Audience Targeting
- **Millennials (27-42)**: Casual, educational, affordability-focused
- **Gen X (43-58)**: Practical, family-oriented, refinancing-focused  
- **Baby Boomers (59-77)**: Professional, security-focused, detailed

### ✅ Platform Optimization
- **Facebook**: Conversational tone, 3 hashtags, discussion-focused
- **Instagram**: Visual-first, 12 hashtags, trendy language
- **LinkedIn**: Professional insights, 5 hashtags, thought leadership

### ✅ Content Types
- **Educational**: Teaching and informing about rates and market
- **Market Update**: Current rate information with context
- **Promotional**: Showcasing expertise and services

### ✅ Dynamic Elements
- Mock rate data that changes each run
- Contextual messaging based on rate trends
- Audience-specific language and concerns
- Platform-appropriate formatting

### ✅ Personalization
- Loan officer name integration
- Company branding
- Custom messaging elements

## Command Reference

### Core Options
- `-p, --platform`: facebook, instagram, linkedin (required)
- `-a, --audience`: millennials, gen_x, baby_boomers (required)
- `-t, --type`: educational, market_update, promotional (default: market_update)
- `--loan-officer`: Add loan officer name for personalization
- `--company`: Add company name for branding
- `--save`: Save output to JSON file

### Information Commands
- `rates`: Show current mortgage rate data
- `audiences`: List all audience segments with details
- `platform-info [platform]`: Show platform specifications
- `variations -p [platform] -a [audience] -n [count]`: Generate multiple versions

## Example Workflow

```bash
# 1. Check current rates
python prototype.py rates

# 2. See available audiences
python prototype.py audiences

# 3. Generate content for your target
python prototype.py generate -p instagram -a millennials -t educational \
  --loan-officer "Sarah Johnson" --company "Premier Mortgage"

# 4. Create variations for testing
python prototype.py variations -p facebook -a gen_x -n 3

# 5. Save your favorite version
python prototype.py generate -p linkedin -a baby_boomers -t promotional \
  --loan-officer "Robert Wilson" --save linkedin_post.json
```

## How It Works

### Mock Rate Data Generator
- Generates realistic rate data (6.5-7.8% range)
- Creates weekly changes and trends
- Includes year-over-year comparisons
- Updates with each run for testing

### Template Engine
- 27 pre-built content templates (3 audiences × 3 content types × 3 variations each)
- Dynamic content insertion based on rate data
- Audience-specific messaging and tone
- Platform-optimized formatting

### Smart Personalization
- Contextual messaging based on rate trends
- Audience-appropriate concerns and benefits
- Platform-specific best practices
- Professional formatting and hashtag optimization

## Differences from Full Version

| Feature | Prototype | Full Version |
|---------|-----------|--------------|
| Content Generation | Built-in templates | AI-powered with Claude API |
| Rate Data | Mock data | Live feeds from Freddie Mac, etc. |
| Personalization | Basic insertion | Advanced AI customization |
| Content Variety | 27 templates | Unlimited AI variations |
| Rate Sources | Simulated | Multiple real-time sources |

## Next Steps

1. **Test All Features**: Try all commands and options
2. **Customize Templates**: Edit templates in `prototype.py` for your style
3. **Add Real Data**: When ready, upgrade to full version with live data
4. **API Integration**: Use full version with Claude API for unlimited content

## Ready for Production?

This prototype demonstrates the full concept and workflow. When you're ready for the production version with Claude AI and live rate data:

1. Set your `ANTHROPIC_API_KEY` environment variable
2. Use the full system: `python -m src.main generate -p instagram -a millennials`
3. Get unlimited, AI-generated content variations

---

**Status: ✅ PROTOTYPE COMPLETE AND FULLY FUNCTIONAL**

No API keys needed - test everything right now!