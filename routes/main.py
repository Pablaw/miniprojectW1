from flask import Blueprint, render_template, request, jsonify
from db import db

main = Blueprint("main", __name__, template_folder="templates")

