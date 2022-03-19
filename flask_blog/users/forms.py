from flask import flash
from flask_blog import mongo
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
import re


class SignupForm(FlaskForm):
    fname = StringField("Your first name",
                        validators=[Length(min=2, max=15), DataRequired()],
                        render_kw={"placeholder": "John"})
    lname = StringField("Your last name",
                        validators=[Length(min=2, max=15), DataRequired()],
                        render_kw={"placeholder": "Doe"})
    email = StringField("Your email",
                        validators=[Email(), Length(max=50), DataRequired()],
                        render_kw={"placeholder": "john.doe@email.com"})
    confirm_email = StringField("Confirm your email",
                                validators=[Email(),
                                            DataRequired(),
                                            EqualTo("email")],
                                render_kw={"placeholder": "john.doe@email.com"})
    password = PasswordField("Your password",
                             validators=[DataRequired(),
                                         Length(min=6, max=40)],
                             render_kw={"placeholder": "••••••••"})
    confirm_password = PasswordField("Confirm your password",
                                     validators=[DataRequired(),
                                                 EqualTo("password")],
                                     render_kw={"placeholder": "••••••••"})
    submit = SubmitField("Create your account")
    
    def validate_fname(slef, fname):
        value = fname.data
        match_regex = re.compile("^[A-Za-z]+$")
        result = re.search(match_regex, value)
        if value.replace(" ", "") != "":
            if not result:
                raise ValidationError("Your first name must only contains letters")
            
    def validate_lname(slef, lname):
        value = lname.data
        match_regex = re.compile("^[A-Za-z]+$")
        result = re.search(match_regex, value)
        if value.replace(" ", "") != "":
            if not result:
                raise ValidationError("Your last name must only contains letters")

    def validate_email(self, email):
        user = mongo.db.users.find_one({"email": email.data})
        if user:
            raise ValidationError(
                'This email already exists in our database.')

    def validate_password(self, password):
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,40}$"
        match_regex = re.compile(regex)
        result = re.search(match_regex, password.data)
        if not result:
            raise ValidationError(
                'Password must have at least 1 capital letter, 1 number, 1 special character and must be 6-40 characters long. Can NOT contain any white space')


class LoginForm(FlaskForm):
    email = StringField("Your email",
                        validators=[DataRequired(), Email(), Length(max=50)],
                        render_kw={"placeholder": "john.doe@email.com"})
    remember = BooleanField("Remember me")
    password = PasswordField("Your password",
                             validators=[DataRequired(),
                                         Length(min=6, max=40)],
                             render_kw={"placeholder": "••••••••"})
    submit = SubmitField("Login to your account")

    def validate_email(self, email):
        user = mongo.db.users.find_one({"email": email.data})
        if not user:
            flash("Wrong email and/or password", "flash-danger")


class SettingsForm(FlaskForm):
    profile_pic = FileField("Update your avatar",
                            validators=[FileAllowed(["jpg", "jpeg", "png"])])
    username = StringField("Change your username")
    fname = StringField("Change your first name")
    lname = StringField("Change your Last name")
    password = PasswordField("Your password",
                             render_kw={"placeholder": "••••••••"})
    confirm_password = PasswordField("Confirm your password",
                                     render_kw={"placeholder": "••••••••"}, 
                                     validators=[EqualTo("password")])
    settingsSubmit = SubmitField("Update profile")

    def validate_username(slef, username):
        value = username.data.replace(" ", "")
        match_regex = re.compile("^[A-Za-z0-9]+$")
        result = re.search(match_regex, value)
        
        if value.replace(" ", "") != "":
            existing_user = mongo.db.users.find_one({"username": value})
            if " " in username.data:
                raise ValidationError(
                    'Your username can NOT have any white space')
            if existing_user and existing_user["username"] != current_user["username"]:
                raise ValidationError(
                    'This username is already taken')
            if len(value) < 2 or len(value) > 15:
                raise ValidationError(
                    'Your username must have between 2 and 15 characters')
            if not result:
                raise ValidationError("Your username must only contains letters and/or numbers")

    def validate_fname(slef, fname):
        value = fname.data
        match_regex = re.compile("^[A-Za-z\s]+$")
        result = re.search(match_regex, value)
        if value.replace(" ", "") != "":
            if len(value) < 2 or len(value) > 15:
                raise ValidationError(
                    'Your first name must have between 2 and 15 characters')
            if not result:
                raise ValidationError("Your first name must only contains letters")

    def validate_lname(slef, lname):
        value = lname.data
        match_regex = re.compile("^[A-Za-z]+$")
        result = re.search(match_regex, value)
        if value.replace(" ", "") != "":
            if len(value) < 2 or len(value) > 15:
                raise ValidationError(
                    'Your last name must have between 2 and 15 characters')
            if not result:
                raise ValidationError("Your last name must only contains letters")

    def validate_password(self, password): 
        value = password.data 
        match_regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,40}$")
        result = re.search(match_regex, value)
        if value != "":
            if not result:
                raise ValidationError(
                'Password must have at least 1 capital letter, 1 number, 1 special character and must be 6-40 characters long. Can NOT contain any white space')
    
    def validate_profile_pic(self, profile_pic):
        max_bytes = 2*1024*1024
        if len(profile_pic.data.read()) > max_bytes:
            raise ValidationError(f"File size must be less than 2MB")