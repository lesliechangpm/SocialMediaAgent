from typing import Dict, List, Tuple
import re
from datetime import datetime

class PlatformOptimizer:
    def __init__(self):
        self.platform_specs = {
            "facebook": {
                "character_limit": 63206,
                "optimal_length": 400,
                "hashtag_limit": 30,
                "optimal_hashtags": 3,
                "supports_long_form": True,
                "engagement_features": ["reactions", "comments", "shares"],
                "visual_formats": ["images", "videos", "carousels", "live"]
            },
            "instagram": {
                "character_limit": 2200,
                "optimal_length": 300,
                "hashtag_limit": 30,
                "optimal_hashtags": 15,
                "supports_long_form": False,
                "engagement_features": ["likes", "comments", "shares", "saves"],
                "visual_formats": ["images", "videos", "stories", "reels", "carousels"]
            },
            "linkedin": {
                "character_limit": 3000,
                "optimal_length": 600,
                "hashtag_limit": 20,
                "optimal_hashtags": 5,
                "supports_long_form": True,
                "engagement_features": ["reactions", "comments", "shares"],
                "visual_formats": ["images", "videos", "documents", "carousels"]
            }
        }
    
    def optimize_content(self, content_dict: Dict, platform: str) -> Dict:
        """
        Optimize content for specific platform requirements
        """
        platform = platform.lower()
        specs = self.platform_specs.get(platform, self.platform_specs["facebook"])
        
        optimized = content_dict.copy()
        
        # Optimize main content length
        optimized["content"] = self._optimize_text_length(
            content_dict["content"], specs["character_limit"], specs["optimal_length"]
        )
        
        # Optimize hashtags
        optimized["hashtags"] = self._optimize_hashtags(
            content_dict.get("hashtags", []), specs["hashtag_limit"], specs["optimal_hashtags"]
        )
        
        # Add platform-specific formatting
        optimized["formatted_content"] = self._format_for_platform(
            optimized["content"], optimized["hashtags"], platform
        )
        
        # Add platform-specific call-to-action
        optimized["cta"] = self._get_platform_cta(platform, content_dict.get("audience", "millennials"))
        
        # Add engagement optimization
        optimized["engagement_tips"] = self._get_engagement_tips(platform)
        
        # Add visual content suggestions
        optimized["visual_suggestions"] = self._enhance_visual_suggestions(
            content_dict.get("visual_suggestions", ""), platform
        )
        
        # Add posting time recommendations
        optimized["best_posting_times"] = self._get_posting_times(platform, content_dict.get("audience", "millennials"))
        
        return optimized
    
    def _optimize_text_length(self, text: str, char_limit: int, optimal_length: int) -> str:
        """Optimize text length for platform"""
        if len(text) <= optimal_length:
            return text
        
        if len(text) > char_limit:
            # Hard truncation with ellipsis
            return text[:char_limit-3] + "..."
        
        # Soft optimization - find natural break point near optimal length
        if len(text) > optimal_length * 1.2:  # 20% over optimal
            sentences = text.split('. ')
            optimized_text = ""
            
            for sentence in sentences:
                test_text = optimized_text + sentence + ". "
                if len(test_text) <= optimal_length * 1.1:  # 10% over optimal is okay
                    optimized_text = test_text
                else:
                    break
            
            return optimized_text.strip()
        
        return text
    
    def _optimize_hashtags(self, hashtags: List[str], limit: int, optimal: int) -> List[str]:
        """Optimize hashtag selection and count"""
        if not hashtags:
            return []
        
        # Remove duplicates while preserving order
        unique_hashtags = []
        seen = set()
        for tag in hashtags:
            if tag.lower() not in seen:
                unique_hashtags.append(tag)
                seen.add(tag.lower())
        
        # Prioritize most relevant hashtags (simplified)
        priority_order = [
            "#MortgageRates", "#HomeLoans", "#RealEstate", "#Refinancing",
            "#FirstTimeBuyer", "#Homeownership", "#MortgageExpert", "#HomeBuying"
        ]
        
        prioritized = []
        remaining = []
        
        for tag in unique_hashtags:
            if tag in priority_order:
                prioritized.append(tag)
            else:
                remaining.append(tag)
        
        # Sort prioritized by priority order
        prioritized.sort(key=lambda x: priority_order.index(x) if x in priority_order else len(priority_order))
        
        # Combine and limit to optimal count
        final_hashtags = (prioritized + remaining)[:min(optimal, limit)]
        
        return final_hashtags
    
    def _format_for_platform(self, content: str, hashtags: List[str], platform: str) -> str:
        """Format content with platform-specific styling"""
        formatted = content
        
        if platform == "instagram":
            # Instagram prefers hashtags at the end or in comments
            if hashtags:
                hashtag_string = " ".join(hashtags)
                formatted = f"{content}\n\n{hashtag_string}"
        
        elif platform == "linkedin":
            # LinkedIn prefers professional formatting
            if hashtags:
                hashtag_string = " ".join(hashtags)
                formatted = f"{content}\n\n{hashtag_string}"
        
        elif platform == "facebook":
            # Facebook is more flexible
            if hashtags:
                hashtag_string = " ".join(hashtags)
                formatted = f"{content}\n\n{hashtag_string}"
        
        return formatted
    
    def _get_platform_cta(self, platform: str, audience: str) -> str:
        """Get platform-appropriate call-to-action"""
        cta_map = {
            "facebook": {
                "millennials": "Comment below with your questions or DM me to get started!",
                "gen_x": "Ready to explore your options? Send me a message or give me a call.",
                "baby_boomers": "I'd be happy to discuss your mortgage needs. Please feel free to contact me."
            },
            "instagram": {
                "millennials": "Drop a 🏠 if you're ready to chat about homeownership! DM me anytime.",
                "gen_x": "Questions about rates? Send me a DM or check the link in my bio.",
                "baby_boomers": "Contact me through DM or the link in my bio for a consultation."
            },
            "linkedin": {
                "millennials": "Connect with me to discuss your homeownership journey.",
                "gen_x": "I'd be happy to discuss how current rates affect your financial strategy.",
                "baby_boomers": "I'm here to provide expert guidance. Please don't hesitate to reach out."
            }
        }
        
        return cta_map.get(platform, {}).get(audience, "Contact me to learn more!")
    
    def _get_engagement_tips(self, platform: str) -> List[str]:
        """Get platform-specific engagement optimization tips"""
        tips = {
            "facebook": [
                "Post when your audience is most active (typically 1-3 PM weekdays)",
                "Ask questions to encourage comments",
                "Respond quickly to comments to boost engagement",
                "Use Facebook Live for real-time Q&A sessions",
                "Share behind-the-scenes content to build trust"
            ],
            "instagram": [
                "Use Instagram Stories for daily updates",
                "Post consistently at optimal times (11 AM - 1 PM)",
                "Use relevant hashtags in comments for cleaner look",
                "Engage with your audience's content too",
                "Save important content as Story Highlights"
            ],
            "linkedin": [
                "Post during business hours for maximum reach",
                "Share industry insights and thought leadership",
                "Engage with comments professionally and promptly",
                "Use LinkedIn's publishing platform for longer content",
                "Connect with local real estate professionals"
            ]
        }
        
        return tips.get(platform, [])
    
    def _enhance_visual_suggestions(self, original_suggestion: str, platform: str) -> Dict[str, str]:
        """Enhance visual content suggestions for each platform"""
        
        base_suggestions = {
            "chart_visual": "Professional rate chart with clean, easy-to-read design",
            "infographic": "Key rate information in visually appealing format",
            "quote_card": "Rate quote with professional branding",
            "carousel": "Multi-slide breakdown of rate information and tips"
        }
        
        platform_specific = {
            "facebook": {
                "primary": "Clean, professional chart showing rate trends",
                "secondary": "Carousel post with rate breakdown and tips",
                "video": "Short explainer video about current market conditions"
            },
            "instagram": {
                "primary": "Bright, eye-catching infographic with rate highlights",
                "secondary": "Story series breaking down rate information",
                "video": "Reel explaining what current rates mean for buyers"
            },
            "linkedin": {
                "primary": "Professional data visualization with market analysis",
                "secondary": "Document carousel with detailed market insights",
                "video": "Professional presentation about rate trends"
            }
        }
        
        return platform_specific.get(platform, platform_specific["facebook"])
    
    def _get_posting_times(self, platform: str, audience: str) -> Dict[str, List[str]]:
        """Get optimal posting times for platform and audience"""
        
        times = {
            "facebook": {
                "millennials": ["9-10 AM", "3-4 PM", "7-8 PM"],
                "gen_x": ["6-9 AM", "12-2 PM", "7-9 PM"],
                "baby_boomers": ["10-11 AM", "2-4 PM", "6-8 PM"]
            },
            "instagram": {
                "millennials": ["11 AM-1 PM", "5-7 PM", "7-9 PM"],
                "gen_x": ["8-10 AM", "12-2 PM", "5-7 PM"],
                "baby_boomers": ["10 AM-12 PM", "2-4 PM", "6-7 PM"]
            },
            "linkedin": {
                "millennials": ["8-9 AM", "12-1 PM", "5-6 PM"],
                "gen_x": ["7-9 AM", "12-2 PM", "5-6 PM"],
                "baby_boomers": ["8-10 AM", "11 AM-12 PM", "1-3 PM"]
            }
        }
        
        platform_times = times.get(platform, times["facebook"])
        audience_times = platform_times.get(audience, platform_times["millennials"])
        
        return {
            "weekdays": audience_times,
            "weekends": ["10 AM-12 PM", "2-4 PM"],
            "timezone_note": "Times shown in local timezone. Adjust based on your audience location."
        }
    
    def validate_content(self, content_dict: Dict, platform: str) -> Dict[str, any]:
        """Validate content meets platform requirements"""
        platform = platform.lower()
        specs = self.platform_specs.get(platform, self.platform_specs["facebook"])
        
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "character_count": len(content_dict.get("content", "")),
            "hashtag_count": len(content_dict.get("hashtags", []))
        }
        
        content_length = len(content_dict.get("content", ""))
        hashtag_count = len(content_dict.get("hashtags", []))
        
        # Check character limits
        if content_length > specs["character_limit"]:
            validation_result["errors"].append(
                f"Content exceeds {platform} character limit ({content_length} > {specs['character_limit']})"
            )
            validation_result["is_valid"] = False
        elif content_length > specs["optimal_length"]:
            validation_result["warnings"].append(
                f"Content longer than optimal for {platform} ({content_length} > {specs['optimal_length']})"
            )
        
        # Check hashtag limits
        if hashtag_count > specs["hashtag_limit"]:
            validation_result["errors"].append(
                f"Too many hashtags for {platform} ({hashtag_count} > {specs['hashtag_limit']})"
            )
            validation_result["is_valid"] = False
        elif hashtag_count > specs["optimal_hashtags"]:
            validation_result["warnings"].append(
                f"More hashtags than optimal for {platform} ({hashtag_count} > {specs['optimal_hashtags']})"
            )
        
        return validation_result
    
    def get_platform_best_practices(self, platform: str) -> Dict[str, List[str]]:
        """Get best practices for each platform"""
        
        practices = {
            "facebook": {
                "content": [
                    "Use conversational tone",
                    "Ask questions to encourage engagement",
                    "Share valuable insights, not just promotions",
                    "Include local market information when relevant"
                ],
                "timing": [
                    "Post 1-2 times per day maximum",
                    "Best times are typically 1-3 PM on weekdays",
                    "Avoid posting late at night or very early morning"
                ],
                "engagement": [
                    "Respond to comments within 2-4 hours",
                    "Like and reply to engage the algorithm",
                    "Share user-generated content when appropriate",
                    "Go live occasionally for real-time interaction"
                ]
            },
            "instagram": {
                "content": [
                    "Focus on high-quality visuals",
                    "Use Stories for behind-the-scenes content",
                    "Create branded, consistent visual style",
                    "Mix educational and personal content"
                ],
                "timing": [
                    "Post once daily consistently",
                    "Use Stories multiple times per day",
                    "Best engagement typically 11 AM - 1 PM",
                    "Post Reels in the evening for maximum reach"
                ],
                "engagement": [
                    "Use relevant hashtags in first comment",
                    "Engage with similar accounts in your niche",
                    "Respond to DMs quickly",
                    "Use Instagram's newest features early"
                ]
            },
            "linkedin": {
                "content": [
                    "Share industry expertise and insights",
                    "Write longer-form educational content",
                    "Comment thoughtfully on industry discussions",
                    "Share company news and achievements"
                ],
                "timing": [
                    "Post during business hours",
                    "Tuesday-Thursday typically get best engagement",
                    "Avoid weekends unless sharing personal insights",
                    "Consistency over frequency"
                ],
                "engagement": [
                    "Connect with industry peers and clients",
                    "Participate in relevant group discussions",
                    "Share others' content with thoughtful commentary",
                    "Send personalized connection requests"
                ]
            }
        }
        
        return practices.get(platform.lower(), practices["facebook"])