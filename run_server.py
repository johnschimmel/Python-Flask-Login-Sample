from app import app
from notes import notes_app
from auth import auth_flask_login

app.register_blueprint(notes_app)
app.register_blueprint(auth_flask_login)

if __name__ == "__main__":
	app.run()