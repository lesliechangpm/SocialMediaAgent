#!/usr/bin/env python3

import click
import os
import json
from typing import Dict, Optional
from datetime import datetime

from .data_fetcher import MortgageRateFetcher
from .content_generator import SocialContentGenerator
from .audience_profiles import AudienceTargeting
from .platform_optimizer import PlatformOptimizer

class MortgageRateAgent:
    def __init__(self):
        self.rate_fetcher = MortgageRateFetcher()
        self.audience_targeting = AudienceTargeting()
        self.platform_optimizer = PlatformOptimizer()
        self.content_generator = None
        
    def initialize_generator(self, api_key: Optional[str] = None):
        """Initialize the content generator with API key"""
        try:
            self.content_generator = SocialContentGenerator(api_key)
            return True
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            return False

@click.group()
@click.pass_context
def cli(ctx):
    """Mortgage Rate Social Media Agent - Generate targeted content for loan officers"""
    ctx.ensure_object(dict)
    ctx.obj['agent'] = MortgageRateAgent()

@cli.command()
@click.option('--platform', '-p', 
              type=click.Choice(['facebook', 'instagram', 'linkedin'], case_sensitive=False),
              required=True, help='Target social media platform')
@click.option('--audience', '-a',
              type=click.Choice(['millennials', 'gen_x', 'baby_boomers'], case_sensitive=False),
              required=True, help='Target audience demographic')
@click.option('--tone', '-t',
              type=click.Choice(['educational', 'promotional', 'market_update', 'call_to_action'], case_sensitive=False),
              default='market_update', help='Content tone/type')
@click.option('--api-key', envvar='ANTHROPIC_API_KEY', help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
@click.option('--loan-officer', '-lo', help='Loan officer name for personalization')
@click.option('--company', '-c', help='Company name for personalization')
@click.option('--location', '-l', help='Location for local market context')
@click.option('--output', '-o', type=click.Path(), help='Save output to file (JSON format)')
@click.option('--preview', is_flag=True, help='Preview content before finalizing')
@click.pass_context
def generate(ctx, platform, audience, tone, api_key, loan_officer, company, location, output, preview):
    """Generate social media content for current mortgage rates"""
    
    agent = ctx.obj['agent']
    
    # Initialize content generator
    if not agent.initialize_generator(api_key):
        return
    
    try:
        # Fetch current rate data
        click.echo("📊 Fetching current mortgage rate data...")
        rate_data = agent.rate_fetcher.get_current_rates()
        market_context = agent.rate_fetcher.get_market_context(rate_data)
        
        # Display current rates
        click.echo("\n" + "="*50)
        click.echo("CURRENT MORTGAGE RATE DATA")
        click.echo("="*50)
        click.echo(f"30-Year Fixed Rate: {rate_data.get('current_rate', 'N/A')}%")
        click.echo(f"Previous Rate: {rate_data.get('previous_rate', 'N/A')}%")
        change = rate_data.get('rate_change', 0)
        if change > 0:
            click.echo(f"Weekly Change: +{change:.3f}% ⬆️")
        elif change < 0:
            click.echo(f"Weekly Change: {change:.3f}% ⬇️")
        else:
            click.echo(f"Weekly Change: No change ➡️")
        click.echo(f"Date: {rate_data.get('date', 'Current')}")
        click.echo(f"Source: {rate_data.get('source', 'N/A')}")
        click.echo(f"Market Context: {market_context}")
        
        # Prepare loan officer info
        loan_officer_info = None
        if loan_officer or company or location:
            loan_officer_info = {
                'name': loan_officer or 'Your Loan Officer',
                'company': company or 'Your Mortgage Company', 
                'location': location or 'Your Area',
                'specialties': ['Home Loans', 'Refinancing']
            }
        
        # Generate content
        click.echo(f"\n🤖 Generating {tone} content for {audience} on {platform}...")
        
        content_result = agent.content_generator.generate_post(
            rate_data=rate_data,
            platform=platform,
            audience=audience,
            content_type=tone,
            loan_officer_info=loan_officer_info
        )
        
        # Optimize for platform
        optimized_content = agent.platform_optimizer.optimize_content(content_result, platform)
        
        # Validate content
        validation = agent.platform_optimizer.validate_content(optimized_content, platform)
        
        # Display results
        display_content_results(optimized_content, validation, platform, audience)
        
        # Preview and confirmation
        if preview:
            if not click.confirm("\nDo you want to proceed with this content?"):
                click.echo("Content generation cancelled.")
                return
        
        # Save to file if requested
        if output:
            save_content_to_file(optimized_content, output, rate_data)
            click.echo(f"\n💾 Content saved to {output}")
        
        # Show next steps
        show_next_steps(platform, optimized_content)
        
    except Exception as e:
        click.echo(f"Error generating content: {e}", err=True)

@cli.command()
@click.option('--platform', '-p', 
              type=click.Choice(['facebook', 'instagram', 'linkedin'], case_sensitive=False),
              required=True, help='Target social media platform')
@click.option('--audience', '-a',
              type=click.Choice(['millennials', 'gen_x', 'baby_boomers'], case_sensitive=False),
              required=True, help='Target audience demographic')
@click.option('--api-key', envvar='ANTHROPIC_API_KEY', help='Anthropic API key')
@click.option('--count', '-n', default=3, help='Number of variations to generate')
@click.pass_context
def variations(ctx, platform, audience, api_key, count):
    """Generate multiple content variations for A/B testing"""
    
    agent = ctx.obj['agent']
    
    if not agent.initialize_generator(api_key):
        return
    
    try:
        # Fetch rate data
        click.echo("📊 Fetching current mortgage rate data...")
        rate_data = agent.rate_fetcher.get_current_rates()
        
        # Generate variations
        click.echo(f"\n🔄 Generating {count} content variations for {audience} on {platform}...")
        
        variations = agent.content_generator.generate_content_variations(
            rate_data, platform, audience, count
        )
        
        # Display each variation
        for i, variation in enumerate(variations, 1):
            click.echo(f"\n" + "="*60)
            click.echo(f"VARIATION #{i} ({variation.get('content_type', 'unknown').upper()})")
            click.echo("="*60)
            
            optimized = agent.platform_optimizer.optimize_content(variation, platform)
            display_content_results(optimized, {}, platform, audience, show_tips=False)
        
        # Best practices reminder
        practices = agent.platform_optimizer.get_platform_best_practices(platform)
        click.echo(f"\n📝 {platform.upper()} BEST PRACTICES:")
        for category, tips in practices.items():
            click.echo(f"\n{category.upper()}:")
            for tip in tips:
                click.echo(f"  • {tip}")
        
    except Exception as e:
        click.echo(f"Error generating variations: {e}", err=True)

@cli.command()
def rates(ctx):
    """Display current mortgage rates and market context"""
    
    agent = ctx.obj['agent']
    
    try:
        click.echo("📊 Fetching current mortgage rate data...")
        rate_data = agent.rate_fetcher.get_current_rates()
        market_context = agent.rate_fetcher.get_market_context(rate_data)
        year_comparison = agent.rate_fetcher.get_year_over_year_comparison()
        
        click.echo("\n" + "="*50)
        click.echo("MORTGAGE RATE SUMMARY")
        click.echo("="*50)
        click.echo(f"30-Year Fixed Rate: {rate_data.get('current_rate', 'N/A')}%")
        click.echo(f"Previous Rate: {rate_data.get('previous_rate', 'N/A')}%")
        
        change = rate_data.get('rate_change', 0)
        if change > 0:
            click.echo(f"Weekly Change: +{change:.3f}% (↑ INCREASED)")
        elif change < 0:
            click.echo(f"Weekly Change: {change:.3f}% (↓ DECREASED)")
        else:
            click.echo(f"Weekly Change: No change (→ STEADY)")
        
        click.echo(f"\nDate: {rate_data.get('date', 'Current')}")
        click.echo(f"Data Source: {rate_data.get('source', 'N/A')}")
        click.echo(f"\nMarket Context: {market_context}")
        click.echo(f"Year-over-Year: {year_comparison}")
        
    except Exception as e:
        click.echo(f"Error fetching rates: {e}", err=True)

@cli.command()
def audiences():
    """List available audience segments and their characteristics"""
    
    agent = MortgageRateAgent()
    
    click.echo("🎯 AVAILABLE AUDIENCE SEGMENTS\n")
    
    for audience_key in agent.audience_targeting.list_audiences():
        profile = agent.audience_targeting.get_profile(audience_key)
        
        click.echo(f"👥 {profile.name.upper()} ({profile.age_range})")
        click.echo(f"Communication Style: {profile.communication_style}")
        click.echo("Key Concerns:")
        for concern in profile.key_concerns[:3]:
            click.echo(f"  • {concern}")
        click.echo("Messaging Focus:")
        for focus in profile.messaging_focus[:3]:
            click.echo(f"  • {focus}")
        click.echo("")

@cli.command()
@click.argument('platform', type=click.Choice(['facebook', 'instagram', 'linkedin'], case_sensitive=False))
def platform_info(platform):
    """Show platform specifications and best practices"""
    
    agent = MortgageRateAgent()
    
    # Get platform limits
    limits = agent.content_generator.get_platform_limits(platform) if agent.content_generator else {}
    practices = agent.platform_optimizer.get_platform_best_practices(platform)
    
    click.echo(f"📱 {platform.upper()} PLATFORM INFORMATION\n")
    
    if limits:
        click.echo("CHARACTER LIMITS & RECOMMENDATIONS:")
        click.echo(f"  • Max Characters: {limits.get('character_limit', 'N/A')}")
        click.echo(f"  • Recommended Length: {limits.get('recommended_length', 'N/A')}")
        click.echo(f"  • Max Hashtags: {limits.get('hashtag_limit', 'N/A')}")
        click.echo(f"  • Recommended Hashtags: {limits.get('recommended_hashtags', 'N/A')}")
        click.echo("")
    
    for category, tips in practices.items():
        click.echo(f"{category.upper()} BEST PRACTICES:")
        for tip in tips:
            click.echo(f"  • {tip}")
        click.echo("")

def display_content_results(content: Dict, validation: Dict, platform: str, audience: str, show_tips: bool = True):
    """Display formatted content results"""
    
    click.echo(f"\n📝 GENERATED CONTENT:")
    click.echo("-" * 40)
    click.echo(content.get('formatted_content', content.get('content', '')))
    
    if content.get('hashtags'):
        click.echo(f"\n🏷️  HASHTAGS: {' '.join(content['hashtags'])}")
    
    click.echo(f"\n📊 CONTENT STATS:")
    click.echo(f"  • Character Count: {content.get('character_count', len(content.get('content', '')))}")
    click.echo(f"  • Hashtag Count: {len(content.get('hashtags', []))}")
    click.echo(f"  • Platform: {platform.title()}")
    click.echo(f"  • Audience: {audience.replace('_', ' ').title()}")
    
    # Validation results
    if validation.get('warnings'):
        click.echo(f"\n⚠️  WARNINGS:")
        for warning in validation['warnings']:
            click.echo(f"  • {warning}")
    
    if validation.get('errors'):
        click.echo(f"\n❌ ERRORS:")
        for error in validation['errors']:
            click.echo(f"  • {error}")
    
    # Visual suggestions
    if content.get('visual_suggestions'):
        visual_sugg = content['visual_suggestions']
        if isinstance(visual_sugg, dict):
            click.echo(f"\n🎨 VISUAL CONTENT SUGGESTIONS:")
            for key, suggestion in visual_sugg.items():
                click.echo(f"  • {key.replace('_', ' ').title()}: {suggestion}")
        else:
            click.echo(f"\n🎨 VISUAL SUGGESTION: {visual_sugg}")
    
    # Optimal posting times
    if content.get('best_posting_times') and show_tips:
        times = content['best_posting_times']
        click.echo(f"\n⏰ OPTIMAL POSTING TIMES:")
        click.echo(f"  • Weekdays: {', '.join(times.get('weekdays', []))}")
        click.echo(f"  • Weekends: {', '.join(times.get('weekends', []))}")
        if times.get('timezone_note'):
            click.echo(f"  • Note: {times['timezone_note']}")

def save_content_to_file(content: Dict, filepath: str, rate_data: Dict):
    """Save content to JSON file"""
    
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'rate_data': rate_data,
        'content': content,
        'metadata': {
            'platform': content.get('platform'),
            'audience': content.get('audience'),
            'content_type': content.get('content_type'),
            'character_count': content.get('character_count'),
            'hashtag_count': len(content.get('hashtags', []))
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

def show_next_steps(platform: str, content: Dict):
    """Show suggested next steps"""
    
    click.echo(f"\n🚀 NEXT STEPS:")
    click.echo(f"  1. Copy the content above for posting to {platform.title()}")
    click.echo(f"  2. Create or source the suggested visual content")
    
    if content.get('best_posting_times'):
        times = content['best_posting_times']
        click.echo(f"  3. Schedule for optimal times: {', '.join(times.get('weekdays', [])[:2])}")
    
    click.echo(f"  4. Monitor engagement and adjust future content accordingly")
    click.echo(f"  5. Consider running A/B tests with different variations")

if __name__ == '__main__':
    cli()