#!/bin/bash
cd resources
# Create run executable
cd python

mkdir env
python3 -m venv env
chmod +x env/bin/activate
source env/bin/activate
pip install -r requirements.txt

pyinstaller --onefile --nowindow --name "run.sh" run.py
rm -r build
rm run.sh.spec
mv dist/* .
rm -r dist
rm -r __pycache__
deactivate
rm -r env
cd ..

# Create updater
cd updater

mkdir env
python3 -m venv env
chmod +x env/bin/activate
source env/bin/activate
pip install -r requirements.txt

pyinstaller --onefile --nowindow --name "updater.sh" updater.py
rm -r build
rm updater.sh.spec
mv dist/* .
rm -r dist
rm -r __pycache__
deactivate
rm -r env
cd ..
