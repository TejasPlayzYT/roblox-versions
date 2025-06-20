@echo off
start http://localhost:8000
python -m http.server --directory public 8000
echo("")
echo("If you see errors, verify your python installation or install http.server")
pause