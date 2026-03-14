from wtforms import DateField, Form, HiddenField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, Length, NumberRange


class ClienteForm(Form):
    nombre_completo = StringField(
        "Nombre completo",
        validators=[DataRequired(message="El nombre es obligatorio"), Length(min=3, max=120)],
    )
    direccion = StringField(
        "Direccion",
        validators=[DataRequired(message="La direccion es obligatoria"), Length(min=5, max=200)],
    )
    telefono = StringField(
        "Telefono",
        validators=[DataRequired(message="El telefono es obligatorio"), Length(min=8, max=10)],
    )
    fecha_pedido = DateField("Fecha del pedido", format="%Y-%m-%d", validators=[DataRequired()])


class PizzaForm(Form):
    tamano = SelectField(
        "Tamano",
        choices=[("chica", "Chica"), ("mediana", "Mediana"), ("grande", "Grande")],
        validators=[DataRequired()],
    )
    ingredientes = StringField(
        "Ingredientes",
        validators=[DataRequired(message="Escribe al menos un ingrediente"), Length(min=3, max=200)],
    )
    cantidad = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=1, max=50)])


class QuitarDetalleForm(Form):
    indice = HiddenField(validators=[DataRequired()])
