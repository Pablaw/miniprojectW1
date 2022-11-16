from flask import Blueprint, render_template, request, jsonify

sign_up = Blueprint("sign_up", __name__, template_folder="templates")

@sign_up.route('/')
def home():
    'hello sign_up!'
    return render_template('sign_up.html')