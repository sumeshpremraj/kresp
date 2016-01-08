from flask import Flask ,flash, session , redirect, url_for
from flask import render_template
from flask import request

app = Flask(__name__)
app.secret_key = 'SecrestKey123!#'

    
@app.route("/login", methods=['POST','GET'])
def login():
    error = "None" 
    if (request.method == 'POST'):
        if (request.form['username'] == 'user'):
            session['logged_in'] = True
            return redirect(url_for('.home', username=request.form['username']))
        else:
            error="Username required"
            return render_template('login.html')
    else:   
        return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash ('You have been logged out')
    return login()


@app.route("/home")
def home():
    return render_template('home.html', username=request.args.get('username'),
                           categories=['Art'], allCategories=['Science','Comics'],providers=['blah1@domain.com'],
                           allProviders=['blah2@domain.com','blah3@domain.com'], frequency='Monthly',
                           otherFrequencies=['Daily','Weekly','Bi-weekly'])

@app.route("/signup" ,methods=['POST','GET'])
def signup():
    if (request.method == 'POST'):
         flash("here")
         #Do more validation
         if (request.form['username']):
            #use as needed
            store = {
                 'username' : request.form['username'],
                 'password' : request.form['password'],
                 'categories': request.form.getlist('categories'),
                 'providers' : request.form.getlist('providers'),
                 'frequency': request.form.getlist('frequency')
                 }
            flash( store )
            #redirect to login
            return redirect(url_for('.login'))
         else:
            return ("There was an error")
    else:    
        return render_template('signUp.html')

@app.route("/resetpwd")
def resetpwd():
    return render_template('pwdReset.html')

if __name__ == "__main__":
    app.run(debug=True)
