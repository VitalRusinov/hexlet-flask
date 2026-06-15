import os

from flask import Flask, abort, flash, get_flashed_messages, redirect, render_template, request, url_for
# import json
from dotenv import load_dotenv
from userRepository_db import UserRepository
from utils import validate_user
from datetime import timedelta

import atexit
import psycopg2

# Константы (начало)
# ----------------------------------------------------
USER_PATH = '/users'
# ----------------------------------------------------
# Константы (конец)

app = Flask(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=7)

def get_db_connection():
    """Создает и возвращает соединение с БД"""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    """Создает таблицы в базе данных, если их нет"""
    print("🔄 Проверяю и инициализирую базу данных...")

    conn = get_db_connection()
    cur = conn.cursor()

    # Читаем init.sql и выполняем его
    try:
        with open('init.sql', 'r') as f:
            sql = f.read()

        cur.execute(sql)
        conn.commit()
        print("✅ База данных инициализирована (таблицы созданы)")
    except Exception as e:
        print(f"⚠️ Ошибка при инициализации БД: {e}")
    finally:
        cur.close()
        conn.close()

# Инициализируем базу данных при старте приложения
with app.app_context():
    init_db()

# Создаем соединение для работы репозитория
conn = get_db_connection()
atexit.register(lambda: conn.close())

# Передаем соединение в репозиторий
repo = UserRepository(conn)

@app.get("/")
def home_index():
    app.logger.debug("Получен запрос к главной странице")
    return render_template(
        'layouts/layout.html',
    )

@app.get(f'{USER_PATH}')
def users_index():
    app.logger.debug("Получен запрос к странице с пользователями")
    query = request.args.get('query')

    if query is None:
        users = repo.get_all()
    else:
        users = repo.get_by_query(query)
    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'users/index.html',
        users = users,
        query = query,
        messages = messages
    )

@app.route(f'{USER_PATH}/<int:id>')
def users_show(id):
    user = repo.find(id)

    if not user:
        abort(404)

    return render_template("users/show.html", user=user)


# Создание новго пользователя
@app.post(f'{USER_PATH}')
def users_post():
    app.logger.info("Отправка данных нового пользователя")
    # извлекаем данные из формы
    user = request.form.to_dict()
    # валидируем данные
    errors = validate_user(user)

    if errors:
        app.logger.error("Данные пользователя не прошли валидацию")
        # flash("Ошибка при создании нового пользователя", "error")
        return render_template(
            "users/new.html",
            user=user,
            errors=errors,
        ), 422

    repo.add(user)

    flash(f"Новый пользователь {user['name']} создан", "success")
    return redirect(url_for('users_index'), code=302)

# Форма для редактирования данных пользователя
@app.route(f'{USER_PATH}/<int:id>/edit')
def user_edit(id):

    user = repo.find(id)
    if not user:
        abort(404)
    errors = {}

    return render_template(
        "users/edit.html",
        user=user,
        errors=errors,
    )

# Обновление данных пользователя
@app.route(f"{USER_PATH}/<int:id>/patch", methods=["POST"])
def users_update(id):
    app.logger.info(f"Обновление данных пользователя с id {id}")
    # извлекаем данные из формы
    new_user = request.form.to_dict()
    # валидируем данные
    errors = validate_user(new_user)

    if errors:
        app.logger.error("Данные пользователя не прошли валидацию")
        new_user['id'] = id
        return render_template(
            "users/edit.html",
            user=new_user,
            errors=errors,
        ), 422

    repo.update(id, new_user)

    return redirect(url_for('users_index'), code=302)

# Форма для создания нового пользователя
@app.route(f'{USER_PATH}/new')
def users_new():
    app.logger.info("Запрос формы для создания нового пользователя")
    user = {
        "name": "",
        "email": "",
    }
    errors = {}

    return render_template("users/new.html", user=user, errors=errors)

# Удаление пользователя
@app.route(f'{USER_PATH}/<int:id>/delete', methods=["POST"])
def users_delete(id):
    repo.delete(id)

    flash("User has been deleted", "success")
    return redirect(url_for("users_index"))

@app.errorhandler(404)
def not_found(error):
    return "Oops!", 404

