from flask import Blueprint, render_template, request, jsonify

login = Blueprint("login", __name__, template_folder="templates")

@login.route('/')
def home():
    'hello login!'
    return render_template('login.html')