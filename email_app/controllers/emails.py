from email_app import app
from flask import render_template, redirect, request, session
from email_app.models.emails import Email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    data = {
        'email' : request.form['email']
    }
    if not Email.validate(data):
        return redirect('/')

    session['new_email'] = Email.save(data)
    return redirect('/success')

@app.route('/success')
def success():
    users = Email.get_all()
    data = {
        'id' : session['new_email']
    }
    new_user = Email.get_email_by_id(data)
    print('****************************')
    print(new_user)
    if new_user == False:
        return redirect('/')
    return render_template('success.html', users = users, new_user = new_user)

