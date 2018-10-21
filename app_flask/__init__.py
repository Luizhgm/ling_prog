from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
import json

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

  
    from . import db,auth,blog
    db.init_app(app)    
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')


    return app

app=create_app()



"""@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(url_for('hello'))
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    logins=dict()
    with open('app_flask/textos/logins.json') as data_file:    
        data = json.load(data_file)
        for aux in data:
            logins[aux["username"]]=aux["password"]
            
    if  request.form['username'] in logins:
        if request.form['password'] == logins [request.form['username']]:
            session['logged_in'] = True
            session["name"]=request.form['username']
        else:
            flash('wrong password!')
    else:
        flash('wrong login!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
""" 
