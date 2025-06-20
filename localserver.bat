@echo off
python -m http.server --directory public 8000
echo("")
echo("If you see errors, verify your python installation or install http.server")
pause