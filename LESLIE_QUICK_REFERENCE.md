# Leslie Chang - CMG Mortgage | Quick Reference Guide

## Your Personalized Command Templates

### Instagram (Millennials - First-Time Buyers)
```bash
# Educational content
python prototype.py generate -p instagram -a millennials -t educational --loan-officer "Leslie Chang" --company "CMG Mortgage"

# Market updates
python prototype.py generate -p instagram -a millennials -t market_update --loan-officer "Leslie Chang" --company "CMG Mortgage"

# Promotional posts
python prototype.py generate -p instagram -a millennials -t promotional --loan-officer "Leslie Chang" --company "CMG Mortgage"
```

### Facebook (Gen X - Refinancing Focus)
```bash
# Market updates with strategy focus
python prototype.py generate -p facebook -a gen_x -t market_update --loan-officer "Leslie Chang" --company "CMG Mortgage"

# Educational content about refinancing
python prototype.py generate -p facebook -a gen_x -t educational --loan-officer "Leslie Chang" --company "CMG Mortgage"

# Professional services promotion
python prototype.py generate -p facebook -a gen_x -t promotional --loan-officer "Leslie Chang" --company "CMG Mortgage"
```

### LinkedIn (Baby Boomers - Professional Network)
```bash
# Thought leadership content
python prototype.py generate -p linkedin -a baby_boomers -t educational --loan-officer "Leslie Chang" --company "CMG Mortgage"

# Market analysis posts
python prototype.py generate -p linkedin -a baby_boomers -t market_update --loan-officer "Leslie Chang" --company "CMG Mortgage"

# Professional expertise showcase
python prototype.py generate -p linkedin -a baby_boomers -t promotional --loan-officer "Leslie Chang" --company "CMG Mortgage"
```

## Sample Content Generated for Leslie Chang - CMG Mortgage

### Instagram Example (Millennials - Promotional)
```
With rates at 7.33%, I'm here to help you navigate today's market! I make the homebuying 
process clear, simple, and stress-free. Ready to turn your homeownership dreams into reality? 
Let's connect!

- Leslie Chang, CMG Mortgage

#FirstTimeBuyer #Homeownership #MortgageRates #RealEstate #HomeBuying #MortgageProfessional 
#HomeLoanExpert #BuyingAHome #MortgageAdvice #RateUpdate #HomeFinancing
```

### Facebook Example (Gen X - Market Update)
```
This week: rates dropping to 6.84%. Consider closing costs vs. monthly savings. Ready to make 
your next smart financial move? I'm here to help.

- Leslie Chang, CMG Mortgage

#Refinancing #MortgageRates #HomeEquity
```

### LinkedIn Example (Baby Boomers - Educational)
```
Rate update: 30-year mortgages at 6.9%. Financial security should always be the primary 
consideration. Whether refinancing or exploring reverse mortgage options, let's discuss your 
financial security.

- Leslie Chang, CMG Mortgage

#MortgageExpert #RefinanceOptions #HomeLoans #RetirementPlanning #MortgageProfessional
```

## Quick Daily Workflow

### Monday Morning - Week Setup
```bash
# Check current rates
python prototype.py rates

# Generate content for the week
python prototype.py variations -p instagram -a millennials -n 3 --loan-officer "Leslie Chang" --company "CMG Mortgage"
```

### Throughout the Week
```bash
# Instagram (daily) - Target millennials
python prototype.py generate -p instagram -a millennials -t educational --loan-officer "Leslie Chang" --company "CMG Mortgage"

# Facebook (3x/week) - Target Gen X families  
python prototype.py generate -p facebook -a gen_x -t market_update --loan-officer "Leslie Chang" --company "CMG Mortgage"

# LinkedIn (2x/week) - Professional network
python prototype.py generate -p linkedin -a baby_boomers -t promotional --loan-officer "Leslie Chang" --company "CMG Mortgage"
```

### Save Your Best Content
```bash
# Save to files for scheduling tools
python prototype.py generate -p instagram -a millennials --loan-officer "Leslie Chang" --company "CMG Mortgage" --save monday_instagram.json

python prototype.py generate -p facebook -a gen_x --loan-officer "Leslie Chang" --company "CMG Mortgage" --save tuesday_facebook.json
```

## Your Audience Breakdown

### Instagram - Millennials (27-42)
- **Focus**: First-time homebuying, affordability, education
- **Tone**: Casual, encouraging, accessible
- **Best Times**: 11 AM-1 PM, 5-7 PM weekdays
- **Hashtags**: 10-12 recommended
- **Content**: Visual-first, behind-the-scenes, educational

### Facebook - Gen X (43-58) 
- **Focus**: Refinancing, family financial strategy, home equity
- **Tone**: Practical, results-oriented, straightforward
- **Best Times**: 1-3 PM weekdays
- **Hashtags**: 3-5 recommended  
- **Content**: Discussion-focused, family benefits, strategic advice

### LinkedIn - Baby Boomers (59-77)
- **Focus**: Financial security, retirement planning, expert guidance
- **Tone**: Professional, respectful, detailed
- **Best Times**: 8-10 AM, 12-2 PM weekdays
- **Hashtags**: 3-5 recommended
- **Content**: Thought leadership, market analysis, professional expertise

## Pro Tips for Leslie

1. **Rate Timing**: Use `python prototype.py rates` to check current data before posting
2. **A/B Testing**: Use `variations` command to create multiple versions, then track performance
3. **Personalization**: Always include your name and CMG Mortgage for brand consistency
4. **Platform Strategy**: 
   - Instagram: Daily posts, focus on education and opportunity
   - Facebook: 3x/week, focus on family benefits and smart money moves
   - LinkedIn: 2x/week, focus on expertise and professional insights
5. **Content Mix**: Rotate between educational (50%), market updates (30%), promotional (20%)

## Ready to Scale Up?

When you get your Anthropic API key restored:
- Switch to full AI system: `python -m src.main generate -p instagram -a millennials`
- Get unlimited content variations with Claude AI
- Access live mortgage rate data feeds
- Advanced personalization and compliance features

---

**Leslie Chang | CMG Mortgage | Mortgage Rate Social Media Agent**
*Helping families achieve homeownership through smart mortgage solutions*