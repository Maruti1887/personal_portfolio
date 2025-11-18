from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # change this for production

# ---------------- DATABASE CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Contact Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

# ---------------- EMAIL CONFIG ----------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "naikgundanna@gmail.com"   # replace with your email
app.config["MAIL_PASSWORD"] = "yaaa vryv ifqq mahb"      # use app password for Gmail
app.config["MAIL_DEFAULT_SENDER"] = "your_email@gmail.com"
mail = Mail(app)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html", title="Home")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/projects")
def projects():
    return render_template("projects.html", title="Projects")

@app.route("/experience")
def experience():
    return render_template("experience.html", title="Experience")

@app.route('/certification')
def certification():
    return render_template('certification.html', title="Certification")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Save to Database
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        # Send Email
        try:
            msg = Message("📩 New Contact from Portfolio",
                          recipients=["naikgundanna@gmail.com"])  # <-- change to your email
            msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            mail.send(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            print("Email error:", e)
            flash("Message saved but email not sent.", "warning")

        return redirect(url_for("contact"))

    return render_template("contact.html", title="Contact")

@app.route("/resume")
def resume():
    return send_from_directory(".", "resume.pdf")

# ---------------- INIT DB ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
