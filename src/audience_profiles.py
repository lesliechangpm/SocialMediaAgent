from typing import Dict, List
from dataclasses import dataclass

@dataclass
class AudienceProfile:
    name: str
    age_range: str
    key_concerns: List[str]
    communication_style: str
    preferred_content: List[str]
    financial_priorities: List[str]
    messaging_focus: List[str]
    call_to_action_style: str

class AudienceTargeting:
    def __init__(self):
        self.profiles = {
            "baby_boomers": AudienceProfile(
                name="Baby Boomers",
                age_range="59-77",
                key_concerns=[
                    "Financial security in retirement",
                    "Protecting accumulated wealth",
                    "Legacy planning for children",
                    "Market stability and predictability",
                    "Fixed income considerations"
                ],
                communication_style="Professional, respectful, detailed explanations",
                preferred_content=[
                    "Market analysis and expert opinions",
                    "Long-term stability focus",
                    "Risk management strategies",
                    "Refinancing benefits for equity access",
                    "Reverse mortgage considerations"
                ],
                financial_priorities=[
                    "Debt reduction",
                    "Cash flow optimization",
                    "Asset preservation",
                    "Tax advantages",
                    "Estate planning alignment"
                ],
                messaging_focus=[
                    "Experience and expertise",
                    "Stability and security",
                    "Trusted advisor relationship",
                    "Conservative financial strategies",
                    "Personalized service"
                ],
                call_to_action_style="Respectful consultation invitation"
            ),
            
            "gen_x": AudienceProfile(
                name="Generation X",
                age_range="43-58",
                key_concerns=[
                    "Balancing family and financial goals",
                    "Children's education funding",
                    "Retirement planning catch-up",
                    "Home equity optimization",
                    "Career stability and income growth"
                ],
                communication_style="Straightforward, practical, time-conscious",
                preferred_content=[
                    "Refinancing opportunities",
                    "Home equity strategies",
                    "Investment property guidance",
                    "Debt consolidation benefits",
                    "Rate timing strategies"
                ],
                financial_priorities=[
                    "Maximizing home equity",
                    "Lower monthly payments",
                    "Debt consolidation",
                    "Education funding strategies",
                    "Building wealth through real estate"
                ],
                messaging_focus=[
                    "Practical financial solutions",
                    "Time-saving processes",
                    "Family-focused benefits",
                    "Smart financial moves",
                    "Experienced guidance"
                ],
                call_to_action_style="Direct consultation offer with clear benefits"
            ),
            
            "millennials": AudienceProfile(
                name="Millennials",
                age_range="27-42",
                key_concerns=[
                    "Homeownership affordability",
                    "Student loan debt management",
                    "Building credit and savings",
                    "Market timing and FOMO",
                    "Technology-driven solutions"
                ],
                communication_style="Casual, educational, digital-first",
                preferred_content=[
                    "First-time buyer education",
                    "Affordability strategies",
                    "Market timing insights",
                    "Down payment assistance programs",
                    "Technology and digital tools"
                ],
                financial_priorities=[
                    "Achieving homeownership",
                    "Managing multiple debts",
                    "Building emergency funds",
                    "Optimizing credit scores",
                    "Long-term wealth building"
                ],
                messaging_focus=[
                    "Educational content",
                    "Accessibility and inclusion",
                    "Technology integration",
                    "Future-focused planning",
                    "Community and social impact"
                ],
                call_to_action_style="Educational consultation with no pressure"
            )
        }
    
    def get_profile(self, audience: str) -> AudienceProfile:
        """Get audience profile by name"""
        return self.profiles.get(audience.lower().replace(" ", "_"), 
                                self.profiles["millennials"])
    
    def get_messaging_keywords(self, audience: str) -> List[str]:
        """Get relevant keywords for audience targeting"""
        profile = self.get_profile(audience)
        
        keyword_map = {
            "baby_boomers": [
                "stability", "security", "expertise", "trusted", "experienced",
                "conservative", "reliable", "established", "proven", "professional"
            ],
            "gen_x": [
                "practical", "efficient", "smart", "strategic", "family-focused",
                "time-saving", "value", "opportunity", "flexible", "results"
            ],
            "millennials": [
                "affordable", "accessible", "innovative", "transparent", "educational",
                "digital", "convenient", "future", "opportunity", "community"
            ]
        }
        
        return keyword_map.get(audience.lower().replace(" ", "_"), 
                              keyword_map["millennials"])
    
    def get_content_tone(self, audience: str, content_type: str) -> Dict[str, str]:
        """Get appropriate tone and style for content"""
        profile = self.get_profile(audience)
        
        base_tones = {
            "baby_boomers": {
                "educational": "Professional and authoritative with detailed explanations",
                "promotional": "Respectful and relationship-focused with expertise emphasis",
                "market_update": "Analytical and thoughtful with stability focus",
                "call_to_action": "Consultative and relationship-building"
            },
            "gen_x": {
                "educational": "Practical and straightforward with actionable insights",
                "promotional": "Benefit-focused and results-oriented",
                "market_update": "Strategic and opportunity-focused",
                "call_to_action": "Direct and value-proposition clear"
            },
            "millennials": {
                "educational": "Accessible and engaging with visual elements",
                "promotional": "Transparent and community-oriented",
                "market_update": "Trend-focused and future-looking",
                "call_to_action": "Low-pressure and educational-first"
            }
        }
        
        audience_key = audience.lower().replace(" ", "_")
        return base_tones.get(audience_key, base_tones["millennials"]).get(
            content_type, "Professional and helpful")
    
    def get_platform_optimization(self, audience: str, platform: str) -> Dict[str, any]:
        """Get platform-specific optimization for audience"""
        optimizations = {
            "facebook": {
                "baby_boomers": {
                    "post_length": "medium_to_long",
                    "hashtags": 2,
                    "emoji_usage": "minimal",
                    "engagement_style": "comment_encouraging",
                    "visual_style": "professional_charts"
                },
                "gen_x": {
                    "post_length": "medium",
                    "hashtags": 3,
                    "emoji_usage": "moderate",
                    "engagement_style": "question_based",
                    "visual_style": "infographics"
                },
                "millennials": {
                    "post_length": "short_to_medium",
                    "hashtags": 5,
                    "emoji_usage": "generous",
                    "engagement_style": "interactive",
                    "visual_style": "modern_graphics"
                }
            },
            "instagram": {
                "baby_boomers": {
                    "post_length": "medium",
                    "hashtags": 8,
                    "emoji_usage": "minimal",
                    "engagement_style": "informative",
                    "visual_style": "clean_professional"
                },
                "gen_x": {
                    "post_length": "short_to_medium",
                    "hashtags": 12,
                    "emoji_usage": "moderate",
                    "engagement_style": "story_driven",
                    "visual_style": "lifestyle_focused"
                },
                "millennials": {
                    "post_length": "short",
                    "hashtags": 15,
                    "emoji_usage": "high",
                    "engagement_style": "trendy",
                    "visual_style": "bold_colorful"
                }
            },
            "linkedin": {
                "baby_boomers": {
                    "post_length": "long",
                    "hashtags": 3,
                    "emoji_usage": "none",
                    "engagement_style": "thought_leadership",
                    "visual_style": "business_professional"
                },
                "gen_x": {
                    "post_length": "medium_to_long",
                    "hashtags": 4,
                    "emoji_usage": "rare",
                    "engagement_style": "industry_insights",
                    "visual_style": "data_driven"
                },
                "millennials": {
                    "post_length": "medium",
                    "hashtags": 5,
                    "emoji_usage": "minimal",
                    "engagement_style": "educational",
                    "visual_style": "modern_professional"
                }
            }
        }
        
        audience_key = audience.lower().replace(" ", "_")
        return optimizations.get(platform, {}).get(audience_key, 
                               optimizations["facebook"]["millennials"])
    
    def list_audiences(self) -> List[str]:
        """Get list of available audience segments"""
        return list(self.profiles.keys())
    
    def get_audience_summary(self, audience: str) -> str:
        """Get a brief summary of the audience segment"""
        profile = self.get_profile(audience)
        return f"{profile.name} ({profile.age_range}): {profile.communication_style}"