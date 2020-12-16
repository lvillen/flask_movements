from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length


class MovementForm(FlaskForm):
    #id = IntegerField('id') Este campo en realidad no lo uso nunca, en modifica.html puedo meter el parámetro a mano fácilmente
    fecha = DateField('Fecha', validators=[DataRequired()])
    concepto = StringField('Concepto', validators=[DataRequired(), Length(min=10, message='10 car. min.')])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])

    submit = SubmitField('Aceptar')