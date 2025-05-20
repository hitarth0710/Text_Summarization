from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, URL, Optional, NumberRange
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SummarizationForm(FlaskForm):
    url = URLField('Article URL', validators=[Optional(), URL()])
    text = TextAreaField('Article Text', validators=[Optional(), Length(min=100, max=50000)])
    title = StringField('Title (optional)', validators=[Optional(), Length(max=200)])
    min_length = IntegerField('Min Length', validators=[
        NumberRange(min=30, max=200, message='Min length must be between 30-200')
    ], default=50)
    max_length = IntegerField('Max Length', validators=[
        NumberRange(min=50, max=500, message='Max length must be between 50-500')
    ], default=150)
    save_summary = BooleanField('Save Summary to History', default=True)
    submit = SubmitField('Summarize')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        # Check that either URL or text is provided
        if not self.url.data and not self.text.data:
            self.url.errors.append('Please enter either a URL or text to summarize')
            self.text.errors.append('Please enter either a URL or text to summarize')
            return False

        # Check that min_length is less than max_length
        if self.min_length.data >= self.max_length.data:
            self.min_length.errors.append('Minimum length must be less than maximum length')
            return False

        return True