cd resources
mkdir python/env
python -m venv python/env
python/env/Scripts/python3.exe
pip install -r python/requirements.txt

:: Executable run
cd python
pyinstaller --onefile --nowindow run.py
rmdir /s build
del run.spec
move "dist/run.exe" .
rmdir /s dist
rmdir /s __pycache__
rmdir /s env
cd ..

:: Executable updater
cd updater
pyinstaller --onefile --nowindow updater.py
rmdir /s build
del updater.spec
move "dist/updater.exe" .
rmdir /s dist
rmdir /s __pycache__
rmdir /s env
cd ..

