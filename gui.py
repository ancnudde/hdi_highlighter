#gui.py

from flaskwebgui import FlaskUI
from highlighter import app

FlaskUI(app, width=1000, height=800).run()
