#!/usr/bin/env python3
"""
Social Media Agent - Web Application
AI-Powered Mortgage Content Generator for Leslie Chang - CMG Mortgage
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
from pathlib import Path

# Import our existing modules
try:
    from social_media_agent import SocialMediaAgent, SmartAudienceTargeting
except ImportError:
    # If direct import fails, try relative import
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from social_media_agent import SocialMediaAgent, SmartAudienceTargeting

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize our agent
agent = SocialMediaAgent()
targeting = SmartAudienceTargeting()

# Global settings
DEFAULT_SETTINGS = {
    'loan_officer': 'Leslie Chang',
    'company': 'CMG Mortgage',
    'default_platform': 'instagram',
    'default_audience': 'millennials',
    'api_key_set': bool(os.getenv('ANTHROPIC_API_KEY'))
}

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        # Get current rates for dashboard
        current_rates = agent.get_current_rates()
        market_analysis = agent.get_market_analysis()
        
        return render_template('index.html', 
                             rates=current_rates,
                             market_analysis=market_analysis,
                             settings=DEFAULT_SETTINGS)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        flash(f"Error loading dashboard: {e}", 'error')
        return render_template('index.html', 
                             rates=None,
                             market_analysis="Unable to fetch market data",
                             settings=DEFAULT_SETTINGS)

@app.route('/generate')
def generate_page():
    """Content generation page"""
    return render_template('generate.html', 
                         settings=DEFAULT_SETTINGS,
                         audiences=targeting.list_audiences())

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for content generation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['platform', 'audience', 'content_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Initialize agent if needed
        api_key = data.get('api_key') or os.getenv('ANTHROPIC_API_KEY')
        if not agent.content_generator:
            if not agent.initialize(api_key):
                return jsonify({'error': 'Failed to initialize AI generator. Check your API key.'}), 400
        
        # Generate content
        result = agent.generate_content(
            platform=data['platform'],
            audience=data['audience'],
            content_type=data['content_type'],
            loan_officer=data.get('loan_officer', DEFAULT_SETTINGS['loan_officer']),
            company=data.get('company', DEFAULT_SETTINGS['company']),
            custom_focus=data.get('custom_focus'),
            save_output=data.get('save_output', False)
        )
        
        # Add generation timestamp
        result['generated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'content': result
        })
        
    except Exception as e:
        logger.error(f"Content generation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/variations', methods=['POST'])
def api_variations():
    """API endpoint for generating content variations"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'platform' not in data or 'audience' not in data:
            return jsonify({'error': 'Missing required fields: platform, audience'}), 400
        
        # Initialize agent if needed
        api_key = data.get('api_key') or os.getenv('ANTHROPIC_API_KEY')
        if not agent.content_generator:
            if not agent.initialize(api_key):
                return jsonify({'error': 'Failed to initialize AI generator. Check your API key.'}), 400
        
        # Generate variations
        variations = agent.generate_variations(
            platform=data['platform'],
            audience=data['audience'],
            count=data.get('count', 3),
            loan_officer=data.get('loan_officer', DEFAULT_SETTINGS['loan_officer']),
            company=data.get('company', DEFAULT_SETTINGS['company'])
        )
        
        return jsonify({
            'success': True,
            'variations': variations
        })
        
    except Exception as e:
        logger.error(f"Variations generation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/rates')
def api_rates():
    """API endpoint for current mortgage rates"""
    try:
        rates = agent.get_current_rates()
        analysis = agent.get_market_analysis()
        
        return jsonify({
            'success': True,
            'rates': rates,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Rates API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/audiences')
def api_audiences():
    """API endpoint for audience information"""
    try:
        audiences_data = {}
        for audience_key in targeting.list_audiences():
            profile = targeting.get_profile(audience_key)
            audiences_data[audience_key] = {
                'name': profile['name'],
                'age_range': profile['age_range'],
                'demographics': profile['demographics'],
                'psychographics': profile['psychographics'],
                'digital_behavior': profile['digital_behavior'],
                'mortgage_focus': profile['mortgage_focus']
            }
        
        return jsonify({
            'success': True,
            'audiences': audiences_data
        })
        
    except Exception as e:
        logger.error(f"Audiences API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/audiences')
def audiences_page():
    """Audience information page"""
    return render_template('audiences.html')

@app.route('/analytics')
def analytics_page():
    """Analytics and performance page"""
    try:
        # Load recent generated content for analytics
        content_dir = Path('generated_content')
        recent_content = []
        
        if content_dir.exists():
            for file_path in sorted(content_dir.glob('*.json'), reverse=True)[:20]:
                try:
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        content['filename'] = file_path.name
                        recent_content.append(content)
                except Exception as e:
                    logger.warning(f"Error loading {file_path}: {e}")
        
        return render_template('analytics.html', recent_content=recent_content)
        
    except Exception as e:
        logger.error(f"Analytics page error: {e}")
        return render_template('analytics.html', recent_content=[])

@app.route('/settings')
def settings_page():
    """Settings and configuration page"""
    return render_template('settings.html', settings=DEFAULT_SETTINGS)

@app.route('/api/settings', methods=['POST'])
def api_update_settings():
    """API endpoint for updating settings"""
    try:
        data = request.get_json()
        
        # Update environment file
        env_path = Path('.env')
        env_lines = []
        
        # Read existing .env file
        if env_path.exists():
            with open(env_path, 'r') as f:
                env_lines = f.readlines()
        
        # Update or add new settings
        settings_map = {
            'api_key': 'ANTHROPIC_API_KEY',
            'loan_officer': 'DEFAULT_LOAN_OFFICER_NAME',
            'company': 'DEFAULT_COMPANY_NAME',
            'location': 'DEFAULT_LOCATION'
        }
        
        updated_lines = []
        updated_keys = set()
        
        for line in env_lines:
            line = line.strip()
            if '=' in line:
                key, _ = line.split('=', 1)
                # Check if this key needs updating
                for setting_key, env_key in settings_map.items():
                    if key == env_key and setting_key in data:
                        updated_lines.append(f"{env_key}={data[setting_key]}\n")
                        updated_keys.add(env_key)
                        break
                else:
                    updated_lines.append(line + '\n')
            else:
                updated_lines.append(line + '\n')
        
        # Add new settings that weren't in the file
        for setting_key, env_key in settings_map.items():
            if env_key not in updated_keys and setting_key in data:
                updated_lines.append(f"{env_key}={data[setting_key]}\n")
        
        # Write updated .env file
        with open(env_path, 'w') as f:
            f.writelines(updated_lines)
        
        # Update environment variables for current session
        for setting_key, env_key in settings_map.items():
            if setting_key in data:
                os.environ[env_key] = data[setting_key]
        
        # Reinitialize agent if API key changed
        if 'api_key' in data:
            agent.initialize(data['api_key'])
        
        flash('Settings updated successfully!', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Settings update error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/help')
def help_page():
    """Help and documentation page"""
    return render_template('help.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal server error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Ensure required directories exist
    for directory in ['templates', 'static/css', 'static/js', 'static/images', 'generated_content']:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Initialize agent on startup
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        try:
            agent.initialize(api_key)
            logger.info("Agent initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize agent: {e}")
    
    # Run the web application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("SOCIAL MEDIA AGENT - WEB APPLICATION")
    print("=" * 60)
    print(f"Starting server on http://localhost:{port}")
    print("Leslie Chang - CMG Mortgage Ready")
    if api_key:
        print("AI Agent Initialized")
    else:
        print("API Key Not Set - Configure in Settings")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)