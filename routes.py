from flask import Flask, render_template, request
from forms import SignupForm

app = Flask(__name__)

app.secret_key = "development-key"

@app.route("/", methods=['GET','POST'])
def login():
	form = SignupForm();

	if request.method == 'POST':
		return "success!"
		
	else:
		return render_template("login.html", form=form)

if __name__ == "__main__":
	app.run(debug=True)