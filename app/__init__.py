from flask import Flask, request, redirect, abort, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object()
    db.init_app(app)

    return app
