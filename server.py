# Импорт необходимых библиотек и их компонентов
from flask import Flask, request, render_template, redirect, abort, make_response, jsonify, send_file
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.worlds import WorldsForm
from forms.world_edit import WorldsEditForm
from data import db_session
from data.users import User
from data.worlds import Worlds
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os

# Инициализация приложения Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# Домашнаяя страница - просмотр всех опубликованных миров
@app.route("/")
def home():
    db_sess = db_session.create_session()
    worlds = db_sess.query(Worlds)
    return render_template("world_view.html", worlds=worlds)

# Личная страница пользователя с указанным ID
@app.route("/user/<int:id>")
def user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        return render_template("user_page.html", user=user)
    else:
        abort(404)

# Форма и обработка регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

# Форма и обработка авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

# Обработка деавторизации
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

# Форма и обработка публикации нового мира
@app.route('/new_world', methods=['GET', 'POST'])
@login_required
def new_world():
    form = WorldsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        world = Worlds()
        world.title = form.title.data
        world.description = form.description.data

        c = db_sess.query(Worlds).all()
        filename = str(c[-1].id + 1) if c else '1'
        form.file.data.save('files/' + filename + '.zip')
        
        current_user.worlds.append(world)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('worlds.html', title='Добавление мира',
                           form=form)

# Обработка запроса на повышение пользователя до уровня модератора
@app.route('/make_mod/<int:id>')
@login_required
def make_mod(id):
    if not current_user.mod:
        abort(403)    
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id,
                                      ).first()
    user.mod = True
    db_sess.commit()
    return redirect(f'/user/{id}')

# Форма и обработка изменения сведений о мире
@app.route('/edit_world/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_world(id):
    form = WorldsEditForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if not current_user.mod:
            world = db_sess.query(Worlds).filter(Worlds.id == id,
                                                 Worlds.owner == current_user
                                                 ).first()
        else:
            world = db_sess.query(Worlds).filter(Worlds.id == id,
                                                 ).first()            
        if world:
            form.title.data = world.title
            form.description.data = world.description
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not current_user.mod:
            world = db_sess.query(Worlds).filter(Worlds.id == id,
                                                 Worlds.owner == current_user
                                                 ).first()
        else:
            world = db_sess.query(Worlds).filter(Worlds.id == id,
                                                 ).first()  
        if world:
            world.title = form.title.data
            world.description = form.description.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('worldsedit.html',
                           title='Редактирование Мира',
                           form=form
                           )

# Обработка удаления мира с сервера
@app.route('/delete_world/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_world(id):
    db_sess = db_session.create_session()
    if not current_user.mod:
        world = db_sess.query(Worlds).filter(Worlds.id == id,
                                             Worlds.owner == current_user
                                             ).first()
    else:
        world = db_sess.query(Worlds).filter(Worlds.id == id,
                                             ).first()
    if world:
        db_sess.delete(world)
        path = 'files/' + str(world.id) + '.zip'
        if os.path.isfile(path):
            os.remove(path)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

# Обработка ошибки 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Обработка запроса о загрузке мира
@app.route("/download_world/<int:id>")
def download_world(id):
    db_sess = db_session.create_session()
    world = db_sess.query(Worlds).filter(Worlds.id == id
                                         ).first()
    if world and os.path.isfile('files/' + str(world.id) + '.zip'):
        name = world.title + '.zip'
        if True in map(lambda x: x in name, '/\*:?"<>') or len(name) >= 255:
            name = str(world.id)
        return send_file(open('files/' + str(world.id) + '.zip', mode='rb'),
                         attachment_filename=name, as_attachment=True,
                         cache_timeout=0)
    else:
        abort(404)

if __name__ == '__main__':
    db_session.global_init('db/hexaportal.db')
    app.run()

