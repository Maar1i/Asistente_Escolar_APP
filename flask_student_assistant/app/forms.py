from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

from wtforms import StringField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

# ... LoginForm y RegisterForm ya existen

class TaskForm(FlaskForm):
    title = StringField('Título de la tarea', validators=[DataRequired()])
    due_date = DateField('Fecha de entrega', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Guardar tarea')

class EventForm(FlaskForm):
    title = StringField('Título del evento', validators=[DataRequired()])
    date = DateField('Fecha del evento', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Guardar evento')

class NoteForm(FlaskForm):
    content = StringField('Contenido de la nota', validators=[DataRequired()])
    tag = StringField('Etiqueta o materia (opcional)')
    submit = SubmitField('Guardar nota')


class GradeForm(FlaskForm):
    subject = StringField('Materia', validators=[DataRequired()])
    score = StringField('Calificación (0-10)', validators=[DataRequired()])
    submit = SubmitField('Agregar calificación')

from wtforms.fields import DateTimeLocalField

class NotificationForm(FlaskForm):
    message = StringField('Mensaje', validators=[DataRequired()])
    notify_at = DateTimeLocalField('Fecha y hora de notificación', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Guardar notificación')

class SearchForm(FlaskForm):
    query = StringField('¿En qué te puedo ayudar?', validators=[DataRequired()])
    submit = SubmitField('Buscar')
