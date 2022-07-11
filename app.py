from crypt import methods
from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '12345'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    """Displays list of all current pets"""
    pets = Pet.query.all()
    return render_template("list.html", pets=pets)


@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Handles the submission of the AddPetForm and returns the empty form if none
    is submitted"""
    form = AddPetForm()

    if form.validate_on_submit():
        data = {d: v for d, v in form.data.items() if d != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        return redirect("/")

    else:
        return render_template("add_form.html", form=form)


@app.route('/<int:pet_id>', methods=["GET", "POST"])
def edit_pet(pet_id):
    """ Handles the submission of the EditPetForm and returns the empty form if 
    none is submitted"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        return redirect("/")

    else:
        return render_template("edit_form.html", form=form, pet=pet)
