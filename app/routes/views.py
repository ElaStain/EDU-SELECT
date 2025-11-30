from flask import Blueprint, render_template

# Crear Blueprint
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/admin')
def admin():
    return render_template('admin.html')