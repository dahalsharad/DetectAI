# DetectAI
DetectAI is a modular tool that uses state of the art techniques to identify ai generated text and deepfake images.
## HOW TO Install ? 👷

# BACKEND
Download and install Python 3.10 from: https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe

It is recommended to run it in a virtual environment, Following steps also assume the same.
```terminal
git clone https://github.com/dahalsharad/DetectAI.git
cd DetectAI
py -3.10 -m venv venv_py310 #if py not available: python -m venv venv_py310
venv_py310\Scripts\activate
python -m pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
python manage.py runserver # The backend server will start at http://127.0.0.1:8000/.
```

# FRONTEND
```terminal
cd frontend
npm install
npm start
```
