from aquaritrack.extensions import app, db
from aquaritrack.main.routes import main
from aquaritrack.auth.routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
