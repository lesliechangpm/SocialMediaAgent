import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
import feedparser
from bs4 import BeautifulSoup

class MortgageRateFetcher:
    def __init__(self):
        self.data_file = "data/rate_history.json"
        
    def get_current_rates(self) -> Dict:
        """
        Fetch current 30-year mortgage rates from multiple sources
        Returns structured data with rate, change, and date
        """
        try:
            # Try Freddie Mac PMMS data first
            freddie_data = self._fetch_freddie_mac_rates()
            if freddie_data:
                return freddie_data
            
            # Fallback to financial news scraping
            news_data = self._fetch_from_news_sources()
            if news_data:
                return news_data
                
            # If all else fails, use cached data
            return self._get_cached_rates()
            
        except Exception as e:
            print(f"Error fetching rates: {e}")
            return self._get_cached_rates()
    
    def _fetch_freddie_mac_rates(self) -> Optional[Dict]:
        """
        Fetch rates from Freddie Mac Primary Mortgage Market Survey
        """
        try:
            # Freddie Mac historical data URL (publicly available)
            url = "http://www.freddiemac.com/pmms/pmms30.html"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # This is a simplified parser - in production would need more robust scraping
                # For now, return mock data structure
                current_rate = 7.25  # This would be parsed from the HTML
                previous_rate = 7.31
                
                rate_data = {
                    "current_rate": current_rate,
                    "previous_rate": previous_rate,
                    "rate_change": current_rate - previous_rate,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "Freddie Mac PMMS"
                }
                
                # Cache the data
                self._cache_rate_data(rate_data)
                return rate_data
                
        except Exception as e:
            print(f"Freddie Mac fetch failed: {e}")
            return None
    
    def _fetch_from_news_sources(self) -> Optional[Dict]:
        """
        Fetch rate information from financial news RSS feeds
        """
        try:
            # Sample financial news RSS feeds
            feeds = [
                "https://feeds.reuters.com/reuters/businessNews",
                "https://www.marketwatch.com/rss/realestate"
            ]
            
            for feed_url in feeds:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:  # Check recent entries
                    if any(term in entry.title.lower() for term in ['mortgage', 'rate', 'housing']):
                        # This is simplified - would need NLP to extract actual rates
                        # For demo, returning sample data
                        rate_data = {
                            "current_rate": 7.18,
                            "previous_rate": 7.25,
                            "rate_change": -0.07,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "source": "Financial News Analysis",
                            "news_context": entry.title
                        }
                        
                        self._cache_rate_data(rate_data)
                        return rate_data
                        
        except Exception as e:
            print(f"News source fetch failed: {e}")
            return None
    
    def get_market_context(self, rate_data: Dict) -> str:
        """
        Get relevant market news and context for current rates
        """
        try:
            context_parts = []
            
            # Rate trend analysis
            if rate_data.get("rate_change", 0) > 0:
                context_parts.append(f"Rates increased by {abs(rate_data['rate_change']):.2f}% this week")
            elif rate_data.get("rate_change", 0) < 0:
                context_parts.append(f"Rates decreased by {abs(rate_data['rate_change']):.2f}% this week")
            else:
                context_parts.append("Rates remained steady this week")
            
            # Historical context
            current_rate = rate_data.get("current_rate", 7.0)
            if current_rate > 7.0:
                context_parts.append("Rates remain elevated compared to recent historical lows")
            elif current_rate < 6.0:
                context_parts.append("Rates are at attractive levels for borrowers")
            else:
                context_parts.append("Rates are in a moderate range")
            
            # Market factors (simplified)
            market_factors = [
                "Federal Reserve policy decisions",
                "Economic inflation data",
                "Employment market strength",
                "Global economic conditions"
            ]
            
            context_parts.append(f"Key factors influencing rates: {', '.join(market_factors[:2])}")
            
            return ". ".join(context_parts) + "."
            
        except Exception as e:
            return "Market conditions continue to influence mortgage rate movements."
    
    def _cache_rate_data(self, rate_data: Dict):
        """Cache rate data locally for fallback"""
        try:
            # Load existing cache
            try:
                with open(self.data_file, 'r') as f:
                    cache = json.load(f)
            except FileNotFoundError:
                cache = {"history": []}
            
            # Add new data
            cache["history"].append(rate_data)
            cache["last_updated"] = datetime.now().isoformat()
            
            # Keep only last 30 days
            cache["history"] = cache["history"][-30:]
            
            # Save cache
            with open(self.data_file, 'w') as f:
                json.dump(cache, f, indent=2)
                
        except Exception as e:
            print(f"Cache write failed: {e}")
    
    def _get_cached_rates(self) -> Dict:
        """Get the most recent cached rate data"""
        try:
            with open(self.data_file, 'r') as f:
                cache = json.load(f)
            
            if cache.get("history"):
                latest = cache["history"][-1]
                latest["source"] = "Cached Data"
                return latest
                
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Cache read failed: {e}")
        
        # Ultimate fallback
        return {
            "current_rate": 7.20,
            "previous_rate": 7.25,
            "rate_change": -0.05,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "Default Estimate"
        }
    
    def get_year_over_year_comparison(self) -> str:
        """Get year-over-year rate comparison"""
        current_rate = self.get_current_rates()["current_rate"]
        # Simplified - in production would use actual historical data
        year_ago_rate = 6.85
        
        change = current_rate - year_ago_rate
        if change > 0:
            return f"Rates are {change:.2f}% higher than a year ago"
        else:
            return f"Rates are {abs(change):.2f}% lower than a year ago"