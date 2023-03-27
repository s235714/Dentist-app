import os
from flask import Flask
from pony.orm import *
from flask_login import LoginManager
from pony.flask import Pony

app = Flask(__name__)
Pony(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db = Database()
from ProjInzynierski import routes
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.Osoba.get(osoba_id=user_id)