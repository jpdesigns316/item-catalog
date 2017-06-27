from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField, HiddenField
from wtforms.validators import DataRequired, Required


class BookForm(FlaskForm):
    book_title = StringField('Title', validators=[DataRequired()])
    book_author = StringField('Author', validators=[DataRequired()])
    book_description = TextAreaField(
        'Review', validators=[DataRequired()])
    language_id = IntegerField('Language')
    book_img = FileField('Image', validators=[DataRequired()])
    user_id = HiddenField('User Id')
