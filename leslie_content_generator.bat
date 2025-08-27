@echo off
echo ====================================
echo Leslie Chang - CMG Mortgage 
echo Social Media Content Generator
echo ====================================
echo.

:menu
echo Choose your platform and audience:
echo.
echo 1. Instagram - Millennials (Educational)
echo 2. Instagram - Millennials (Promotional)  
echo 3. Facebook - Gen X (Market Update)
echo 4. Facebook - Gen X (Educational)
echo 5. LinkedIn - Baby Boomers (Professional)
echo 6. LinkedIn - Baby Boomers (Market Analysis)
echo 7. Generate 3 variations for testing
echo 8. Check current mortgage rates
echo 9. Exit
echo.

set /p choice="Enter your choice (1-9): "

if %choice%==1 (
    echo Generating Instagram educational content for millennials...
    python prototype.py generate -p instagram -a millennials -t educational --loan-officer "Leslie Chang" --company "CMG Mortgage"
    goto continue
)

if %choice%==2 (
    echo Generating Instagram promotional content for millennials...
    python prototype.py generate -p instagram -a millennials -t promotional --loan-officer "Leslie Chang" --company "CMG Mortgage"
    goto continue
)

if %choice%==3 (
    echo Generating Facebook market update for Gen X...
    python prototype.py generate -p facebook -a gen_x -t market_update --loan-officer "Leslie Chang" --company "CMG Mortgage"
    goto continue
)

if %choice%==4 (
    echo Generating Facebook educational content for Gen X...
    python prototype.py generate -p facebook -a gen_x -t educational --loan-officer "Leslie Chang" --company "CMG Mortgage"
    goto continue
)

if %choice%==5 (
    echo Generating LinkedIn professional content for Baby Boomers...
    python prototype.py generate -p linkedin -a baby_boomers -t promotional --loan-officer "Leslie Chang" --company "CMG Mortgage"
    goto continue
)

if %choice%==6 (
    echo Generating LinkedIn market analysis for Baby Boomers...
    python prototype.py generate -p linkedin -a baby_boomers -t market_update --loan-officer "Leslie Chang" --company "CMG Mortgage"
    goto continue
)

if %choice%==7 (
    echo Choose platform for variations:
    echo 1. Instagram   2. Facebook   3. LinkedIn
    set /p platform_choice="Enter choice: "
    
    if !platform_choice!==1 (
        echo Generating 3 Instagram variations for millennials...
        python prototype.py variations -p instagram -a millennials -n 3
    ) else if !platform_choice!==2 (
        echo Generating 3 Facebook variations for Gen X...
        python prototype.py variations -p facebook -a gen_x -n 3
    ) else if !platform_choice!==3 (
        echo Generating 3 LinkedIn variations for Baby Boomers...
        python prototype.py variations -p linkedin -a baby_boomers -n 3
    )
    goto continue
)

if %choice%==8 (
    echo Current Mortgage Rate Data:
    python prototype.py rates
    goto continue
)

if %choice%==9 (
    echo Thank you for using the Leslie Chang - CMG Mortgage Content Generator!
    exit /b
)

echo Invalid choice. Please try again.
goto menu

:continue
echo.
echo ====================================
set /p again="Generate more content? (y/n): "
if /i %again%==y goto menu
echo Thank you for using the Leslie Chang - CMG Mortgage Content Generator!
pause