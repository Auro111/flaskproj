# models.py

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy (this will be used in your Flask app)
db = SQLAlchemy()

class Utente(db.Model):
    __tablename__ = 'utenti'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    psswd = db.Column(db.String(150), nullable=False)  # DO NOT USE HASHING for this assignment
    
    # Relationships for saved announcements
    saved_cats = db.relationship('SavedCat', back_populates='utente', cascade="all, delete-orphan")
    saved_dogs = db.relationship('SavedDog', back_populates='utente', cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.psswd = password

    def check_password(self, password):
        return self.psswd == password
    
    def __repr__(self):
        return f"<Utente {self.username}>"

class Annuncio(db.Model):
    __tablename__ = 'annunci'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(150), nullable=True)  # Field to store the image path
    is_cat = db.Column(db.Integer, nullable=False, default=0)  # 1 if is_cat flag is set, 0 otherwise
    is_dog = db.Column(db.Integer, nullable=False, default=0)  # 1 if is_dog flag is set, 0 otherwise
    user_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=True)  # Stores the id of the user

    # Optional: relationship for easier access to the user object 
    user = db.relationship('Utente', backref='annunci')

    def __repr__(self):
        return f"<Annuncio {self.title}>"

class SavedCat(db.Model):
    __tablename__ = 'saved_cat'
    
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)
    annuncio_id = db.Column(db.Integer, db.ForeignKey('annunci.id'), nullable=False)
    
    # Define relationships
    utente = db.relationship('Utente', back_populates='saved_cats')
    annuncio = db.relationship('Annuncio')
    
    def __repr__(self):
        return f"<SavedCat User:{self.utente_id} Annuncio:{self.annuncio_id}>"

class SavedDog(db.Model):
    __tablename__ = 'saved_dog'
    
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)
    annuncio_id = db.Column(db.Integer, db.ForeignKey('annunci.id'), nullable=False)
    
    # Define relationships
    utente = db.relationship('Utente', back_populates='saved_dogs')
    annuncio = db.relationship('Annuncio')
    
    def __repr__(self):
        return f"<SavedDog User:{self.utente_id} Annuncio:{self.annuncio_id}>"
