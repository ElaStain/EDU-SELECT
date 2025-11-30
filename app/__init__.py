from flask import Flask

app = Flask(__name__)

# Importar blueprints
from app.routes.views import views_bp
from app.routes.api import api_bp

# Registrar blueprints
app.register_blueprint(views_bp)
app.register_blueprint(api_bp)