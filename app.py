from flask import Flask, render_template
from flask_migrate import Migrate

from config import DevelopmentConfig
from models import db
from pedidos import pedidos_bp
from reportes import reportes_bp


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(pedidos_bp, url_prefix="/pedidos")
app.register_blueprint(reportes_bp, url_prefix="/reportes")


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
