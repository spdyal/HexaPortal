from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class WorldsEditForm(FlaskForm):
    title = StringField('Название мира', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])

    submit = SubmitField('Подтвердить')
 