# Mortgage Rate Social Media Agent

An AI-powered tool that automatically fetches current mortgage rate data and generates targeted social media content for loan officers to build their following and promote their services.

## Features

- 📊 **Automatic Rate Data Fetching**: Gets current 30-year mortgage rates from reliable sources
- 🎯 **Audience Targeting**: Generates content optimized for Baby Boomers, Gen X, or Millennials  
- 📱 **Platform Optimization**: Formats content specifically for Facebook, Instagram, or LinkedIn
- 🤖 **AI Content Generation**: Uses Claude AI to create engaging, professional posts
- ✅ **Content Validation**: Ensures posts meet platform requirements and best practices
- 📈 **Multiple Content Types**: Educational, promotional, market updates, and call-to-action posts

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Your API Key**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

3. **Generate Content**
   ```bash
   python -m src.main generate --platform instagram --audience millennials --tone educational
   ```

## Usage Examples

### Generate Basic Content
```bash
# Generate a market update for millennials on Instagram
python -m src.main generate -p instagram -a millennials -t market_update

# Generate educational content for Gen X on LinkedIn
python -m src.main generate -p linkedin -a gen_x -t educational --preview

# Generate promotional content for Baby Boomers on Facebook
python -m src.main generate -p facebook -a baby_boomers -t promotional --loan-officer "John Smith" --company "ABC Mortgage"
```

### Generate Multiple Variations
```bash
# Create 3 different versions for A/B testing
python -m src.main variations -p facebook -a gen_x -n 3
```

### Check Current Rates
```bash
# View current mortgage rate data
python -m src.main rates
```

### Get Platform Information
```bash
# See platform specs and best practices
python -m src.main platform-info instagram

# List available audience segments  
python -m src.main audiences
```

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional personalization
DEFAULT_LOAN_OFFICER_NAME=Your Name
DEFAULT_COMPANY_NAME=Your Mortgage Company  
DEFAULT_LOCATION=Your City, State
```

### Settings
Customize behavior in `config/settings.yaml`:
- Content generation parameters
- Platform limits and recommendations  
- Audience targeting preferences
- Rate data sources
- Compliance settings

## Command Line Options

### Generate Command
```bash
python -m src.main generate [OPTIONS]

Options:
  -p, --platform [facebook|instagram|linkedin]  Target platform (required)
  -a, --audience [millennials|gen_x|baby_boomers]  Target audience (required)  
  -t, --tone [educational|promotional|market_update|call_to_action]  Content type
  --loan-officer TEXT    Loan officer name for personalization
  --company TEXT         Company name for personalization
  --location TEXT        Location for local market context
  --output PATH          Save output to JSON file
  --preview              Preview content before finalizing
```

### Other Commands
- `variations` - Generate multiple content versions
- `rates` - Show current mortgage rate data
- `audiences` - List available audience segments
- `platform-info` - Show platform specifications

## Output Example

```
📊 CURRENT MORTGAGE RATE DATA
30-Year Fixed Rate: 7.25%
Previous Rate: 7.31%  
Weekly Change: -0.06% ⬇️

📝 GENERATED CONTENT:
🏠 Great news for potential homebuyers! 30-year mortgage rates dropped to 7.25% this week - down 0.06% from last week. This small decrease could mean significant savings over the life of your loan...

🏷️ HASHTAGS: #MortgageRates #FirstTimeBuyer #Homeownership #RealEstate #HomeLoan

📊 CONTENT STATS:
• Character Count: 284
• Hashtag Count: 5
• Platform: Instagram  
• Audience: Millennials

🎨 VISUAL SUGGESTIONS:
• Primary: Bright, eye-catching infographic with rate highlights
• Secondary: Story series breaking down rate information  

⏰ OPTIMAL POSTING TIMES:
• Weekdays: 11 AM-1 PM, 5-7 PM
• Weekends: 10 AM-12 PM
```

## Architecture

- **`data_fetcher.py`** - Fetches mortgage rate data from multiple sources
- **`audience_profiles.py`** - Defines target audience characteristics and preferences  
- **`content_generator.py`** - AI-powered content generation using Claude API
- **`platform_optimizer.py`** - Platform-specific formatting and optimization
- **`main.py`** - Command-line interface and orchestration

## Audience Segments

### Millennials (27-42)
- Focus: Affordability, first-time buying, education
- Platforms: Instagram, Facebook
- Tone: Casual, educational, digital-first

### Generation X (43-58)  
- Focus: Refinancing, family benefits, practical solutions
- Platforms: Facebook, LinkedIn
- Tone: Straightforward, time-conscious, results-oriented

### Baby Boomers (59-77)
- Focus: Stability, security, expert guidance
- Platforms: Facebook, LinkedIn  
- Tone: Professional, detailed, relationship-focused

## Platform Optimization

### Facebook
- Optimal length: ~400 characters
- Hashtags: 3-5 recommended
- Best times: 1-3 PM weekdays

### Instagram  
- Optimal length: ~300 characters
- Hashtags: 10-15 recommended
- Best times: 11 AM-1 PM, 5-7 PM weekdays

### LinkedIn
- Optimal length: ~600 characters  
- Hashtags: 3-5 recommended
- Best times: 8-10 AM, 12-2 PM weekdays

## Data Sources

The system fetches mortgage rate data from:
1. **Freddie Mac PMMS** - Primary source for 30-year fixed rates
2. **Financial News RSS** - Backup source with market context
3. **Cached Data** - Fallback when live sources unavailable

## Compliance Features

- Required disclaimers automatically added
- Content validation for compliance keywords
- NMLS ID integration for loan officer posts
- Equal Housing Opportunity notices

## Development

### Project Structure
```
mortgage-rate-agent/
├── src/                    # Main application code
├── config/                 # Configuration files  
├── data/                   # Local data storage
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .env.example           # Environment variables template
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes  
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or support:
1. Check the documentation in this README
2. Review the configuration files in `config/`
3. Examine the example outputs and commands above
4. Open an issue on the project repository

## Roadmap

Future enhancements may include:
- Direct posting to social media platforms
- Content scheduling and automation
- Performance analytics and optimization
- Additional rate data sources
- Custom prompt templates
- Team collaboration features