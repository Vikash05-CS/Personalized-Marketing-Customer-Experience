# PowerShell script to install dependencies and run the Flask app

Set-Location -Path $PSScriptRoot

pip install -r requirements.txt
python app.py
