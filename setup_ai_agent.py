#!/usr/bin/env python3
"""
Setup script for Social Media Agent - AI-Powered
"""

import os
import sys
from pathlib import Path
import subprocess
import shutil

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        "data",
        "logs", 
        "generated_content",
        "config/backups",
        "templates",
        "docs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def setup_environment():
    """Setup environment configuration"""
    env_template = Path(".env.production")
    env_file = Path(".env")
    
    if not env_file.exists() and env_template.exists():
        shutil.copy(env_template, env_file)
        print("Created .env file from template")
        print("Please edit .env file and add your ANTHROPIC_API_KEY")
    else:
        print("Environment file already exists")

def install_dependencies():
    """Install required Python packages"""
    requirements_files = ["requirements_ai.txt", "requirements.txt"]
    
    for req_file in requirements_files:
        if Path(req_file).exists():
            print(f"Installing dependencies from {req_file}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-r", req_file
                ])
                print(f"Successfully installed dependencies from {req_file}")
                break
            except subprocess.CalledProcessError as e:
                print(f"Failed to install dependencies from {req_file}: {e}")
                continue
    else:
        print("No requirements file found")

def create_config_files():
    """Create additional configuration files"""
    
    # Create logging config
    log_config = """
version: 1
formatters:
  default:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: default
  file:
    class: logging.FileHandler
    filename: logs/social_media_agent.log
    level: INFO
    formatter: default
root:
  level: INFO
  handlers: [console, file]
"""
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    with open(config_dir / "logging.yaml", "w") as f:
        f.write(log_config.strip())
    print("Created logging configuration")
    
    # Create AI prompts template
    prompts_config = """
# AI Content Generation Prompts

system_prompt: |
  You are an expert mortgage industry social media content creator specializing in 
  converting prospects into qualified leads through engaging, compliant content.

content_templates:
  educational:
    millennials: "Focus on first-time buyer education and affordability"
    gen_x: "Emphasize refinancing strategies and family financial planning" 
    baby_boomers: "Highlight security, stability, and retirement planning"
  
  market_update:
    hook_patterns:
      - "This week's mortgage rates:"
      - "Market update:"
      - "Rate alert:"
    
  promotional:
    value_propositions:
      - "Personalized guidance throughout the process"
      - "Expert market knowledge and timing"
      - "Access to multiple loan programs"

compliance:
  required_disclaimers:
    - "Rates subject to change"
    - "Equal Housing Opportunity"
  
  review_keywords:
    - "guarantee"
    - "sure thing"
    - "no risk"
"""
    
    with open(config_dir / "ai_prompts.yaml", "w") as f:
        f.write(prompts_config.strip())
    print("Created AI prompts configuration")

def test_installation():
    """Test if the installation was successful"""
    print("\nTesting installation...")
    
    try:
        # Test imports
        import anthropic
        import click
        import yaml
        import requests
        print("All required packages imported successfully")
        
        # Test API key (without making actual calls)
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key and api_key != 'your_anthropic_api_key_here':
            print("API key found in environment")
        else:
            print("API key not set - please configure ANTHROPIC_API_KEY")
        
        # Test file structure
        required_files = [
            "social_media_agent.py",
            "config/settings.yaml", 
            "config/ai_prompts.yaml"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"Missing files: {', '.join(missing_files)}")
        else:
            print("All required files present")
            
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    
    return True

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print("SOCIAL MEDIA AGENT - AI-POWERED SETUP COMPLETE!")
    print("="*60)
    print()
    print("NEXT STEPS:")
    print()
    print("1. Configure your API key:")
    print("   - Edit .env file and add your ANTHROPIC_API_KEY")
    print("   - Or set environment variable: set ANTHROPIC_API_KEY=your_key")
    print()
    print("2. Test the installation:")
    print("   - python social_media_agent.py rates")
    print()
    print("3. Generate your first AI content:")
    print("   - python social_media_agent.py generate -p instagram -a millennials")
    print()
    print("4. Use the easy menu interface:")
    print("   - Double-click: social_media_agent.bat")
    print()
    print("AVAILABLE COMMANDS:")
    print("   - generate - Create AI-powered content")
    print("   - variations - Generate multiple versions")
    print("   - rates - Get current mortgage rates") 
    print("   - audiences - View targeting guide")
    print("   - platform-info - Platform best practices")
    print()
    print("For Leslie Chang - CMG Mortgage:")
    print("   All commands automatically include your branding!")
    print()
    print("Ready to create unlimited AI-powered mortgage content!")

def main():
    """Main setup function"""
    print("Setting up Social Media Agent - AI-Powered...")
    print("="*60)
    
    try:
        create_directory_structure()
        setup_environment()
        install_dependencies()
        create_config_files()
        
        if test_installation():
            print_next_steps()
            return True
        else:
            print("Installation test failed. Please check the errors above.")
            return False
            
    except Exception as e:
        print(f"Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)