from app import app
from classnotesdisplay import class_pages
from admin import admin_pages
from auth import auth_flask_login

app.register_blueprint(class_pages)
app.register_blueprint(admin_pages, url_prefix='/admin')
app.register_blueprint(auth_flask_login)

if __name__ == "__main__":
	app.run()