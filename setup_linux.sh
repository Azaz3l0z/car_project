#!/bin/bash
cd resources
mkdir python/env
python3 -m venv python/env
chmod +x python/env/bin/activate
source python/env/bin/activate
pip install -r python/requirements.txt

# Create run executable
cd python
pyinstaller --onefile --nowindow run.py
rm -r build
rm run.spec
mv dist/* .
rm -r dist
rm -r __pycache__
rm -r env
cd ..

# Create updater
cd python
pyinstaller --onefile --nowindow updater.py
rm -r build
rm updater.spec
mv dist/updater .
rm -r dist
rm -r __pycache__
cd ..
