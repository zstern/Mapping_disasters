from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Required
from flask_wtf.file import FileField, FileRequired

# Address entry form
class AddressForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit Address')


# Photo entry form (file selector)
class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit Photo')


class SurveyForm(FlaskForm):
    dropdown = SelectField(u'Select Test', choices = [('Damaged', 'Damaged'), ('Undamaged', 'Undamaged')], validators = [DataRequired()])

    singletext = StringField('Test')

    multiple = SelectMultipleField(choices = [('Fire', 'Fire'), ('Flood', 'Flood')])

    submit = SubmitField('Submit Damage Form')
