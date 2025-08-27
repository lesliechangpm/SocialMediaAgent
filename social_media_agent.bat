@echo off
echo =========================================
echo Social Media Agent - AI-Powered
echo Leslie Chang - CMG Mortgage
echo =========================================
echo.

REM Check if .env file exists and has API key configured
if exist .env (
    echo Found .env file - checking API key configuration...
    findstr /C:"ANTHROPIC_API_KEY=your_anthropic_api_key_here" .env >nul
    if not errorlevel 1 (
        echo.
        echo WARNING: API key not configured in .env file!
        echo Edit .env file and replace 'your_anthropic_api_key_here' with your actual key
        echo.
        echo The agent will work with fallback templates, but AI features require the API key.
        echo Press any key to continue with fallback mode...
        pause
    )
) else (
    echo.
    echo WARNING: .env file not found!
    echo Copy .env.example to .env and add your API key for full functionality
    echo.
    echo The agent will work with fallback templates only.
    echo Press any key to continue with fallback mode...
    pause
)

:menu
echo Choose your action:
echo.
echo 1. Generate Instagram content (Millennials)
echo 2. Generate Facebook content (Gen X) 
echo 3. Generate LinkedIn content (Baby Boomers)
echo 4. Create 3 variations for testing
echo 5. Check current mortgage rates
echo 6. View audience targeting guide
echo 7. Platform best practices
echo 8. Exit
echo.

set /p choice="Enter your choice (1-8): "

if %choice%==1 (
    echo Generating AI-powered Instagram content for millennials...
    python social_media_agent.py generate -p instagram -a millennials --loan-officer "Leslie Chang" --company "CMG Mortgage" --save
    goto continue
)

if %choice%==2 (
    echo Generating AI-powered Facebook content for Gen X...
    python social_media_agent.py generate -p facebook -a gen_x --loan-officer "Leslie Chang" --company "CMG Mortgage" --save
    goto continue
)

if %choice%==3 (
    echo Generating AI-powered LinkedIn content for Baby Boomers...
    python social_media_agent.py generate -p linkedin -a baby_boomers --loan-officer "Leslie Chang" --company "CMG Mortgage" --save
    goto continue
)

if %choice%==4 (
    echo Choose platform for AI variations:
    echo 1. Instagram   2. Facebook   3. LinkedIn
    set /p platform_choice="Enter choice: "
    
    if !platform_choice!==1 (
        echo Generating 3 AI-powered Instagram variations...
        python social_media_agent.py variations -p instagram -a millennials --loan-officer "Leslie Chang" --company "CMG Mortgage"
    ) else if !platform_choice!==2 (
        echo Generating 3 AI-powered Facebook variations...
        python social_media_agent.py variations -p facebook -a gen_x --loan-officer "Leslie Chang" --company "CMG Mortgage"
    ) else if !platform_choice!==3 (
        echo Generating 3 AI-powered LinkedIn variations...
        python social_media_agent.py variations -p linkedin -a baby_boomers --loan-officer "Leslie Chang" --company "CMG Mortgage"
    )
    goto continue
)

if %choice%==5 (
    echo Fetching current mortgage rates with AI analysis...
    python social_media_agent.py rates
    goto continue
)

if %choice%==6 (
    echo Loading comprehensive audience targeting guide...
    python social_media_agent.py audiences
    goto continue
)

if %choice%==7 (
    echo Choose platform for best practices:
    echo 1. Instagram   2. Facebook   3. LinkedIn
    set /p platform_choice="Enter choice: "
    
    if !platform_choice!==1 (
        python social_media_agent.py platform-info instagram
    ) else if !platform_choice!==2 (
        python social_media_agent.py platform-info facebook
    ) else if !platform_choice!==3 (
        python social_media_agent.py platform-info linkedin
    )
    goto continue
)

if %choice%==8 (
    echo Thank you for using Social Media Agent!
    exit /b
)

echo Invalid choice. Please try again.
goto menu

:continue
echo.
echo =========================================
set /p again="Continue using Social Media Agent? (y/n): "
if /i %again%==y goto menu
echo Thank you for using Social Media Agent - AI-Powered!
pause