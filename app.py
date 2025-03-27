import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from models import db, Annuncio, Utente  # Ensure these are defined in models.py

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db.init_app(app)


with app.app_context():
   
    db.create_all()

@app.route("/", endpoint='index')
def index():
    annunci = Annuncio.query.all()
    return render_template("index.html", annunci=annunci)

@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/Login.html", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Utente.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            flash("Logged in successfully.")
            return redirect(url_for("utente"))
        else:
            flash("Invalid credentials.")
    return render_template("Login.html")

@app.route("/register.html", methods=["GET", "POST"], endpoint="register")
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # Simple validation; extend as needed
        if Utente.query.filter_by(username=username).first():
            flash("Username already exists.")
        else:
            new_user = Utente(username=username, email=email)  # Pass email during creation
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registered successfully. Please log in.")
            return redirect(url_for("login"))
    return render_template("Register.html")

@app.route("/Annuncio.html", methods=["GET"], endpoint="annuncio")
def annuncio_form():
    # Render the form to post a new listing
    return render_template("Annuncio.html")

@app.route("/add_listing", methods=["POST"])
def add_listing():
    if "user_id" not in session:
        flash("Please log in to post an item.")
        return redirect(url_for("login"))
        
    title = request.form.get("title")
    desc = request.form.get("desc")
    is_cat = request.form.get("is_cat") == "1"  # Checkbox returns '1' when checked
    image = request.files.get("image")
    
    filename = None
    if image and image.filename:
        filename = secure_filename(image.filename)
        upload_folder = app.config["UPLOAD_FOLDER"]
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        image.save(os.path.join(upload_folder, filename))
    
    new_annuncio = Annuncio(
        title=title,
        desc=desc,
        image_filename=filename,
        is_cat=is_cat,
        user_id=session.get("user_id")
    )
    db.session.add(new_annuncio)
    db.session.commit()
    flash("Listing added successfully.")
    return redirect(url_for("index"))

@app.route("/dogs", endpoint="dogs")
def dogs():
    # Use 0 for dogs listings since is_cat is 0 (false) for dogs
    dogs_annunci = Annuncio.query.filter_by(is_cat=0).all()
    return render_template("dogs.html", annunci=dogs_annunci)

@app.route("/cats", endpoint="cats")
def cats():
    cats_annunci = Annuncio.query.filter_by(is_cat=True).all()
    return render_template("cats.html", annunci=cats_annunci)

@app.route("/utente", endpoint="utente")
def utente():
    if "user_id" not in session:
        flash("Please log in to view your profile.")
        return redirect(url_for("login"))
        
    user = Utente.query.get(session["user_id"])
    if not user:
        flash("User not found.")
        return redirect(url_for("login"))
        
    return render_template("utente.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)