@echo off

call %~dp0pythonProject\venv\Scripts\activate

cd %~dp0pythonProject

set TOKEN=5636728056:AAEujHHf2xu0ITfqB1zxYgpktUAWHCw2QKw

python main.py

pause