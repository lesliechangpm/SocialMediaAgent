@echo off
echo =========================================
echo Social Media Agent - AI-Powered
echo Leslie Chang - CMG Mortgage
echo =========================================
echo.

REM Check if API key is set
if "%ANTHROPIC_API_KEY%"=="" (
    echo ERROR: ANTHROPIC_API_KEY environment variable not set!
    echo.
    echo Please set your Anthropic API key:
    echo set ANTHROPIC_API_KEY=your_key_here
    echo.
    echo Or copy .env.production to .env and edit with your key
    pause
    exit /b 1
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