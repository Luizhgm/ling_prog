from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, p.link, hours, places, created, author_id, username, type,money'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' JOIN options_post o ON p.options_id = o.id'
        ' ORDER BY created DESC'
    ).fetchall()
    
    print(posts)
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        money = request.form['money']
        hours = request.form['hours']
        link = request.form['link']
        places = request.form['places']
        tipo = request.form['options']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            
            db.execute(
                'INSERT INTO post (title, body, author_id, money, hours, link, places, options_id)'
                ' VALUES (?, ?, ?, ? ,? ,? ,?,?)',
                (title, body, g.user['id'], money, hours, link, places, int(tipo))
            )
            db.commit()
            return redirect(url_for('blog.index'))
        
    row = [(item[0],item[1]) for item in db.execute("SELECT id,type FROM options_post").fetchall()]
    return render_template('blog/create.html', options=row)

@bp.route('/create_opt', methods=('GET', 'POST'))
@login_required
def create_opt():
    if request.method == 'POST':
        title = request.form['type']
        link = request.form['link']
        
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO options_post (type, link)'
                ' VALUES (?, ?)',
                (title, link)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create_opt.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, p.link, hours, places, created, author_id, username, type,money'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' JOIN options_post o ON p.options_id = o.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
    
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        money = request.form['money']
        hours = request.form['hours']
        link = request.form['link']
        places = request.form['places']
        options_id  = request.form['options_id']
        
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, link = ?, hours = ?, places = ?, money=?, type = ?'
                ' WHERE id = ?',
                (title, body , link, hours, places, money,  options_id, id )
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/show', methods=('GET', 'POST'))
@login_required
def show(id):
    post = get_post(id,check_author=False)
    
    if request.method == 'POST':
        
        if request.form.get('mark'):
            print("mEEE")
            return redirect(url_for('blog.email'))
        else:
            return redirect(url_for('blog.index'))
        
        
        
    return render_template('blog/show.html', post=post)

@bp.route('/email', methods=('GET', 'POST'))
@login_required
def email():
    if request.method == 'POST':
        return redirect(url_for('blog.index'))
        
    
    return render_template('blog/email.html')

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

