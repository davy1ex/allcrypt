from flask import render_template, redirect, url_for
from app import app
from app.forms import RegistrationForm


@app.route('/')
def index():
    return render_template('index.html', title='home')


@app.route('/reg')
def reg():
    form = RegistrationForm()
    return render_template('reg.html', form=form)


@app.route('/logout')
def out():
    return redirect(url_for('index'))
