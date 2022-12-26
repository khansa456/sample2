from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
#from flask_wtf.file import FileField, FileRequired, FileAllowed
#have to install (pip install Flask-WTF)


class CreateProductForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    category = SelectField('Category', [validators.DataRequired()],
                           choices=[("", 'Select'), ('F', 'Food'), ('D', 'Drinks'), ('C', 'Clothes')], default='')
    price = StringField('Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    rating = RadioField('Rating', choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')], default='5')
    picture = TextAreaField('Picture', [validators.Optional()])
    #picture = FileField('Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'Images only!'])])
