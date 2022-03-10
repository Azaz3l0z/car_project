cd resources

:: Executable run
cd python
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
pyinstaller --onefile --nowindow run.py

rmdir /Q /s build
del run.spec
move "dist\run.exe" .
rmdir /Q /s dist
rmdir /Q /s __pycache__
call deactivate
rmdir /Q /s env
cd ..

:: Executable updater
cd updater
python -m venv env
call env\Scripts\activate.bat
pip install -r requirements.txt
pyinstaller --onefile --nowindow updater.py

rmdir /Q /s build
del updater.spec
move "dist\updater.exe" .
rmdir /Q /s dist
rmdir /Q /s __pycache__
call deactivate
rmdir /Q /s env
cd ..

cd ..
