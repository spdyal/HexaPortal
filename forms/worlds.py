from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


class WorldsForm(FlaskForm):
    title = StringField('Название мира', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    file = FileField('Файл', validators=[FileRequired(),
                                         FileAllowed(['zip'], 'Zip only!')])
    submit = SubmitField('Подтвердить')
 