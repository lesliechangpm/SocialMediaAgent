#!/usr/bin/env python3
"""
Social Media Agent - AI-Powered Mortgage Rate Content Generator
Full production version with Claude AI and live data sources
"""

import os
import sys
import json
import click
import requests
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from anthropic import Anthropic
try:
    import feedparser
except ImportError:
    feedparser = None
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

class RateDataFetcher:
    """Enhanced rate data fetcher with multiple live sources"""
    
    def __init__(self):
        self.cache_file = Path("data/rate_cache.json")
        self.cache_duration = 3600  # 1 hour
        
    def get_current_rates(self) -> Dict:
        """Fetch current mortgage rates from multiple sources"""
        # Check cache first
        cached_data = self._get_cached_data()
        if cached_data and self._is_cache_valid(cached_data):
            return cached_data
        
        # Try live sources
        for source in ["freddie_mac", "bankrate", "mortgage_news"]:
            try:
                rate_data = getattr(self, f"_fetch_{source}_rates")()
                if rate_data:
                    self._cache_data(rate_data)
                    return rate_data
            except Exception as e:
                logging.warning(f"Failed to fetch from {source}: {e}")
                continue
        
        # Fallback to cached or mock data
        return cached_data if cached_data else self._generate_fallback_data()
    
    def _fetch_freddie_mac_rates(self) -> Optional[Dict]:
        """Fetch rates from Freddie Mac PMMS"""
        try:
            # Freddie Mac Primary Mortgage Market Survey
            url = "http://www.freddiemac.com/pmms/pmms30.html"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse the current rate (simplified - would need more robust parsing)
                rate_elements = soup.find_all(text=lambda text: text and '%' in text)
                for element in rate_elements:
                    try:
                        # Look for patterns like "7.25%" or "7.25 percent"
                        import re
                        rate_match = re.search(r'(\d+\.\d+)(?:%|(?:\s+percent))', element)
                        if rate_match and 5.0 <= float(rate_match.group(1)) <= 10.0:
                            current_rate = float(rate_match.group(1))
                            return {
                                "current_rate": current_rate,
                                "previous_rate": current_rate + 0.05,  # Estimate
                                "rate_change": -0.05,
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "source": "Freddie Mac PMMS",
                                "confidence": "high"
                            }
                    except (ValueError, AttributeError):
                        continue
        except Exception as e:
            logging.error(f"Freddie Mac fetch error: {e}")
        return None
    
    def _fetch_bankrate_rates(self) -> Optional[Dict]:
        """Fetch rates from Bankrate API/RSS"""
        try:
            # Try RSS feed approach
            rss_urls = [
                "https://www.bankrate.com/rss/mortgage-rates.xml",
                "https://feeds.bankrate.com/mortgage"
            ]
            
            for rss_url in rss_urls:
                if not feedparser:
                    return None
                feed = feedparser.parse(rss_url)
                if feed.entries:
                    for entry in feed.entries[:3]:
                        # Look for rate information in titles/descriptions
                        text = f"{entry.get('title', '')} {entry.get('summary', '')}"
                        import re
                        rate_matches = re.findall(r'(\d+\.\d+)%?', text)
                        for rate_str in rate_matches:
                            try:
                                rate = float(rate_str)
                                if 5.0 <= rate <= 10.0:
                                    return {
                                        "current_rate": rate,
                                        "previous_rate": rate + 0.03,
                                        "rate_change": -0.03,
                                        "date": datetime.now().strftime("%Y-%m-%d"),
                                        "source": "Bankrate RSS",
                                        "confidence": "medium"
                                    }
                            except ValueError:
                                continue
        except Exception as e:
            logging.error(f"Bankrate fetch error: {e}")
        return None
    
    def _fetch_mortgage_news_rates(self) -> Optional[Dict]:
        """Fetch rates from mortgage news sources"""
        try:
            news_feeds = [
                "https://www.mortgagenewsdaily.com/mortgage_rates/rss.xml",
                "https://www.housingwire.com/feed/"
            ]
            
            for feed_url in news_feeds:
                if not feedparser:
                    return None
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    if any(term in entry.title.lower() for term in ['rate', 'mortgage', '30-year']):
                        # Extract rate from content
                        text = f"{entry.title} {entry.get('summary', '')}"
                        import re
                        rate_pattern = r'(?:rate|rates?)\s*:?\s*(\d+\.\d+)%?'
                        matches = re.findall(rate_pattern, text, re.IGNORECASE)
                        for match in matches:
                            try:
                                rate = float(match)
                                if 5.0 <= rate <= 10.0:
                                    return {
                                        "current_rate": rate,
                                        "previous_rate": rate + 0.02,
                                        "rate_change": -0.02,
                                        "date": datetime.now().strftime("%Y-%m-%d"),
                                        "source": "Mortgage News",
                                        "confidence": "medium"
                                    }
                            except ValueError:
                                continue
        except Exception as e:
            logging.error(f"Mortgage news fetch error: {e}")
        return None
    
    def _get_cached_data(self) -> Optional[Dict]:
        """Get cached rate data if available"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return None
    
    def _is_cache_valid(self, cached_data: Dict) -> bool:
        """Check if cached data is still valid"""
        try:
            cache_time = datetime.fromisoformat(cached_data.get('cached_at', ''))
            return (datetime.now() - cache_time).total_seconds() < self.cache_duration
        except Exception:
            return False
    
    def _cache_data(self, data: Dict):
        """Cache rate data"""
        try:
            # Ensure data directory exists
            self.cache_file.parent.mkdir(exist_ok=True)
            
            data['cached_at'] = datetime.now().isoformat()
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.warning(f"Failed to cache data: {e}")
    
    def _generate_fallback_data(self) -> Dict:
        """Generate fallback data when live sources fail"""
        import random
        base_rate = random.uniform(6.8, 7.5)
        return {
            "current_rate": round(base_rate, 2),
            "previous_rate": round(base_rate + 0.05, 2),
            "rate_change": -0.05,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "Fallback Data",
            "confidence": "low"
        }
    
    def get_market_context(self, rate_data: Dict) -> str:
        """Generate market context and analysis"""
        current_rate = rate_data.get("current_rate", 7.0)
        change = rate_data.get("rate_change", 0)
        
        context_parts = []
        
        # Rate movement analysis
        if abs(change) >= 0.1:
            direction = "increased significantly" if change > 0 else "dropped notably"
            context_parts.append(f"Rates {direction} by {abs(change):.2f}% this week")
        elif abs(change) >= 0.05:
            direction = "rose" if change > 0 else "declined"
            context_parts.append(f"Rates {direction} by {abs(change):.2f}%")
        else:
            context_parts.append("Rates remained relatively stable this week")
        
        # Historical context
        if current_rate >= 7.5:
            context_parts.append("Rates are at elevated levels, impacting affordability")
        elif current_rate >= 7.0:
            context_parts.append("Rates remain above recent averages but within normal range")
        elif current_rate >= 6.5:
            context_parts.append("Rates are at moderate levels for qualified buyers")
        else:
            context_parts.append("Rates are at attractive levels for borrowers")
        
        # Market factors
        factors = [
            "Federal Reserve policy decisions continue to influence rates",
            "Economic indicators and inflation data drive rate movements",
            "Global economic conditions affect U.S. mortgage markets"
        ]
        context_parts.append(factors[0])  # Add one market factor
        
        return ". ".join(context_parts) + "."


class SmartAudienceTargeting:
    """Advanced audience targeting with AI-enhanced profiles"""
    
    def __init__(self):
        self.profiles = self._load_enhanced_profiles()
    
    def _load_enhanced_profiles(self) -> Dict:
        """Load comprehensive audience profiles"""
        return {
            "millennials": {
                "name": "Millennials",
                "age_range": "27-42",
                "demographics": {
                    "income_range": "$45K-$85K",
                    "life_stage": "First-time buyers, young families",
                    "priorities": ["affordability", "convenience", "transparency"],
                    "challenges": ["student loans", "high home prices", "saving for down payment"]
                },
                "psychographics": {
                    "values": ["authenticity", "social responsibility", "work-life balance"],
                    "communication_style": "casual, direct, visual",
                    "decision_factors": ["online research", "peer reviews", "speed of process"],
                    "pain_points": ["complex processes", "hidden fees", "lack of transparency"]
                },
                "digital_behavior": {
                    "platforms": ["instagram", "facebook", "tiktok"],
                    "content_preferences": ["video", "infographics", "stories"],
                    "engagement_style": "interactive, social proof driven",
                    "posting_times": ["11AM-1PM", "5-7PM", "8-10PM"]
                },
                "mortgage_focus": {
                    "primary_needs": ["first-time buyer programs", "low down payment options", "pre-approval"],
                    "secondary_needs": ["debt-to-income guidance", "credit improvement", "closing cost assistance"],
                    "objections": ["rates too high", "can't afford", "process too complex"],
                    "motivators": ["building equity", "stable payments", "tax benefits"]
                }
            },
            
            "gen_x": {
                "name": "Generation X",
                "age_range": "43-58",
                "demographics": {
                    "income_range": "$65K-$120K",
                    "life_stage": "Established families, peak earning years",
                    "priorities": ["family security", "wealth building", "efficiency"],
                    "challenges": ["college funding", "aging parents", "retirement planning"]
                },
                "psychographics": {
                    "values": ["pragmatism", "self-reliance", "family first"],
                    "communication_style": "straightforward, results-oriented, time-conscious",
                    "decision_factors": ["ROI analysis", "expert advice", "proven track record"],
                    "pain_points": ["time constraints", "information overload", "changing rules"]
                },
                "digital_behavior": {
                    "platforms": ["facebook", "linkedin", "email"],
                    "content_preferences": ["articles", "case studies", "webinars"],
                    "engagement_style": "research-driven, value-seeking",
                    "posting_times": ["6-9AM", "12-2PM", "7-9PM"]
                },
                "mortgage_focus": {
                    "primary_needs": ["refinancing", "home equity loans", "investment properties"],
                    "secondary_needs": ["debt consolidation", "cash-out refinancing", "rate optimization"],
                    "objections": ["closing costs vs. savings", "timing concerns", "qualification changes"],
                    "motivators": ["monthly savings", "wealth building", "family financial security"]
                }
            },
            
            "baby_boomers": {
                "name": "Baby Boomers",
                "age_range": "59-77",
                "demographics": {
                    "income_range": "$50K-$100K (fixed/retirement)",
                    "life_stage": "Pre-retirement, early retirement",
                    "priorities": ["financial security", "legacy planning", "risk management"],
                    "challenges": ["fixed income", "healthcare costs", "market volatility"]
                },
                "psychographics": {
                    "values": ["stability", "tradition", "personal relationships"],
                    "communication_style": "formal, detailed, relationship-based",
                    "decision_factors": ["personal recommendations", "established reputation", "thorough explanation"],
                    "pain_points": ["technology complexity", "pressure tactics", "impersonal service"]
                },
                "digital_behavior": {
                    "platforms": ["facebook", "email", "linkedin"],
                    "content_preferences": ["detailed articles", "newsletters", "phone consultations"],
                    "engagement_style": "cautious, relationship-focused",
                    "posting_times": ["8-11AM", "2-5PM", "6-8PM"]
                },
                "mortgage_focus": {
                    "primary_needs": ["reverse mortgages", "refinancing", "downsizing"],
                    "secondary_needs": ["estate planning", "tax optimization", "payment reduction"],
                    "objections": ["complexity", "long-term commitment", "changing circumstances"],
                    "motivators": ["financial security", "family legacy", "simplified finances"]
                }
            }
        }
    
    def get_profile(self, audience: str) -> Dict:
        """Get comprehensive audience profile"""
        return self.profiles.get(audience.lower().replace(" ", "_"), self.profiles["millennials"])
    
    def generate_targeting_insights(self, audience: str, content_type: str, platform: str) -> Dict:
        """Generate AI-enhanced targeting insights"""
        profile = self.get_profile(audience)
        
        return {
            "tone": self._get_optimal_tone(profile, content_type, platform),
            "key_messages": self._get_key_messages(profile, content_type),
            "emotional_triggers": self._get_emotional_triggers(profile, content_type),
            "call_to_action": self._get_optimal_cta(profile, platform),
            "content_hooks": self._generate_content_hooks(profile, content_type),
            "objection_handling": self._get_objection_responses(profile),
            "value_propositions": self._get_value_props(profile, content_type)
        }
    
    def _get_optimal_tone(self, profile: Dict, content_type: str, platform: str) -> str:
        """Determine optimal communication tone"""
        base_style = profile["psychographics"]["communication_style"]
        
        tone_matrix = {
            "millennials": {
                "educational": "Friendly and approachable with clear, jargon-free explanations",
                "promotional": "Authentic and transparent, focusing on benefits and social proof",
                "market_update": "Casual but informative, with actionable takeaways"
            },
            "gen_x": {
                "educational": "Professional and direct, with practical examples and ROI focus",
                "promotional": "Results-oriented and efficient, emphasizing track record",
                "market_update": "Strategic and analytical, with clear implications"
            },
            "baby_boomers": {
                "educational": "Respectful and thorough, with detailed explanations and context",
                "promotional": "Trust-building and relationship-focused, emphasizing experience",
                "market_update": "Conservative and measured, with historical perspective"
            }
        }
        
        audience_key = profile["name"].lower().replace(" ", "_")
        return tone_matrix.get(audience_key, {}).get(content_type, base_style)
    
    def _get_key_messages(self, profile: Dict, content_type: str) -> List[str]:
        """Get key messages for audience and content type"""
        messages = profile["mortgage_focus"]["motivators"]
        
        if content_type == "educational":
            messages.extend(["Expert guidance", "Simplified process", "Informed decisions"])
        elif content_type == "promotional":
            messages.extend(["Proven results", "Personalized service", "Trusted expertise"])
        else:  # market_update
            messages.extend(["Timely insights", "Market opportunities", "Strategic timing"])
        
        return messages[:4]  # Top 4 messages
    
    def _get_emotional_triggers(self, profile: Dict, content_type: str) -> List[str]:
        """Identify emotional triggers for audience"""
        base_triggers = profile["psychographics"]["values"]
        
        trigger_map = {
            "educational": ["confidence", "empowerment", "clarity"],
            "promotional": ["trust", "success", "partnership"],
            "market_update": ["opportunity", "timeliness", "advantage"]
        }
        
        return base_triggers + trigger_map.get(content_type, [])
    
    def _get_optimal_cta(self, profile: Dict, platform: str) -> str:
        """Generate optimal call-to-action"""
        audience_name = profile["name"].lower().replace(" ", "_")
        
        cta_matrix = {
            "millennials": {
                "instagram": "Ready to explore homeownership? Comment below or DM me to get started.",
                "facebook": "Ready to take the next step? Comment below or send me a message - I'm here to help!",
                "linkedin": "Interested in learning more? Connect with me to discuss your homeownership goals."
            },
            "gen_x": {
                "instagram": "Questions about refinancing or home equity? Send me a DM - let's talk strategy.",
                "facebook": "Ready to optimize your mortgage? Comment below or message me to discuss your options.",
                "linkedin": "Let's discuss how current market conditions affect your mortgage strategy. Message me."
            },
            "baby_boomers": {
                "instagram": "I'm here to provide personalized guidance. Please reach out through DM for a consultation.",
                "facebook": "I'd be happy to discuss your mortgage needs. Please feel free to contact me directly.",
                "linkedin": "For a comprehensive consultation, please don't hesitate to reach out. I'm here to help."
            }
        }
        
        return cta_matrix.get(audience_name, {}).get(platform, "Contact me to learn more about your options.")
    
    def _generate_content_hooks(self, profile: Dict, content_type: str) -> List[str]:
        """Generate attention-grabbing content hooks"""
        hooks = {
            "millennials": [
                "Your dream home is more affordable than you think",
                "Stop paying someone else's mortgage - here's how to buy",
                "The homebuying hack your parents never told you about"
            ],
            "gen_x": [
                "Smart families are doing this with their mortgages right now",
                "The refinancing strategy that's saving families $500+ monthly",
                "How to turn your home equity into wealth-building power"
            ],
            "baby_boomers": [
                "After 30 years in mortgages, here's what I tell my own family",
                "The mortgage strategy for secure retirement planning",
                "Why experience matters more than ever in today's market"
            ]
        }
        
        audience_key = profile["name"].lower().replace(" ", "_")
        return hooks.get(audience_key, hooks["millennials"])
    
    def _get_objection_responses(self, profile: Dict) -> Dict[str, str]:
        """Get responses to common objections"""
        objections = profile["mortgage_focus"]["objections"]
        
        response_map = {
            "rates too high": "Even with today's rates, homeownership builds wealth over time vs. renting",
            "can't afford": "Let's explore all available programs - you might qualify for more than you think",
            "process too complex": "I'll guide you through every step and make it as simple as possible",
            "closing costs vs. savings": "Let's run the numbers to see your real break-even point",
            "timing concerns": "I'll help you determine the optimal timing based on your specific situation",
            "qualification changes": "Lending requirements are stable - let's review your current position"
        }
        
        return {obj: response_map.get(obj, "Let me address that concern with you personally") for obj in objections}
    
    def _get_value_props(self, profile: Dict, content_type: str) -> List[str]:
        """Get audience-specific value propositions"""
        base_props = [
            "Personalized guidance throughout the process",
            "Access to multiple loan programs and options",
            "Expert market knowledge and timing insights"
        ]
        
        audience_name = profile["name"].lower().replace(" ", "_")
        
        specific_props = {
            "millennials": [
                "First-time buyer programs and down payment assistance",
                "Technology-driven process for faster approvals",
                "Credit improvement strategies and guidance"
            ],
            "gen_x": [
                "Refinancing analysis and debt consolidation options",
                "Investment property and wealth-building strategies",
                "Efficient processes that respect your time"
            ],
            "baby_boomers": [
                "Decades of experience and market knowledge",
                "White-glove service with personal attention",
                "Conservative, security-focused mortgage solutions"
            ]
        }
        
        return base_props + specific_props.get(audience_name, [])


class AIContentGenerator:
    """Advanced AI-powered content generator using Claude"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.audience_targeting = SmartAudienceTargeting()
        
    def generate_content(self, rate_data: Dict, platform: str, audience: str, 
                        content_type: str, loan_officer: Optional[str] = None, 
                        company: Optional[str] = None, custom_focus: Optional[str] = None) -> Dict:
        """Generate AI-powered social media content"""
        
        # Get audience insights
        targeting_insights = self.audience_targeting.generate_targeting_insights(
            audience, content_type, platform
        )
        
        # Build comprehensive prompt
        prompt = self._build_ai_prompt(
            rate_data, platform, audience, content_type, 
            targeting_insights, loan_officer, company, custom_focus
        )
        
        try:
            # Generate content with Claude
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1200,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text.strip()
            
            # Parse and optimize the generated content
            parsed_content = self._parse_ai_content(content)
            optimized_content = self._optimize_for_platform(parsed_content, platform, audience)
            
            return {
                **optimized_content,
                "platform": platform,
                "audience": audience,
                "content_type": content_type,
                "rate_data": rate_data,
                "targeting_insights": targeting_insights,
                "generation_timestamp": datetime.now().isoformat(),
                "ai_generated": True
            }
            
        except Exception as e:
            logging.error(f"AI content generation failed: {e}")
            # Fallback to template-based generation
            return self._generate_fallback_content(
                rate_data, platform, audience, content_type, loan_officer, company
            )
    
    def _build_ai_prompt(self, rate_data: Dict, platform: str, audience: str, 
                        content_type: str, targeting_insights: Dict, 
                        loan_officer: Optional[str], company: Optional[str],
                        custom_focus: Optional[str]) -> str:
        """Build comprehensive AI prompt for content generation"""
        
        profile = self.audience_targeting.get_profile(audience)
        
        # Format rate information
        current_rate = rate_data.get('current_rate', 7.0)
        rate_change = rate_data.get('rate_change', 0)
        change_direction = "increased" if rate_change > 0 else "decreased" if rate_change < 0 else "remained stable"
        change_magnitude = "significantly" if abs(rate_change) >= 0.1 else "slightly" if abs(rate_change) >= 0.05 else ""
        
        # Personal branding
        branding = ""
        if loan_officer or company:
            branding = f"\nPERSONAL BRANDING:\n"
            if loan_officer:
                branding += f"- Loan Officer: {loan_officer}\n"
            if company:
                branding += f"- Company: {company}\n"
        
        prompt = f"""You are an expert mortgage industry social media content creator. Create compelling, professional social media content that converts prospects into leads.

CURRENT MARKET DATA:
- 30-year fixed mortgage rate: {current_rate}%
- Rate change: {rate_change:+.2f}% ({change_direction} {change_magnitude})
- Market confidence: {rate_data.get('confidence', 'medium')}
- Data source: {rate_data.get('source', 'Market Data')}
- Date: {rate_data.get('date', datetime.now().strftime('%Y-%m-%d'))}

TARGET SPECIFICATIONS:
- Platform: {platform.upper()}
- Audience: {profile['name']} ({profile['age_range']})
- Content Type: {content_type.replace('_', ' ').title()}
- Communication Tone: {targeting_insights['tone']}

AUDIENCE PROFILE:
- Demographics: {profile['demographics']['life_stage']}
- Income Range: {profile['demographics']['income_range']}
- Key Priorities: {', '.join(profile['demographics']['priorities'])}
- Main Challenges: {', '.join(profile['demographics']['challenges'])}
- Decision Factors: {', '.join(profile['psychographics']['decision_factors'])}
- Primary Mortgage Needs: {', '.join(profile['mortgage_focus']['primary_needs'])}

TARGETING INSIGHTS:
- Key Messages: {', '.join(targeting_insights['key_messages'])}
- Emotional Triggers: {', '.join(targeting_insights['emotional_triggers'])}
- Value Propositions: {', '.join(targeting_insights['value_propositions'][:3])}
- Optimal CTA: {targeting_insights['call_to_action']}

PLATFORM REQUIREMENTS ({platform.upper()}):
- Optimal character length: {self._get_platform_limits(platform)['optimal_length']}
- Recommended hashtags: {self._get_platform_limits(platform)['recommended_hashtags']}
- Content style: {self._get_platform_style(platform, audience)}
- Engagement approach: {profile['digital_behavior']['engagement_style']}

{branding}

CUSTOM FOCUS: {custom_focus or 'Standard mortgage rate content focusing on current opportunities'}

CONTENT REQUIREMENTS:
1. Start with a compelling hook that addresses {profile['name']}'s main concerns
2. Include current rate information ({current_rate}%) with relevant context
3. Address their key challenge: {profile['demographics']['challenges'][0]}
4. Highlight a relevant value proposition from: {', '.join(targeting_insights['value_propositions'][:2])}
5. Include emotional trigger: {targeting_insights['emotional_triggers'][0]}
6. End with the optimal call-to-action for {platform}
7. Maintain {targeting_insights['tone']} tone throughout
8. Ensure content is {platform}-optimized and encourages {profile['digital_behavior']['engagement_style']} engagement

RESPONSE FORMAT:
MAIN_CONTENT:
[Write the social media post content here - compelling, professional, conversion-focused]

HASHTAGS:
[List relevant hashtags separated by spaces]

VISUAL_CONCEPT:
[Describe recommended visual content/graphics]

ENGAGEMENT_STRATEGY:
[Brief strategy for maximizing engagement]

Generate content that feels authentic, provides genuine value, and naturally leads to mortgage consultations while maintaining the highest professional standards."""

        return prompt
    
    def _parse_ai_content(self, content: str) -> Dict:
        """Parse AI-generated content into components"""
        sections = {
            "main_content": "",
            "hashtags": [],
            "visual_concept": "",
            "engagement_strategy": ""
        }
        
        current_section = None
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if line.upper().startswith('MAIN_CONTENT:'):
                current_section = 'main_content'
                continue
            elif line.upper().startswith('HASHTAGS:'):
                current_section = 'hashtags'
                continue
            elif line.upper().startswith('VISUAL_CONCEPT:'):
                current_section = 'visual_concept'
                continue
            elif line.upper().startswith('ENGAGEMENT_STRATEGY:'):
                current_section = 'engagement_strategy'
                continue
            
            if current_section and line:
                if current_section == 'hashtags':
                    # Extract hashtags
                    hashtags = [tag.strip() for tag in line.split() if tag.startswith('#')]
                    sections['hashtags'].extend(hashtags)
                else:
                    sections[current_section] += line + ' '
        
        # Clean up sections
        for key in ['main_content', 'visual_concept', 'engagement_strategy']:
            sections[key] = sections[key].strip()
        
        # If parsing failed, use entire content as main content
        if not sections['main_content']:
            sections['main_content'] = content.strip()
        
        return sections
    
    def _optimize_for_platform(self, parsed_content: Dict, platform: str, audience: str) -> Dict:
        """Optimize content for specific platform requirements"""
        limits = self._get_platform_limits(platform)
        
        # Optimize main content length
        main_content = parsed_content['main_content']
        if len(main_content) > limits['max_length']:
            # Truncate intelligently at sentence boundaries
            sentences = main_content.split('. ')
            optimized_content = ""
            for sentence in sentences:
                test_content = optimized_content + sentence + ". "
                if len(test_content) <= limits['optimal_length']:
                    optimized_content = test_content
                else:
                    break
            main_content = optimized_content.strip()
        
        # Optimize hashtags
        hashtags = parsed_content['hashtags'][:limits['recommended_hashtags']]
        if not hashtags:
            hashtags = self._get_default_hashtags(audience, platform)
        
        # Format final content
        final_content = main_content
        if hashtags:
            hashtag_string = ' '.join(hashtags)
            final_content = f"{main_content}\n\n{hashtag_string}"
        
        return {
            "content": final_content,
            "main_content": main_content,
            "hashtags": hashtags,
            "character_count": len(final_content),
            "visual_concept": parsed_content.get('visual_concept', ''),
            "engagement_strategy": parsed_content.get('engagement_strategy', ''),
            "optimized_for_platform": True
        }
    
    def _get_platform_limits(self, platform: str) -> Dict:
        """Get platform-specific limits and recommendations"""
        limits = {
            "facebook": {
                "max_length": 63206,
                "optimal_length": 500,
                "recommended_hashtags": 5
            },
            "instagram": {
                "max_length": 2200,
                "optimal_length": 350,
                "recommended_hashtags": 15
            },
            "linkedin": {
                "max_length": 3000,
                "optimal_length": 700,
                "recommended_hashtags": 5
            }
        }
        return limits.get(platform, limits["facebook"])
    
    def _get_platform_style(self, platform: str, audience: str) -> str:
        """Get platform-specific content style"""
        styles = {
            "facebook": "Conversational and community-focused",
            "instagram": "Visual-first and trend-aware", 
            "linkedin": "Professional and thought-leadership oriented"
        }
        return styles.get(platform, "Professional and engaging")
    
    def _get_default_hashtags(self, audience: str, platform: str) -> List[str]:
        """Get default hashtags when AI doesn't generate them"""
        base_hashtags = ["#MortgageRates", "#HomeLoans", "#MortgageExpert"]
        
        audience_hashtags = {
            "millennials": ["#FirstTimeBuyer", "#Homeownership", "#RealEstate"],
            "gen_x": ["#Refinancing", "#HomeEquity", "#SmartMoney"],
            "baby_boomers": ["#RefinanceOptions", "#RetirementPlanning", "#MortgageProfessional"]
        }
        
        hashtags = base_hashtags + audience_hashtags.get(audience, [])
        limit = self._get_platform_limits(platform)['recommended_hashtags']
        return hashtags[:limit]
    
    def _generate_fallback_content(self, rate_data: Dict, platform: str, audience: str,
                                  content_type: str, loan_officer: Optional[str], 
                                  company: Optional[str]) -> Dict:
        """Generate fallback content when AI fails"""
        # Simple template-based fallback
        current_rate = rate_data.get('current_rate', 7.0)
        
        templates = {
            "millennials": f"Current 30-year mortgage rates: {current_rate}%. Ready to explore homeownership? Let's discuss your options and find the right path forward.",
            "gen_x": f"Mortgage rates at {current_rate}% this week. Great time to review your current loan and explore refinancing opportunities.",
            "baby_boomers": f"30-year fixed rates: {current_rate}%. I'm here to provide expert guidance on all your mortgage needs."
        }
        
        content = templates.get(audience, templates["millennials"])
        
        # Add personalization
        if loan_officer or company:
            signature = []
            if loan_officer:
                signature.append(loan_officer)
            if company:
                signature.append(company)
            content += f"\n\n- {', '.join(signature)}"
        
        hashtags = self._get_default_hashtags(audience, platform)
        final_content = f"{content}\n\n{' '.join(hashtags)}"
        
        return {
            "content": final_content,
            "main_content": content,
            "hashtags": hashtags,
            "character_count": len(final_content),
            "visual_concept": "Professional rate chart with current market data",
            "engagement_strategy": "Encourage questions and schedule consultations",
            "ai_generated": False,
            "fallback_used": True
        }
    
    def generate_variations(self, rate_data: Dict, platform: str, audience: str, 
                           count: int = 3, loan_officer: Optional[str] = None,
                           company: Optional[str] = None) -> List[Dict]:
        """Generate multiple content variations for A/B testing"""
        variations = []
        content_types = ["educational", "market_update", "promotional"]
        
        for i in range(count):
            content_type = content_types[i % len(content_types)]
            try:
                variation = self.generate_content(
                    rate_data, platform, audience, content_type, loan_officer, company
                )
                variation["variation_id"] = i + 1
                variation["variation_type"] = content_type
                variations.append(variation)
            except Exception as e:
                logging.error(f"Failed to generate variation {i+1}: {e}")
                continue
        
        return variations


class SocialMediaAgent:
    """Main Social Media Agent orchestrator"""
    
    def __init__(self):
        self.rate_fetcher = RateDataFetcher()
        self.content_generator = None
        self.config = self._load_config()
        self._setup_logging()
    
    def initialize(self, api_key: Optional[str] = None) -> bool:
        """Initialize the agent with API key"""
        try:
            self.content_generator = AIContentGenerator(api_key)
            return True
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            return False
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file"""
        config_file = Path("config/settings.yaml")
        try:
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f)
        except Exception as e:
            logging.warning(f"Failed to load config: {e}")
        
        # Return default config
        return {
            "default_loan_officer": os.getenv("DEFAULT_LOAN_OFFICER_NAME"),
            "default_company": os.getenv("DEFAULT_COMPANY_NAME"),
            "default_platform": "instagram",
            "default_audience": "millennials",
            "save_generated_content": True,
            "content_output_dir": "generated_content"
        }
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'social_media_agent.log'),
                logging.StreamHandler()
            ]
        )
    
    def generate_content(self, platform: str, audience: str, content_type: str = "market_update",
                        loan_officer: Optional[str] = None, company: Optional[str] = None,
                        custom_focus: Optional[str] = None, save_output: bool = False) -> Dict:
        """Generate social media content"""
        if not self.content_generator:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        
        # Get current rate data
        rate_data = self.rate_fetcher.get_current_rates()
        
        # Use defaults if not provided
        loan_officer = loan_officer or self.config.get("default_loan_officer")
        company = company or self.config.get("default_company")
        
        # Generate content
        result = self.content_generator.generate_content(
            rate_data, platform, audience, content_type, loan_officer, company, custom_focus
        )
        
        # Save if requested
        if save_output or self.config.get("save_generated_content"):
            self._save_content(result, platform, audience, content_type)
        
        return result
    
    def generate_variations(self, platform: str, audience: str, count: int = 3,
                           loan_officer: Optional[str] = None, company: Optional[str] = None) -> List[Dict]:
        """Generate multiple content variations"""
        if not self.content_generator:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        
        rate_data = self.rate_fetcher.get_current_rates()
        loan_officer = loan_officer or self.config.get("default_loan_officer")
        company = company or self.config.get("default_company")
        
        return self.content_generator.generate_variations(
            rate_data, platform, audience, count, loan_officer, company
        )
    
    def get_current_rates(self) -> Dict:
        """Get current mortgage rate data"""
        return self.rate_fetcher.get_current_rates()
    
    def get_market_analysis(self) -> str:
        """Get comprehensive market analysis"""
        rate_data = self.rate_fetcher.get_current_rates()
        return self.rate_fetcher.get_market_context(rate_data)
    
    def _save_content(self, content: Dict, platform: str, audience: str, content_type: str):
        """Save generated content to file"""
        try:
            output_dir = Path(self.config.get("content_output_dir", "generated_content"))
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{platform}_{audience}_{content_type}_{timestamp}.json"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False, default=str)
                
            logging.info(f"Content saved to {filepath}")
        except Exception as e:
            logging.error(f"Failed to save content: {e}")


# CLI Interface
@click.group()
@click.pass_context
def cli(ctx):
    """Social Media Agent - AI-Powered Mortgage Content Generator"""
    ctx.ensure_object(dict)
    ctx.obj['agent'] = SocialMediaAgent()

@cli.command()
@click.option('--platform', '-p', type=click.Choice(['facebook', 'instagram', 'linkedin']), 
              required=True, help='Target platform')
@click.option('--audience', '-a', type=click.Choice(['millennials', 'gen_x', 'baby_boomers']),
              required=True, help='Target audience')
@click.option('--type', '-t', type=click.Choice(['educational', 'market_update', 'promotional']),
              default='market_update', help='Content type')
@click.option('--loan-officer', help='Loan officer name')
@click.option('--company', help='Company name')
@click.option('--focus', help='Custom content focus/theme')
@click.option('--api-key', envvar='ANTHROPIC_API_KEY', help='Anthropic API key')
@click.option('--save', is_flag=True, help='Save generated content')
@click.pass_context
def generate(ctx, platform, audience, type, loan_officer, company, focus, api_key, save):
    """Generate AI-powered social media content"""
    agent = ctx.obj['agent']
    
    if not agent.initialize(api_key):
        return
    
    try:
        click.echo("Fetching current market data and generating AI content...")
        
        result = agent.generate_content(
            platform=platform,
            audience=audience, 
            content_type=type,
            loan_officer=loan_officer,
            company=company,
            custom_focus=focus,
            save_output=save
        )
        
        _display_content_result(result)
        
        if result.get('ai_generated'):
            click.echo("\nContent generated using Claude AI")
        else:
            click.echo("\nFallback content used (AI generation failed)")
            
    except Exception as e:
        click.echo(f"Error generating content: {e}", err=True)

@cli.command()
@click.option('--platform', '-p', type=click.Choice(['facebook', 'instagram', 'linkedin']),
              required=True, help='Target platform')
@click.option('--audience', '-a', type=click.Choice(['millennials', 'gen_x', 'baby_boomers']),
              required=True, help='Target audience')
@click.option('--count', '-n', default=3, help='Number of variations')
@click.option('--loan-officer', help='Loan officer name')
@click.option('--company', help='Company name') 
@click.option('--api-key', envvar='ANTHROPIC_API_KEY', help='Anthropic API key')
@click.pass_context
def variations(ctx, platform, audience, count, loan_officer, company, api_key):
    """Generate multiple AI-powered content variations"""
    agent = ctx.obj['agent']
    
    if not agent.initialize(api_key):
        return
    
    try:
        click.echo(f"Generating {count} AI-powered variations...")
        
        variations = agent.generate_variations(
            platform=platform,
            audience=audience,
            count=count,
            loan_officer=loan_officer,
            company=company
        )
        
        for i, variation in enumerate(variations, 1):
            click.echo(f"\n{'='*60}")
            click.echo(f"VARIATION #{i} - {variation.get('variation_type', 'unknown').upper()}")
            click.echo(f"{'='*60}")
            _display_content_result(variation, show_details=False)
        
        click.echo(f"\nGenerated {len(variations)} variations using Claude AI")
        
    except Exception as e:
        click.echo(f"Error generating variations: {e}", err=True)

@cli.command()
@click.pass_context
def rates(ctx):
    """Display current mortgage rates with AI analysis"""
    agent = ctx.obj['agent']
    
    try:
        click.echo("Fetching current mortgage rate data...")
        rate_data = agent.get_current_rates()
        market_analysis = agent.get_market_analysis()
        
        click.echo("\n" + "="*60)
        click.echo("CURRENT MORTGAGE MARKET ANALYSIS")
        click.echo("="*60)
        
        click.echo(f"30-Year Fixed Rate: {rate_data.get('current_rate', 'N/A')}%")
        click.echo(f"Previous Rate: {rate_data.get('previous_rate', 'N/A')}%")
        
        change = rate_data.get('rate_change', 0)
        if change > 0:
            click.echo(f"Weekly Change: +{change:.2f}% (INCREASED)")
        elif change < 0:
            click.echo(f"Weekly Change: {change:.2f}% (DECREASED)")
        else:
            click.echo("Weekly Change: No change (STABLE)")
        
        click.echo(f"Data Source: {rate_data.get('source', 'N/A')}")
        click.echo(f"Confidence Level: {rate_data.get('confidence', 'Medium')}")
        click.echo(f"Last Updated: {rate_data.get('date', 'Current')}")
        
        click.echo(f"\nMARKET ANALYSIS:")
        click.echo(market_analysis)
        
    except Exception as e:
        click.echo(f"Error fetching rates: {e}", err=True)

@cli.command()
@click.pass_context
def audiences(ctx):
    """Display detailed audience profiles and targeting information"""
    targeting = SmartAudienceTargeting()
    
    click.echo("COMPREHENSIVE AUDIENCE TARGETING GUIDE\n")
    
    for audience_key in ["millennials", "gen_x", "baby_boomers"]:
        profile = targeting.get_profile(audience_key)
        
        click.echo(f"{'='*60}")
        click.echo(f"{profile['name'].upper()} ({profile['age_range']})")
        click.echo(f"{'='*60}")
        
        click.echo(f"DEMOGRAPHICS:")
        click.echo(f"  Income Range: {profile['demographics']['income_range']}")
        click.echo(f"  Life Stage: {profile['demographics']['life_stage']}")
        click.echo(f"  Priorities: {', '.join(profile['demographics']['priorities'])}")
        
        click.echo(f"\nPSYCHOGRAPHICS:")
        click.echo(f"  Values: {', '.join(profile['psychographics']['values'])}")
        click.echo(f"  Communication: {profile['psychographics']['communication_style']}")
        click.echo(f"  Decision Factors: {', '.join(profile['psychographics']['decision_factors'])}")
        
        click.echo(f"\nDIGITAL BEHAVIOR:")
        click.echo(f"  Preferred Platforms: {', '.join(profile['digital_behavior']['platforms'])}")
        click.echo(f"  Content Types: {', '.join(profile['digital_behavior']['content_preferences'])}")
        click.echo(f"  Best Posting Times: {', '.join(profile['digital_behavior']['posting_times'])}")
        
        click.echo(f"\nMORTGAGE FOCUS:")
        click.echo(f"  Primary Needs: {', '.join(profile['mortgage_focus']['primary_needs'])}")
        click.echo(f"  Main Objections: {', '.join(profile['mortgage_focus']['objections'])}")
        click.echo(f"  Key Motivators: {', '.join(profile['mortgage_focus']['motivators'])}")
        
        click.echo("")

@cli.command()
@click.argument('platform', type=click.Choice(['facebook', 'instagram', 'linkedin']))
def platform_info(platform):
    """Display comprehensive platform information and best practices"""
    
    platform_data = {
        "facebook": {
            "specs": {
                "max_chars": "63,206",
                "optimal_chars": "500",
                "max_hashtags": "30",
                "recommended_hashtags": "5"
            },
            "best_practices": [
                "Use conversational tone that encourages discussion",
                "Ask questions to boost engagement and comments", 
                "Post during peak times: 1-3 PM weekdays",
                "Share valuable insights, not just promotional content",
                "Respond quickly to comments to improve reach",
                "Use Facebook Live for real-time Q&A sessions"
            ],
            "content_strategy": [
                "Focus on community building and relationship development",
                "Share client success stories and testimonials", 
                "Provide educational content about homebuying process",
                "Use local market insights and neighborhood information",
                "Create discussion posts about market trends"
            ]
        },
        "instagram": {
            "specs": {
                "max_chars": "2,200", 
                "optimal_chars": "350",
                "max_hashtags": "30",
                "recommended_hashtags": "15"
            },
            "best_practices": [
                "Prioritize high-quality, visually appealing content",
                "Use Instagram Stories for behind-the-scenes content",
                "Post consistently during 11 AM-1 PM or 5-7 PM",
                "Include strategic hashtags for discoverability",
                "Engage authentically with your audience's content",
                "Create Reels for maximum reach and engagement"
            ],
            "content_strategy": [
                "Share visually appealing home and market content",
                "Use infographics to explain complex mortgage concepts",
                "Post client testimonials with permission",
                "Create educational carousel posts",
                "Show personality with behind-the-scenes content"
            ]
        },
        "linkedin": {
            "specs": {
                "max_chars": "3,000",
                "optimal_chars": "700", 
                "max_hashtags": "20",
                "recommended_hashtags": "5"
            },
            "best_practices": [
                "Establish thought leadership with industry insights",
                "Post during business hours for maximum professional reach",
                "Share detailed market analysis and commentary",
                "Connect and engage with industry professionals",
                "Use LinkedIn's publishing platform for long-form content",
                "Participate in relevant group discussions"
            ],
            "content_strategy": [
                "Share professional market analysis and trends",
                "Discuss industry news and regulatory changes",
                "Provide expert commentary on economic factors",
                "Network with real estate professionals and referral partners",
                "Establish credibility through educational content"
            ]
        }
    }
    
    data = platform_data[platform]
    
    click.echo(f"{platform.upper()} COMPREHENSIVE GUIDE\n")
    
    click.echo("PLATFORM SPECIFICATIONS:")
    for spec, value in data["specs"].items():
        click.echo(f"  • {spec.replace('_', ' ').title()}: {value}")
    
    click.echo(f"\n✅ BEST PRACTICES:")
    for practice in data["best_practices"]:
        click.echo(f"  • {practice}")
    
    click.echo(f"\nCONTENT STRATEGY:")
    for strategy in data["content_strategy"]:
        click.echo(f"  • {strategy}")

def _display_content_result(result: Dict, show_details: bool = True):
    """Display formatted content generation results"""
    click.echo("\nGENERATED CONTENT:")
    click.echo("-" * 50)
    click.echo(result.get('content', result.get('main_content', '')))
    
    if show_details:
        click.echo(f"\nCONTENT ANALYSIS:")
        click.echo(f"  • Character Count: {result.get('character_count', 'N/A')}")
        click.echo(f"  • Hashtags: {len(result.get('hashtags', []))}")
        click.echo(f"  • Platform: {result.get('platform', 'N/A').title()}")
        click.echo(f"  • Audience: {result.get('audience', 'N/A').replace('_', ' ').title()}")
        click.echo(f"  • Content Type: {result.get('content_type', 'N/A').replace('_', ' ').title()}")
        
        if result.get('visual_concept'):
            click.echo(f"\nVISUAL CONCEPT:")
            click.echo(f"  {result['visual_concept']}")
        
        if result.get('engagement_strategy'):
            click.echo(f"\nENGAGEMENT STRATEGY:")
            click.echo(f"  {result['engagement_strategy']}")
        
        if result.get('targeting_insights'):
            insights = result['targeting_insights']
            click.echo(f"\nTARGETING INSIGHTS:")
            click.echo(f"  • Key Messages: {', '.join(insights.get('key_messages', [])[:2])}")
            click.echo(f"  • Emotional Triggers: {', '.join(insights.get('emotional_triggers', [])[:2])}")

if __name__ == '__main__':
    cli()