import os
from flask import Flask, render_template, request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user,current_user
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func




app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mykey'

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "login"


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')




@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully', category='success')
                login_user(user,remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect',category='error')
        else:
            flash('Email does not exist.',category='error')
    
    return render_template("login.html", user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup',  methods=["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif password1!=password2:
            flash('password not match',category='error')
        elif len(password1)<4:
            flash('password must be greater than 4 character',category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created',category='success')
            return redirect(url_for('home'))
    return render_template("signup.html", user=current_user)

@app.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note)<1:
            flash('Add something!', category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added succesfully ',category='success')
    return render_template("home.html", user=current_user)

@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.filter_by(id=id).first()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        note =request.form.get('note')
        note = Note.query.filter_by(id=id).first()
        note.data=note
        db.session.add(note)
        db.session.commit()
        return redirect('/')
    note = Note.query.filter_by(id=id).first()
    return render_template('update.html',note=note,user=current_user)



if __name__ == '__main__':
    app.run(debug=True)


    