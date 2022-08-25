from app import create_app
from flask_cors import CORS, cross_origin

app = create_app()
CORS(app)
app.app_context().push()