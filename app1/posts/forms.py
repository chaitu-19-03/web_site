from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class post_form(FlaskForm):
    title = StringField('title',validators=[DataRequired()])
    content = TextAreaField('content',validators=[DataRequired()])
    submit = SubmitField('add_content')
