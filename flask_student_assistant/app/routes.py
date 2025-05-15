from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import User, Task, Event, Note, Grade, Notification
from app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('menu'))
        else:
            flash('Usuario o contraseña incorrectos.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso. Ya puedes iniciar sesión.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

from app.models import Task
from app.forms import TaskForm
from datetime import datetime

@app.route('/tareas')
@login_required
def tareas():
    tareas = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all()
    return render_template('tareas.html', tareas=tareas)

@app.route('/tarea/nueva', methods=['GET', 'POST'])
@login_required
def nueva_tarea():
    form = TaskForm()
    if form.validate_on_submit():
        nueva = Task(
            title=form.title.data,
            due_date=form.due_date.data,
            user_id=current_user.id
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Tarea agregada con éxito.')
        return redirect(url_for('tareas'))
    return render_template('nueva_tarea.html', form=form)

@app.route('/tarea/<int:id>/completar')
@login_required
def completar_tarea(id):
    tarea = Task.query.get_or_404(id)
    if tarea.user_id != current_user.id:
        return redirect(url_for('tareas'))
    tarea.completed = not tarea.completed
    db.session.commit()
    return redirect(url_for('tareas'))

@app.route('/tarea/<int:id>/eliminar')
@login_required
def eliminar_tarea(id):
    tarea = Task.query.get_or_404(id)
    if tarea.user_id != current_user.id:
        return redirect(url_for('tareas'))
    db.session.delete(tarea)
    db.session.commit()
    flash('Tarea eliminada.')
    return redirect(url_for('tareas'))

from app.models import Event
from app.forms import EventForm

@app.route('/eventos')
@login_required
def eventos():
    eventos = Event.query.filter_by(user_id=current_user.id).order_by(Event.date).all()
    return render_template('eventos.html', eventos=eventos)

@app.route('/evento/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_evento():
    form = EventForm()
    if form.validate_on_submit():
        nuevo = Event(
            title=form.title.data,
            date=form.date.data,
            user_id=current_user.id
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Evento guardado correctamente.')
        return redirect(url_for('eventos'))
    return render_template('nuevo_evento.html', form=form)

@app.route('/evento/<int:id>/eliminar')
@login_required
def eliminar_evento(id):
    evento = Event.query.get_or_404(id)
    if evento.user_id != current_user.id:
        return redirect(url_for('eventos'))
    db.session.delete(evento)
    db.session.commit()
    flash('Evento eliminado.')
    return redirect(url_for('eventos'))

from app.models import Note
from app.forms import NoteForm

@app.route('/notas')
@login_required
def notas():
    notas = Note.query.filter_by(user_id=current_user.id).order_by(Note.date_created.desc()).all()
    return render_template('notas.html', notas=notas)

@app.route('/nota/nueva', methods=['GET', 'POST'])
@login_required
def nueva_nota():
    form = NoteForm()
    if form.validate_on_submit():
        nueva = Note(
            content=form.content.data,
            tag=form.tag.data,
            user_id=current_user.id
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Nota guardada con éxito.')
        return redirect(url_for('notas'))
    return render_template('nueva_nota.html', form=form)

@app.route('/nota/<int:id>/eliminar')
@login_required
def eliminar_nota(id):
    nota = Note.query.get_or_404(id)
    if nota.user_id != current_user.id:
        return redirect(url_for('notas'))
    db.session.delete(nota)
    db.session.commit()
    flash('Nota eliminada.')
    return redirect(url_for('notas'))

from app.models import Grade
from app.forms import GradeForm
from sqlalchemy import func

@app.route('/estadisticas', methods=['GET', 'POST'])
@login_required
def estadisticas():
    form = GradeForm()
    if form.validate_on_submit():
        nueva = Grade(
            subject=form.subject.data,
            score=float(form.score.data),
            user_id=current_user.id
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Calificación registrada.')
        return redirect(url_for('estadisticas'))

    # Obtener calificaciones
    calificaciones = Grade.query.filter_by(user_id=current_user.id).all()

    # Calcular promedios
    promedio_general = (
        db.session.query(func.avg(Grade.score))
        .filter_by(user_id=current_user.id)
        .scalar()
    )

    promedio_por_materia = (
        db.session.query(Grade.subject, func.avg(Grade.score))
        .filter_by(user_id=current_user.id)
        .group_by(Grade.subject)
        .all()
    )

    return render_template(
        'estadisticas.html',
        form=form,
        promedio_general=promedio_general,
        promedio_por_materia=promedio_por_materia,
        calificaciones=calificaciones
    )

from app.models import Notification
from app.forms import NotificationForm
from datetime import datetime

@app.route('/notificaciones', methods=['GET', 'POST'])
@login_required
def notificaciones():
    form = NotificationForm()
    if form.validate_on_submit():
        nueva = Notification(
            message=form.message.data,
            notify_at=form.notify_at.data,
            user_id=current_user.id
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Notificación programada.')
        return redirect(url_for('notificaciones'))

    # Mostrar notificaciones futuras ordenadas
    notificaciones = Notification.query.filter(
        Notification.user_id == current_user.id,
        Notification.notify_at >= datetime.utcnow()
    ).order_by(Notification.notify_at).all()

    return render_template('notificaciones.html', form=form, notificaciones=notificaciones)

@app.route('/notificacion/<int:id>/eliminar')
@login_required
def eliminar_notificacion(id):
    notif = Notification.query.get_or_404(id)
    if notif.user_id != current_user.id:
        return redirect(url_for('notificaciones'))
    db.session.delete(notif)
    db.session.commit()
    flash('Notificación eliminada.')
    return redirect(url_for('notificaciones'))

from app.forms import SearchForm

import openai
import os
from flask import request, jsonify

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/buscador', methods=['GET', 'POST'])
@login_required
def buscador():
    respuesta = ""
    if request.method == 'POST':
        pregunta = request.form.get('pregunta')

        # Extrae datos reales del usuario
        tareas = Task.query.filter_by(user_id=current_user.id, completed=False).all()
        eventos = Event.query.filter_by(user_id=current_user.id).all()
        notas = Note.query.filter_by(user_id=current_user.id).all()

        contexto = f"""
        Usuario: {current_user.username}
        Tareas pendientes:
        {', '.join([t.title for t in tareas])}

        Eventos:
        {', '.join([f"{e.title} el {e.date.strftime('%d/%m/%Y')}" for e in eventos])}

        Notas:
        {', '.join([n.content for n in notas])}
        """

        prompt = f"""
        CONTEXTO:
        {contexto}

        PREGUNTA DEL USUARIO:
        {pregunta}

        RESPONDE:
        """

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente escolar que responde en español de manera clara y directa."},
                    {"role": "user", "content": prompt}
                ]
            )
            respuesta = completion.choices[0].message.content.strip()
        except Exception as e:
            respuesta = "Ocurrió un error con la IA: " + str(e)

    return render_template('buscador.html', respuesta=respuesta)

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

@app.route("/asistente", methods=["GET", "POST"])
@login_required
def asistente():
    respuesta = ""
    if request.method == "POST":
        pregunta = request.form["pregunta"]
        try:
            result = model.generate_content(pregunta)
            respuesta = result.text
        except Exception as e:
            respuesta = f"Ocurrió un error con la IA: {e}"
    return render_template("asistente.html", respuesta=respuesta)
