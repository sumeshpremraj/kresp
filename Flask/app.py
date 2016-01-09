from flask import Flask ,flash, session , redirect, url_for
from flask import render_template
from flask import request
import mysql.connector

app = Flask(__name__)
app.secret_key = 'SecrestKey123!#'
app.host = '0.0.0.0'
db=mysql.connector.connect(database="kresp",user='kresp')


    
@app.route("/login", methods=['POST','GET'])
def login():
    user_cursor=db.cursor(buffered = True)
    error = "None" 
    if(request.method == 'POST'):
        user_query='select email_id from user where email_id = %s and password= %s'
        user_cursor.execute(user_query,(request.form['username'], request.form['password']))
        result = user_cursor.fetchone()
        user_cursor.close()
        if(result is not None):
            session['logged_in'] = True
            return redirect(url_for('.home', username=result[0]))
        else:
            flash("Invalid credentials. Please try again.")
            return render_template('login.html')
    else:   
        return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash ('You have been logged out')
    return login()


@app.route("/home", methods=['POST','GET'])
def home():
    user_cursor=db.cursor(buffered = True)
    categories_cursor=db.cursor(buffered = True)
    category_mapping_cursor=db.cursor(buffered = True)
    user_data_query = "select category_ids from user where email_id = '%s'" % request.args['username']
    user_cursor.execute(user_data_query)
    category_id_list = ""
    for (category_ids) in user_cursor:
        category_id_list = ''.join(category_ids)
    # get all categories selected by user    
    categories_user_name_fetch_query = "select * from categories where id in (%s)" % category_id_list 
    categories_cursor.execute(categories_user_name_fetch_query)
    user_categories_list = []
    for (category) in categories_cursor:
        user_categories_list.append({'id':str(category[0]), 'name':str(category[1])})

    #get all categories not selected by user    
    categories_all_name_fetch_query = "select * from categories where id not in (%s)" % category_id_list 
    categories_cursor.execute(categories_all_name_fetch_query)
    all_categories_list = []
    for (category) in categories_cursor:
        all_categories_list.append({'id':str(category[0]), 'name':str(category[1])})

    # get all providers selected by user    
    category_mapping_providers_query = "select site_name from category_mapping"
    category_mapping_cursor.execute(category_mapping_providers_query)
    provider_list= []
    for site_name in category_mapping_cursor:
        provider_list.append(site_name[0])
    user_cursor.close()
    categories_cursor.close()
    category_mapping_cursor.close()
        
    return render_template('home.html', username=request.args.get('username'),
                           categories=user_categories_list, allCategories= all_categories_list,providers=['blah1@domain.com'],
                           allProviders=provider_list, frequency='Monthly',
                           otherFrequencies=['Daily','Weekly','Bi-weekly'])

@app.route("/signup" ,methods=['POST','GET'])
def signup():
    if (request.method == 'POST'):
         user_cursor=db.cursor(buffered = True)
         #Do more validation
         if (request.form['username'] and request.form['password'] ):
             category_list = ""
             for category in request.form.getlist('categories'):
                 category_list += category + ","    
             user_insert_query = "insert into user(email_id,kindle_id,password,frequency,category_ids) values('%s','%s','%s','%s','%s')" %(request.form['username'],request.form['kindle_id'],request.form['password'],request.form['frequency'],category_list[:-1])
             print user_insert_query
             if(user_cursor.execute(user_insert_query)):
                #redirect to login
                db.commit()
                user_cursor.close()
                return redirect(url_for('.login'))
             else:
                 user_cursor.close()
                 flash("Unexpected Error")        
         else:
            flash ("There was an error")
    else:
        categories_cursor=db.cursor(buffered = True)
        #get all categories not selected by user    
        categories_all_name_fetch_query = "select * from categories" 
        categories_cursor.execute(categories_all_name_fetch_query)
        all_categories_list = []
        for (category) in categories_cursor:
            all_categories_list.append({'id':str(category[0]), 'name':str(category[1])})
        categories_cursor.close()   
        return render_template('signUp.html',allCategories= all_categories_list)

@app.route("/resetpwd")
def resetpwd():
    return render_template('pwdReset.html')

if __name__ == "__main__":
    app.run(debug=True)
