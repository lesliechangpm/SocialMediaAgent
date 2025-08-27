import os
from typing import Dict, List, Optional
from anthropic import Anthropic
from .audience_profiles import AudienceTargeting
import json

class SocialContentGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Claude API key"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.audience_targeting = AudienceTargeting()
    
    def generate_post(self, rate_data: Dict, platform: str, audience: str, 
                     content_type: str = "market_update", 
                     loan_officer_info: Optional[Dict] = None) -> Dict[str, str]:
        """
        Generate social media content optimized for platform and audience
        
        Args:
            rate_data: Dictionary with current rate information
            platform: 'facebook', 'instagram', or 'linkedin'
            audience: 'baby_boomers', 'gen_x', or 'millennials'
            content_type: 'educational', 'promotional', 'market_update', or 'call_to_action'
            loan_officer_info: Optional dictionary with loan officer details
        
        Returns:
            Dictionary with generated content and metadata
        """
        
        # Get audience profile and optimization settings
        profile = self.audience_targeting.get_profile(audience)
        platform_opts = self.audience_targeting.get_platform_optimization(audience, platform)
        tone = self.audience_targeting.get_content_tone(audience, content_type)
        keywords = self.audience_targeting.get_messaging_keywords(audience)
        
        # Build the prompt
        prompt = self._build_content_prompt(
            rate_data, platform, profile, platform_opts, tone, 
            keywords, content_type, loan_officer_info
        )
        
        # Generate content using Claude
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text.strip()
            
            # Parse the response to extract different components
            parsed_content = self._parse_generated_content(content, platform, platform_opts)
            
            return {
                "content": parsed_content["main_content"],
                "hashtags": parsed_content.get("hashtags", []),
                "visual_suggestions": parsed_content.get("visual_suggestions", ""),
                "platform": platform,
                "audience": audience,
                "content_type": content_type,
                "character_count": len(parsed_content["main_content"]),
                "rate_data": rate_data
            }
            
        except Exception as e:
            # Fallback to template-based content
            return self._generate_fallback_content(rate_data, platform, audience, content_type)
    
    def _build_content_prompt(self, rate_data: Dict, platform: str, profile, 
                             platform_opts: Dict, tone: str, keywords: List[str],
                             content_type: str, loan_officer_info: Optional[Dict]) -> str:
        """Build the comprehensive prompt for Claude"""
        
        # Format rate data for the prompt
        rate_change_text = "increased" if rate_data.get("rate_change", 0) > 0 else "decreased"
        if rate_data.get("rate_change", 0) == 0:
            rate_change_text = "remained steady"
        
        # Loan officer personalization
        lo_info = ""
        if loan_officer_info:
            lo_info = f"""
LOAN OFFICER INFO:
- Name: {loan_officer_info.get('name', 'Your Loan Officer')}
- Company: {loan_officer_info.get('company', 'Your Mortgage Company')}
- Location: {loan_officer_info.get('location', 'Your Area')}
- Specialties: {', '.join(loan_officer_info.get('specialties', ['Home Loans']))}
"""
        
        prompt = f"""You are an expert mortgage industry social media content creator. Generate engaging, professional social media content for loan officers.

CURRENT MORTGAGE DATA:
- 30-year fixed rate: {rate_data.get('current_rate', 'N/A')}%
- Previous rate: {rate_data.get('previous_rate', 'N/A')}%
- Weekly change: {rate_data.get('rate_change', 'N/A')}% ({rate_change_text})
- Date: {rate_data.get('date', 'Current')}
- Source: {rate_data.get('source', 'Market Data')}

TARGET SPECIFICATIONS:
- Platform: {platform.upper()}
- Audience: {profile.name} ({profile.age_range})
- Content Type: {content_type.replace('_', ' ').title()}
- Tone: {tone}

AUDIENCE PROFILE:
- Key Concerns: {', '.join(profile.key_concerns[:3])}
- Financial Priorities: {', '.join(profile.financial_priorities[:3])}
- Communication Style: {profile.communication_style}
- Messaging Focus: {', '.join(profile.messaging_focus[:3])}

PLATFORM REQUIREMENTS ({platform.upper()}):
- Post Length: {platform_opts.get('post_length', 'medium')}
- Hashtag Count: {platform_opts.get('hashtags', 5)}
- Emoji Usage: {platform_opts.get('emoji_usage', 'moderate')}
- Engagement Style: {platform_opts.get('engagement_style', 'interactive')}
- Character Limit: {'2200 for Instagram, 280 for Twitter' if platform == 'instagram' else '63,206 for Facebook' if platform == 'facebook' else '3000 for LinkedIn'}

{lo_info}

CONTENT REQUIREMENTS:
1. Start with an attention-grabbing hook related to current mortgage rates
2. Include the current rate prominently and context about the change
3. Provide value-driven insights relevant to {profile.name}
4. Address their key concerns: {', '.join(profile.key_concerns[:2])}
5. Include a subtle, professional call-to-action
6. Use keywords: {', '.join(keywords[:5])}
7. Match the {tone} tone
8. Optimize for {platform_opts.get('engagement_style', 'interactive')} engagement

FORMAT YOUR RESPONSE AS:

MAIN CONTENT:
[The social media post content here]

HASHTAGS:
[List of relevant hashtags, separated by spaces]

VISUAL SUGGESTIONS:
[Brief description of recommended visual content]

Generate content that feels authentic, provides genuine value, and encourages meaningful engagement while maintaining professional credibility."""
        
        return prompt
    
    def _parse_generated_content(self, content: str, platform: str, platform_opts: Dict) -> Dict:
        """Parse the generated content into components"""
        lines = content.split('\n')
        
        result = {
            "main_content": "",
            "hashtags": [],
            "visual_suggestions": ""
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.upper().startswith("MAIN CONTENT:"):
                current_section = "main_content"
                continue
            elif line.upper().startswith("HASHTAGS:"):
                current_section = "hashtags"
                continue
            elif line.upper().startswith("VISUAL SUGGESTIONS:"):
                current_section = "visual_suggestions"
                continue
            
            if current_section == "main_content" and line:
                result["main_content"] += line + " "
            elif current_section == "hashtags" and line:
                # Extract hashtags
                hashtags = [tag.strip() for tag in line.split() if tag.startswith('#')]
                result["hashtags"].extend(hashtags)
            elif current_section == "visual_suggestions" and line:
                result["visual_suggestions"] += line + " "
        
        # Clean up
        result["main_content"] = result["main_content"].strip()
        result["visual_suggestions"] = result["visual_suggestions"].strip()
        
        # If parsing failed, treat entire content as main content
        if not result["main_content"]:
            result["main_content"] = content.strip()
        
        return result
    
    def _generate_fallback_content(self, rate_data: Dict, platform: str, 
                                  audience: str, content_type: str) -> Dict[str, str]:
        """Generate template-based content as fallback"""
        
        profile = self.audience_targeting.get_profile(audience)
        
        # Simple template-based content
        rate = rate_data.get("current_rate", 7.0)
        change = rate_data.get("rate_change", 0)
        
        if audience.lower() == "millennials":
            content = f"🏠 30-year mortgage rates are at {rate}% this week! "
            if change < 0:
                content += f"That's down {abs(change):.2f}% - could be a great time for first-time buyers to explore their options!"
            elif change > 0:
                content += f"Up {change:.2f}% from last week, but still within reach for many buyers."
            else:
                content += "Staying steady - perfect time to get pre-approved!"
            
            content += " Ready to explore your homeownership options? Let's chat! 💬"
            hashtags = ["#MortgageRates", "#FirstTimeBuyer", "#Homeownership", "#RealEstate"]
            
        elif audience.lower() == "gen_x":
            content = f"📊 This week's 30-year mortgage rate: {rate}%. "
            if change != 0:
                content += f"That's a {abs(change):.2f}% {'increase' if change > 0 else 'decrease'} from last week. "
            
            content += "If you've been considering refinancing or tapping into your home's equity, now might be the right time to review your options. "
            content += "Let's discuss how current rates could benefit your financial strategy."
            hashtags = ["#MortgageRates", "#Refinancing", "#HomeEquity", "#FinancialPlanning"]
            
        else:  # Baby Boomers
            content = f"Current 30-year fixed mortgage rate: {rate}%. "
            content += f"Market analysis shows rates have {'risen' if change > 0 else 'declined' if change < 0 else 'remained stable'} this week. "
            content += "For those considering refinancing options or exploring reverse mortgage solutions, "
            content += "I'm here to provide expert guidance tailored to your unique financial situation. "
            content += "Contact me for a personalized consultation."
            hashtags = ["#MortgageRates", "#RefinanceOptions", "#RetirementPlanning"]
        
        return {
            "content": content,
            "hashtags": hashtags,
            "visual_suggestions": "Professional chart showing current rates and trends",
            "platform": platform,
            "audience": audience,
            "content_type": content_type,
            "character_count": len(content),
            "rate_data": rate_data
        }
    
    def generate_content_variations(self, rate_data: Dict, platform: str, 
                                   audience: str, count: int = 3) -> List[Dict]:
        """Generate multiple content variations for A/B testing"""
        variations = []
        content_types = ["educational", "market_update", "promotional"]
        
        for i, content_type in enumerate(content_types[:count]):
            try:
                variation = self.generate_post(rate_data, platform, audience, content_type)
                variation["variation_id"] = i + 1
                variations.append(variation)
            except Exception as e:
                print(f"Failed to generate variation {i+1}: {e}")
                continue
        
        return variations
    
    def get_platform_limits(self, platform: str) -> Dict[str, int]:
        """Get character limits and recommendations for each platform"""
        limits = {
            "facebook": {
                "character_limit": 63206,
                "recommended_length": 400,
                "hashtag_limit": 30,
                "recommended_hashtags": 5
            },
            "instagram": {
                "character_limit": 2200,
                "recommended_length": 300,
                "hashtag_limit": 30,
                "recommended_hashtags": 15
            },
            "linkedin": {
                "character_limit": 3000,
                "recommended_length": 600,
                "hashtag_limit": 20,
                "recommended_hashtags": 5
            }
        }
        
        return limits.get(platform, limits["facebook"])