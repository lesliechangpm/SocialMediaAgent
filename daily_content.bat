@echo off
echo ========================================
echo Leslie Chang - CMG Mortgage
echo Daily Content Package Generator
echo ========================================
echo.

echo Fetching current mortgage rates...
python prototype.py rates
echo.

echo Generating today's content package...
echo.

echo [1/3] Instagram Post (Millennials - Educational)
echo ================================================
python prototype.py generate -p instagram -a millennials -t educational --loan-officer "Leslie Chang" --company "CMG Mortgage" --save instagram_daily.json
echo.

echo [2/3] Facebook Post (Gen X - Market Update) 
echo ============================================
python prototype.py generate -p facebook -a gen_x -t market_update --loan-officer "Leslie Chang" --company "CMG Mortgage" --save facebook_daily.json
echo.

echo [3/3] LinkedIn Post (Baby Boomers - Professional)
echo =================================================
python prototype.py generate -p linkedin -a baby_boomers -t promotional --loan-officer "Leslie Chang" --company "CMG Mortgage" --save linkedin_daily.json
echo.

echo ========================================
echo Daily Content Package Complete!
echo ========================================
echo Content saved to:
echo - instagram_daily.json
echo - facebook_daily.json  
echo - linkedin_daily.json
echo.
echo Ready to copy and paste to your social media platforms!
echo.
pause