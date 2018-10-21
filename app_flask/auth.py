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
        tipo = request.form['options']
        
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not tipo:
            error = 'Modalide não escolhida.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            if tipo=="1" or tipo =="2":
                activate=False;
            else:
                activate=True;
            db.execute(
                'INSERT INTO user (username, password,options_id,activate ) VALUES (?, ?, ?, ?)',
                (username, generate_password_hash(password), tipo, True)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    db = get_db()   
    row = [(item[0],item[1]) for item in db.execute("SELECT id,type FROM options_user").fetchall()]
    
    return render_template('auth/register.html', options=row)

@bp.route('/register_conf', methods=('GET', 'POST'))
def register_conf():
    db = get_db()
    if request.method == 'POST':
            activate = request.form['options']
            print(activate)
            username = request.form['username']
            print(username,activate)
            db.execute(
                'UPDATE user set activate = ? '
                'where username = ?',
                (activate, username)
            )
            db.commit()
            
            return redirect(url_for('blog.index'))
        
    rows = db.execute('SELECT username, type, activate'
                      ' FROM user u JOIN options_user o ON u.options_id = o.id'
                     ).fetchall()
    return render_template('auth/register_give.html', options=rows, keys=[(1,True),(0,False)])

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
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

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
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