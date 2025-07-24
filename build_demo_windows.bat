set PYTHONOPTIMIZE=2
uv run pyinstaller demo.py `
    --onefile `
    --add-data="static;static" `
    -i="static\logo\logo.ico"
start dist
