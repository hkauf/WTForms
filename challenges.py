from flask.ext.wtf import form
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required,Email
import requests
import json
#import statements go here

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"

#create class to represent WTForm that inherits flask form
class itunesForm(FlaskForm):
    artist = StringField('Enter artist', validators=[Required()])
    api = IntegerField('Enter the number of results you want the API to return', validators=[Required()])
    email = StringField('Enter your email', validators=[Required(), Email()])
    submit = SubmitField('Submit')


@app.route('/itunes-form')
def itunes_form():
    #what code goes here?
    simpleForm= itunesForm()
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    #what code goes here?
    # HINT : create itunes-results.html to represent the results and return it
    form = itunesForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        artist = form.artist.data #request.args.get('artist')
        api = form.api.data
        params = {}
        params['term']= artist
        params['limit']= api
        base_url= requests.get('https://itunes.apple.com/search', params = params)
        response= json.loads(base_url.text)['results']

    flash('All fields are required!')
    return render_template('itunes-result.html', result_html = response) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
