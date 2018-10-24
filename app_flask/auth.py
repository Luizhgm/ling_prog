import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cpf = request.form["CPF"]
        tipo = request.form['options']
        
        db = get_db()
        error = None
        
        user_infos_id = db.execute(
            'SELECT id FROM user_infos WHERE CPF = ?', (cpf,)
        ).fetchone()['id']
        
        if db.execute(
            'SELECT id FROM account WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        elif user_infos_id is None:
            error = 'CPF {} is not already registered.'.format(cpf)
            
        if error is None:
            if tipo=="1" or tipo =="2":
                activate=False;
            else:
                activate=True;
            db.execute(
                'INSERT INTO account (username, password,options_id,activate, user_id) VALUES (?, ?, ?, ?, ?)',
                (username, generate_password_hash(password), tipo, activate, user_infos_id)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    db = get_db()   
    row = [(item[0],item[1]) for item in db.execute("SELECT id,type FROM options_user").fetchall()]
    
    return render_template('auth/register.html', options=row)

@bp.route('/register_user', methods=('GET', 'POST'))
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        place_id = request.form['place']
        email = request.form['email']
        CPF = request.form['CPF']
        
        db = get_db()
        error = None
        
        
        if db.execute(
            'SELECT id FROM user_infos WHERE CPF = ?', (CPF,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(CPF)

        if error is None:
            db.execute(
                'INSERT INTO user_infos(name, place_id, email, CPF)' 
                'VALUES (?, ?, ?, ?)',
                (name, place_id, email, CPF)
            )
            db.commit()
            return redirect(url_for('auth.register'))

        flash(error)
    db = get_db()   
    
    row = [(item[0],item[1]) for item in db.execute("SELECT id, name FROM places").fetchall()]
    
    return render_template('auth/register_user.html', options_place=row)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM account WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')




@bp.route('/find_register', methods=('GET', 'POST'))
def find_register():
    db = get_db()
    if request.method == 'POST':    
        return redirect(url_for('auth.register_conf', username = request.form['username']))
        
    rows = db.execute('SELECT username, type, activate'
                      ' FROM account u JOIN options_user o ON u.options_id = o.id'
                     ).fetchall()
    return render_template('auth/find_register.html', options=rows)






@bp.route('/register_conf', methods=('GET', 'POST'))
def register_conf():
    username = request.args['username'] 
        
    db = get_db()
    if request.method == 'POST': 
            try:
                request.form['ativar']
                activate=True
            except:
                activate = False
                
            db.execute(
                'UPDATE account SET activate = ?'
                'WHERE username = ?',
                (activate, username,)
            )
            db.commit()
    row = db.execute(
            'SELECT * FROM account a ' 
            'INNER JOIN user_infos u ON a.user_id = u.id '
            'INNER JOIN places  p ON p.id = u.place_id '
            'INNER JOIN options_user o ON  a.options_id = o.id '
            'WHERE a.username = ?', (username,)
        ).fetchone()
    return render_template('auth/register_conf.html', post=row)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM account WHERE id = ?', (user_id,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view