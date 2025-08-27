#!/usr/bin/env python3
"""
Simple test version of the Social Media Agent Web App
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'test-secret-key'
CORS(app)

# Simple mock data
DEFAULT_SETTINGS = {
    'loan_officer': 'Leslie Chang',
    'company': 'CMG Mortgage',
    'default_platform': 'instagram',
    'default_audience': 'millennials',
    'api_key_set': False
}

MOCK_RATES = {
    'current_rate': 6.875,
    'rate_change': -0.125,
    'date': datetime.now().strftime('%Y-%m-%d'),
    'source': 'Mock Data',
    'confidence': 'live',
    'trend': 'stable',
    'last_updated': datetime.now().strftime('%H:%M'),
    'daily_change': -0.125,
    'weekly_change': 0.250,
    'monthly_change': -0.375
}

MOCK_ANALYSIS = "Current rates remain competitive for qualified borrowers. Market conditions favor refinancing opportunities."

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         rates=MOCK_RATES,
                         market_analysis=MOCK_ANALYSIS,
                         settings=DEFAULT_SETTINGS)

@app.route('/generate')
def generate_page():
    """Content generation page"""
    return render_template('generate.html', 
                         settings=DEFAULT_SETTINGS)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for content generation"""
    try:
        data = request.get_json()
        
        # Generate audience-specific mock content
        audience = data.get('audience', 'millennials')
        platform = data.get('platform', 'instagram')
        
        content_templates = {
            'millennials': f"🏠 Current mortgage rates are {MOCK_RATES['current_rate']}%! Great opportunity for first-time buyers to secure competitive rates with CMG Mortgage's innovative solutions. Contact {data.get('loan_officer', 'your loan officer')} at {data.get('company', 'CMG Mortgage')} for personalized guidance! #CMGMortgage #MortgageRates #FirstTimeBuyer #RealEstate",
            'gen_x': f"💼 Refinancing opportunity alert! Rates at {MOCK_RATES['current_rate']}% could help you lower your monthly payments and access home equity with CMG Mortgage's strategic solutions. Strategic planning for your family's financial future starts here. Contact {data.get('loan_officer', 'your loan officer')} at {data.get('company', 'CMG Mortgage')} today. #CMGMortgage #Refinancing #HomeEquity #WealthBuilding",
            'baby_boomers': f"🏡 Current mortgage rates: {MOCK_RATES['current_rate']}%. For those considering downsizing or exploring reverse mortgage options, CMG Mortgage provides trusted guidance. {data.get('loan_officer', 'your loan officer')} at {data.get('company', 'CMG Mortgage')} offers personalized support for your retirement planning needs. #CMGMortgage #RetirementPlanning #TrustedAdvisor #ReverseReverse",
            'generation_alpha': f"🚀 Future homebuyers, take note! Today's rates at {MOCK_RATES['current_rate']}% demonstrate the importance of financial literacy and early planning. Smart homes, sustainable materials, and tech-integrated buying processes will shape tomorrow's real estate market with CMG Mortgage's innovation. Start your homeownership education journey with {data.get('loan_officer', 'your loan officer')} at {data.get('company', 'CMG Mortgage')}! #CMGMortgage #FutureHomebuyers #FinancialEducation #SmartHomes #SustainableLiving"
        }
        
        visual_concepts = {
            'millennials': 'Modern apartment with CMG Green and Teal Blue rate charts, clean minimalist design',
            'gen_x': 'Family home exterior with CMG Aqua Blue equity growth arrows and professional styling',
            'baby_boomers': 'Professional CMG office consultation with branded materials and warm lighting',
            'generation_alpha': 'Futuristic smart home with CMG brand colors, sustainability icons, and AR rate overlay'
        }
        
        engagement_strategies = {
            'millennials': 'Ask followers to share their homebuying questions in comments',
            'gen_x': 'Encourage sharing of refinancing success stories',
            'baby_boomers': 'Invite questions about retirement housing options',
            'generation_alpha': 'Create interactive content with polls about future home features'
        }
        
        mock_content = {
            'platform': platform,
            'audience': audience,
            'content_type': data.get('content_type', 'market_update'),
            'content': content_templates.get(audience, content_templates['millennials']),
            'character_count': len(content_templates.get(audience, content_templates['millennials'])),
            'visual_concept': visual_concepts.get(audience, visual_concepts['millennials']),
            'engagement_strategy': engagement_strategies.get(audience, engagement_strategies['millennials']),
            'ai_generated': False,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'content': mock_content
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/rates')
def api_rates():
    """API endpoint for current mortgage rates"""
    return jsonify({
        'success': True,
        'rates': MOCK_RATES,
        'analysis': MOCK_ANALYSIS
    })

@app.route('/api/audiences')
def api_audiences():
    """API endpoint for audience information"""
    mock_audiences = {
        'millennials': {
            'name': 'Millennials',
            'age_range': '27-42',
            'demographics': {
                'income_range': '$40K-$100K',
                'life_stage': 'First-time buyers',
                'priorities': ['Affordability', 'Transparency', 'Digital-first'],
                'challenges': ['Down payment', 'Credit score', 'Market competition']
            },
            'psychographics': {
                'values': ['Authenticity', 'Innovation', 'Work-life balance'],
                'communication_style': 'Direct, visual, authentic',
                'decision_factors': ['Research', 'Reviews', 'Recommendations']
            },
            'digital_behavior': {
                'platforms': ['Instagram', 'TikTok', 'Facebook'],
                'content_preferences': ['Video', 'Infographics', 'Stories'],
                'engagement_style': 'Interactive, social sharing',
                'posting_times': ['6-9AM', '6-9PM']
            },
            'mortgage_focus': {
                'primary_needs': ['First-time buyer programs', 'Down payment assistance'],
                'objections': ['High prices', 'Complex process', 'Hidden fees'],
                'motivators': ['Building equity', 'Stability', 'Investment']
            }
        },
        'gen_x': {
            'name': 'Generation X',
            'age_range': '43-58',
            'demographics': {
                'income_range': '$60K-$150K',
                'life_stage': 'Established families, refinancing',
                'priorities': ['Wealth building', 'Family security', 'Results-oriented'],
                'challenges': ['Market timing', 'Interest rate changes', 'Property taxes']
            },
            'psychographics': {
                'values': ['Stability', 'Self-reliance', 'Practicality'],
                'communication_style': 'Straightforward, fact-based, professional',
                'decision_factors': ['Data analysis', 'Expert advice', 'Track record']
            },
            'digital_behavior': {
                'platforms': ['Facebook', 'LinkedIn', 'Email'],
                'content_preferences': ['Articles', 'Data charts', 'Case studies'],
                'engagement_style': 'Research-focused, cautious sharing',
                'posting_times': ['7-9AM', '5-8PM']
            },
            'mortgage_focus': {
                'primary_needs': ['Refinancing options', 'Home equity loans', 'Investment properties'],
                'objections': ['Rate volatility', 'Closing costs', 'Time commitment'],
                'motivators': ['Lower payments', 'Cash out equity', 'Portfolio growth']
            }
        },
        'baby_boomers': {
            'name': 'Baby Boomers',
            'age_range': '59-77',
            'demographics': {
                'income_range': '$50K-$120K',
                'life_stage': 'Pre-retirement, downsizing',
                'priorities': ['Security', 'Stability', 'Professional relationships'],
                'challenges': ['Fixed income planning', 'Downsizing decisions', 'Health considerations']
            },
            'psychographics': {
                'values': ['Trust', 'Experience', 'Personal service'],
                'communication_style': 'Formal, detailed, relationship-based',
                'decision_factors': ['Reputation', 'Personal meetings', 'Referrals']
            },
            'digital_behavior': {
                'platforms': ['Facebook', 'LinkedIn', 'Email'],
                'content_preferences': ['Detailed articles', 'Personal stories', 'Educational content'],
                'engagement_style': 'Conservative, relationship-focused',
                'posting_times': ['8-11AM', '2-5PM']
            },
            'mortgage_focus': {
                'primary_needs': ['Reverse mortgages', 'Downsizing options', 'Retirement planning'],
                'objections': ['Complex terms', 'High fees', 'Risk concerns'],
                'motivators': ['Financial security', 'Legacy planning', 'Simplified finances']
            }
        },
        'generation_alpha': {
            'name': 'Generation Alpha',
            'age_range': '0-15',
            'demographics': {
                'income_range': 'Future earners',
                'life_stage': 'Students, digital natives',
                'priorities': ['Technology integration', 'Sustainability', 'Global connectivity'],
                'challenges': ['Future market conditions', 'Climate change', 'Economic uncertainty']
            },
            'psychographics': {
                'values': ['Innovation', 'Sustainability', 'Social impact', 'Authenticity'],
                'communication_style': 'Visual, interactive, instant, mobile-first',
                'decision_factors': ['AI assistance', 'Peer influence', 'Social proof', 'Environmental impact']
            },
            'digital_behavior': {
                'platforms': ['TikTok', 'YouTube Shorts', 'Instagram Reels', 'Discord'],
                'content_preferences': ['Short videos', 'Interactive content', 'AR/VR experiences', 'Gamified learning'],
                'engagement_style': 'Highly interactive, multi-platform, community-driven',
                'posting_times': ['3-6PM', '8-10PM']
            },
            'mortgage_focus': {
                'primary_needs': ['Financial education', 'Future planning', 'Sustainable housing', 'Tech-enabled processes'],
                'objections': ['Traditional processes', 'Complex paperwork', 'Lack of transparency', 'Environmental concerns'],
                'motivators': ['Smart home technology', 'Sustainable living', 'Community building', 'Investment potential']
            }
        }
    }
    
    return jsonify({
        'success': True,
        'audiences': mock_audiences
    })

@app.route('/audiences')
def audiences_page():
    """Audience information page"""
    return render_template('audiences.html')

@app.route('/analytics')
def analytics_page():
    """Analytics and performance page"""
    return render_template('analytics.html', recent_content=[])

@app.route('/settings')
def settings_page():
    """Settings and configuration page"""
    return render_template('settings.html', settings=DEFAULT_SETTINGS)

@app.route('/help')
def help_page():
    """Help and documentation page"""
    return render_template('help.html')

if __name__ == '__main__':
    # Ensure required directories exist
    for directory in ['templates', 'static/css', 'static/js']:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    port = 5000
    print("=" * 60)
    print("SOCIAL MEDIA AGENT - TEST WEB APPLICATION")
    print("=" * 60)
    print(f"Starting server on http://localhost:{port}")
    print("Leslie Chang - CMG Mortgage Ready (TEST MODE)")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=True)