from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ← Esto soluciona CORS

# Importar blueprints
from app.routes.views import views_bp
from app.routes.api import api_bp

# Registrar blueprints
app.register_blueprint(views_bp)
app.register_blueprint(api_bp)