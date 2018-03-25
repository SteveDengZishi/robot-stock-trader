from flask import Flask, render_template
from forms import SignupForm

app = Flask(__name__)

app.secret_key = "development-key"

@app.route("/")
def login():
	form = SignupForm();
	return render_template("login.html", form=form)

if __name__ == "__main__":
	app.run(debug=True)