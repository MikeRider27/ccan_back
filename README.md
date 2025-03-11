# Readiness Backend

## Requirements

- Python 3.8+ 
- Git
- Instant Cli - Oracle

## Setup

If you're using and IDE (vscode, Pycharm, etc.) please consult your ide instructions to setup and start the server

These instructions asume you have `virtualenv` installed in your python libraries

### Install dependencies

#### Linux

```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

#### Windows

```cmd
virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Usage 

Once the correct virtual environment is activated start the `app.py` script

```bash
python app.py
```

## Translations
Generate template of messages
```bash
pybabel extract -F babel.cfg -o translations/messages.pot app.py
```
Create specific files for language
```bash
pybabel init -i translations/messages.pot -d translations -l es
pybabel init -i translations/messages.pot -d translations -l en
```
Compile changes of files
```bash
pybabel compile -d translations  
```