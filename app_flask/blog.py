from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import time
from datetime import datetime,timedelta 
from .auth import login_required
from .db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, p.link, hours, places, created, author_id, username, type,money'
        ' FROM post p JOIN account u ON p.author_id = u.id'
        ' JOIN options_post o ON p.options_id = o.id'
        ' ORDER BY created DESC'
    ).fetchall()
    
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
        place_id = request.form['opt_place']
        try:
            times = datetime.strptime(request.form['dia'],'%Y/%m/%d').date()
        except ValueError:
            times = datetime.strptime(request.form['dia'],'%Y-%m-%d').date()
        
        error = None
        if not title:
            error = 'Title is required.'
        elif times < datetime.now().date():
            error = 'Data no passado'
        if error is not None:
            flash(error)
        else:
            
            db.execute(
                'INSERT INTO post (title, body, author_id, money, hours, link, places, options_id,place_id,end_created)'
                ' VALUES (?, ?, ?, ? ,? ,? ,?, ?, ?,?)',
                (title, body, g.user['id'], money, hours, link, places, int(tipo), place_id,times)
            )
            db.commit()
            return redirect(url_for('blog.index'))
        
    opt_post = [(item[0],item[1]) for item in db.execute("SELECT id,type FROM options_post").fetchall()]
    opt_plac = [(item[0],item[1]) for item in db.execute("SELECT id,name FROM places").fetchall()]
    return render_template('blog/create.html', options1=opt_post, options2=opt_plac)

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
                'INSERT INTO options_post (type, about)'
                ' VALUES (?, ?)',
                (title, link)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create_opt.html')

@bp.route('/create_center', methods=('GET', 'POST'))
@login_required
def create_center():
    if request.method == 'POST':
        db = get_db()
        name = request.form['name']
        address = request.form['address']
        
        about = request.form['about']
        
        error = None

        if db.execute(
            'SELECT id FROM places WHERE name = ?', (name,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(name)
            
       
        if error is not None:
            flash(error)
        else:
            
            db.execute(
                'INSERT INTO places (name, adress, about)'
                ' VALUES (?, ?, ?)',
                (name, address, about)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create_center.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, p.link, hours, end_created, places, created, author_id, username, type,money, l.name, l.adress'
        ' FROM post p JOIN account u ON p.author_id = u.id'
        ' JOIN user_infos i ON i.id = u.user_id'
        ' JOIN options_post o ON p.options_id = o.id'
        ' JOIN places l ON p.place_id = l.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
 
@bp.route('/<int:id>/find_submits', methods=('GET', 'POST'))
def find_submits(id):
    db = get_db()
    if request.method == 'POST':    
        return redirect(url_for('blog.register_conf', user_id= request.form['user_id']))

    print(id)
    rows = db.execute('SELECT * FROM post_submit '
                      'INNER JOIN user_infos u ON user_id = u.id '
                      ' WHERE post_id = ?',
                      (id,)
                     ).fetchall()
    print(rows)
    return render_template('blog/find_submits.html', options=rows)


@bp.route('/register_conf', methods=('GET', 'POST'))
def register_conf():
    user_id = request.args['user_id'] 
        
    db = get_db()
    if request.method == 'POST': 
            try:
                request.form['selecionar']
                aprovado = True
            except:
                aprovado = False
                
            print("cheguei",aprovado)
            
            db.execute(
                'UPDATE post_submit SET aprovado = ?'
                'WHERE user_id = ?',
                (aprovado, user_id,)
            )
            db.commit()
            
    row = db.execute(
            'SELECT * FROM post_submit k ' 
            'INNER JOIN user_infos u ON k.user_id = u.id '
            'INNER JOIN account a ON a.user_id = u.id '
            'INNER JOIN places  p ON p.id = u.place_id '
            'INNER JOIN options_user o ON  a.options_id = o.id '
            'WHERE u.id = ?', (user_id,)
        ).fetchone()
    
    print("aprovado",user_id, row["aprovado"])
    
    return render_template('blog/register_conf.html', post=row)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    print("me")
    post = get_post(id)
    
    
    
    if request.method == 'POST':
        if g.user['activate']!=True:
            flash('Nada mudou, pq vc é inativo!!')
            pass
        else:
            title = request.form['title']
            body = request.form['body']
            money = request.form['money']
            hours = request.form['hours']
            link = request.form['link']
            places = request.form['places']
            try:
                times = datetime.strptime(request.form['dia'],'%Y/%m/%d').date()
            except ValueError:
                times = datetime.strptime(request.form['dia'],'%Y-%m-%d').date()

            error = None
            if not title:
                error = 'Title is required.'
            elif times < datetime.now().date():
                error = 'Data no passado'

            
            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    'UPDATE post SET title = ?, body = ?, link = ?, hours = ?, places = ?, money=?, end_created=?'
                    ' WHERE id = ?',
                    (title, body , link, hours, places, money, times  , id )
                )
                db.commit()
        return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/show', methods=('GET', 'POST'))
@login_required
def show(id):
    post = get_post(id,check_author=False)
    if post['end_created'] > datetime.now().date():
        in_day=True
    else:
        in_day=False
    
    if request.method == 'POST':
        
        if request.form.get('mark'):
            return redirect(url_for('blog.email', email = post["author_id"], post_id=post["id"]))
        else:
            return redirect(url_for('blog.index'))
        
        
        
    return render_template('blog/show.html', post=post,in_day=in_day)

@bp.route('/email', methods=('GET', 'POST'))
@login_required
def email():
    post_id = request.args["post_id"]
    idx = request.args['email']
    db = get_db()
    if request.method == 'POST':
        
        text = request.form['curriculo']
        email = db.execute('SELECT email'
            ' FROM account u JOIN user_infos i ON i.id = u.user_id'
            ' WHERE u.id = ?',
            (g.user['id'],)
        ).fetchone()
        idx= db.execute('SELECT user_id '
            'FROM account '
            'WHERE id=? ' ,
            (g.user['id'],)
        ).fetchone()
        print("id: ",idx,email)
        try:
            db.execute(
                'INSERT INTO post_submit (post_id,user_id,email,body)'
                ' VALUES (?, ?,?,?)',
                (post_id, idx['user_id'], email['email'],text)
            )
            db.commit()
        except:
            flash("Já cadastrado para essa vaga")
        return redirect(url_for('blog.index'))
    
    
    

        
    email = db.execute('SELECT email'
        ' FROM account u JOIN user_infos i ON i.id = u.user_id'
        ' WHERE u.id = ?',
        (idx,)
    ).fetchone()
    return render_template('blog/email.html', email= email['email'])

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

