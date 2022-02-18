from flask_blog import mongo
from model.pymongo_model import SimpleModel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, TextAreaField
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
                'Password must have at least 1 capital letter, 1 number, 1 special character and must be 6-40 characters long.')


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

    # def validate_email(self, email):
    #     check if email exists in DB

    # def validate_password(self, password):
    #     check if password match with DB using email
