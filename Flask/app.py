from flask import Flask ,flash, session , redirect, url_for
from flask import render_template
from flask import request
import mysql.connector
import json
from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__)
app.secret_key = 'SecrestKey123!#'
app.host = '0.0.0.0'
db=mysql.connector.connect(database="kresp",user='kresp')

@app.route("/", methods=['POST','GET'])
def root():
    session.permanent = True
    try:
        user = session['user'] 
        return redirect(url_for('.home', username=user))    
    except KeyError:
        session['logged_in']= False
    return redirect(url_for('.login'))
                        
    
@app.route("/login", methods=['POST','GET'])
def login():
    session.permanent = True              
    user_cursor=db.cursor(buffered = True)
    error = "None" 
    if(request.method == 'POST'):
        user_query='select email_id,password_hash from user where email_id = "%s"' % request.form['username'] 
        user_cursor.execute(user_query)
        if user_cursor.rowcount:
            tmp,result = user_cursor.fetchone()
            if pwd_context.verify(request.form['password'], result):
                session['logged_in'] = True
                session['user'] = request.form['username']
                return redirect(url_for('.home', username=request.form['username']))
            else:
                flash("Wrong Password. Please try again.")
                return render_template('login.html')
        else:
                flash("Invalid credentials. Please try again.")
                return render_template('login.html')
    else:   
        return render_template('login.html', error=error)
    user_cursor.close()

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash ('You have been logged out')
    return login()


@app.route("/home", methods=['POST','GET'])
def home():
    user_cursor=db.cursor(buffered = True)
    categories_cursor=db.cursor(buffered = True)
    category_mapping_cursor=db.cursor(buffered = True)
    user_data_query = "select category_ids, providers_list,kindle_id from user where email_id = '%s'" % request.args['username']
    user_cursor.execute(user_data_query)
    category_id_list = ""
    provider_id_list = ""
    kindle_id = ""
    for list_ids in user_cursor:
        category_id_list = ''.join(list_ids[0])
        provider_id_list = ''.join(list_ids[1])
        kindle_id = ''.join(list_ids[2])
    # get all categories selected by user
    user_categories_list = []
    all_categories_list = []
    categories_user_name_fetch_query = None
    categories_all_name_fetch_query = None
    if(len(category_id_list) <=0 ):
        user_categories_list = []
        categories_user_name_fetch_query = None
        categories_all_name_fetch_query = "select * from categories"
    else:    
        categories_user_name_fetch_query = "select * from categories where id in (%s)" % category_id_list 
        categories_all_name_fetch_query = "select * from categories where id not in (%s)" % category_id_list 
    if(categories_user_name_fetch_query is not None):
        categories_cursor.execute(categories_user_name_fetch_query)
        for (category) in categories_cursor:
            user_categories_list.append({'id':str(category[0]), 'name':str(category[1])})
    if(categories_all_name_fetch_query is not None):        
        categories_cursor.execute(categories_all_name_fetch_query)
        for (category) in categories_cursor:
            all_categories_list.append({'id':str(category[0]), 'name':str(category[1])})

    # get all providers selected by user
    user_providers_list = []
    all_providers_list = []
    category_mapping_user_providers_query =None
    category_mapping_all_providers_query = None
    if(len(category_id_list) <=0 and len(provider_id_list) <=0 ):
        category_mapping_all_providers_query = "select id,site_name from category_mapping"
    elif (len(category_id_list) > 0 and len(provider_id_list) >0 ):
        category_mapping_user_providers_query = "select id,site_name from category_mapping where category_id in (%s) and id in (%s)" % (category_id_list, provider_id_list)
        category_mapping_all_providers_query = "select id,site_name from category_mapping where category_id in (%s) and id not in (%s)" % (category_id_list, provider_id_list)
    elif(len(category_id_list) > 0 and len(provider_id_list) <=0):
        category_mapping_all_providers_query = "select id,site_name from category_mapping where category_id in (%s) " % category_id_list
    elif(len(category_id_list) <=0 and len(provider_id_list) > 0 ):
        category_mapping_user_providers_query = "select id,site_name from category_mapping where  id in (%s)" %  provider_id_list
    else:
        category_mapping_user_providers_query =None
        category_mapping_all_providers_query = None
    if(category_mapping_user_providers_query is not None):
         category_mapping_cursor.execute(category_mapping_user_providers_query)
         for (provider) in category_mapping_cursor:
            user_providers_list.append({'id':str(provider[0]), 'name':str(provider[1])})
    if(category_mapping_all_providers_query is not None):
         category_mapping_cursor.execute(category_mapping_all_providers_query)
         for (provider) in category_mapping_cursor:
            all_providers_list.append({'id':str(provider[0]), 'name':str(provider[1])})
        
        
    freq_list = getFrequencyDict(request.args['username'])
    
    
    user_cursor.close()
    categories_cursor.close()
    category_mapping_cursor.close()
    if("kindle" not in request.headers.get('User-Agent')):
            #render template with javascript   
            return render_template('home_JS.html', kindle_id=kindle_id,
                           categories=user_categories_list, allCategories= all_categories_list,providers=user_providers_list,
                           allProviders= all_providers_list, frequencies=freq_list)
    else:
        #render template without javascript   
            return render_template('home.html', kindle_id=kindle_id,
                           categories=user_categories_list, allCategories= all_categories_list,providers=user_providers_list,
                           allProviders= all_providers_list, frequencies=freq_list)
        
def getFrequencyDict(user):
        user_cursor=db.cursor(buffered = True)
        user_data_query = "select frequency, kindle_id from user where email_id = '%s'" % user
        user_cursor.execute(user_data_query)
        for (frequency) in user_cursor:
            freq = frequency[0]
            kindle_id = frequency[1]
        freq_list = []   
        frequency = {1: 'Daily', 7: 'Weekly', 14: 'Bi-weekly', 30:'Monthly'}
        for i in frequency:
            if( i == freq):
                freq_list.append({'id':i,'name':frequency[i],'selected':'selected'})
            else:
                freq_list.append({'id':i,'name':frequency[i],'selected':''})          
        user_cursor.close()
        return freq_list

@app.route("/signup" ,methods=['POST','GET'])
def signup():
    if (request.method == 'POST'):
         user_cursor=db.cursor(buffered = True)
         #Do more validation
         if (request.form['username'] and request.form['password'] ):
             password_hash = pwd_context.encrypt(request.form['password'])
             category_list = ""
             provider_list= ""    
             for category in request.form.getlist('categories'):
                 category_list += category + ","    
             for provider in request.form.getlist('providers'):
                 provider_list += provider + ","  
             user_insert_query = "insert into user(email_id,kindle_id,password,password_hash,frequency,category_ids,providers_list) values('%s','%s','%s','%s','%s','%s','%s')" %(request.form['username'],request.form['kindle_id'],request.form['password'],password_hash,request.form['frequency'],category_list[:-1],provider_list[:-1])
             print user_insert_query
             if(user_cursor.execute(user_insert_query)):
                #redirect to login
                db.commit()
                user_cursor.close()
                return redirect(url_for('.login'))
             else:
                 user_cursor.close()
                 flash("Unexpected Error")
                 return render_template('signUp_JS.html',allCategories= request.form.getlist('categories'), allProviders =request.form.getlist('providers'))
                     
         else:
            flash ("Please enter missing fields.")
            return render_template('signUp_JS.html',allCategories= request.form.getlist('categories'), allProviders =request.form.getlist('providers'))
    else:
        categories_cursor=db.cursor(buffered = True)
        category_mapping_cursor=db.cursor(buffered = True)
        #get all categories not selected by user    
        categories_all_name_fetch_query = "select * from categories" 
        categories_cursor.execute(categories_all_name_fetch_query)
        all_categories_list = []
        for (category) in categories_cursor:
            all_categories_list.append({'id':str(category[0]), 'name':str(category[1])})
            
         # get all providers 
        category_mapping_providers_query = "select id,site_name from category_mapping"
        category_mapping_cursor.execute(category_mapping_providers_query)
        provider_list= []
        for provider in category_mapping_cursor:
            provider_list.append({'id':provider[0],'name':provider[1]})
        category_mapping_cursor.close()    
        categories_cursor.close()   
        if("kindle" not in request.headers.get('User-Agent')):
            #render template with javascript
            return render_template('signUp_JS.html',allCategories= all_categories_list, allProviders =provider_list)
        else:
            #render template without javascript
            return render_template('signUp.html',allCategories= all_categories_list )
    

@app.route("/updateProvider" ,methods=['POST','GET'])
def updateProvider():    
    return getUpdatedProviders(request.form.getlist('categories'), request.form.getlist('providers'))
 
 

@app.route("/updateProviderSignUp" ,methods=['POST','GET'])
def updateProviderSignUp():    
    return getUpdatedProviders_SignUp(request.form.getlist('categories'), request.form.getlist('providers'))


def getUpdatedProviders_SignUp(cats,provs):
    category_mapping_cursor=db.cursor(buffered = True)
    categories_cursor=db.cursor(buffered = True)
    category_list = ""
    provider_list = ""
    for category in cats:
        category_list += category + ","  
    for provider in provs:
        provider_list += provider + ","  
    if(len(category_list ) <= 0 ):
         user_categories_list = []
         categories_all_name_fetch_query = "select * from categories"
    else:        
         categories_user_name_fetch_query = "select * from categories where id in (%s)" % category_list[:-1]
         categories_all_name_fetch_query = "select * from categories where id not in (%s)" % category_list[:-1]
         categories_cursor.execute(categories_user_name_fetch_query)
         user_categories_list=[]
         for (category) in categories_cursor:
            user_categories_list.append({'id':str(category[0]), 'name':str(category[1])})
         
    categories_cursor.execute(categories_all_name_fetch_query)
    all_categories_list=[]
    
    for (category) in categories_cursor:
        all_categories_list.append({'id':str(category[0]), 'name':str(category[1])})
    
     # get all providers selected by user
    category_mapping_user_providers_query =None
    category_mapping_all_providers_query = None
    all_providers_list = []
    user_providers_list = []
    if(len(category_list) <=0 and len(provider_list) <=0 ):
        category_mapping_all_providers_query = "select id,site_name from category_mapping"
    elif (len(category_list) > 0 and len(provider_list) >0 ):
        category_mapping_user_providers_query = "select id,site_name from category_mapping where category_id in (%s) and id in (%s)" % (category_list[:-1], provider_list[:-1])
        category_mapping_all_providers_query = "select id,site_name from category_mapping where category_id in (%s) and id not in (%s)" % (category_list[:-1], provider_list[:-1])
    elif(len(category_list) > 0 and len(provider_list) <=0):
        category_mapping_all_providers_query = "select id,site_name from category_mapping where category_id in (%s) " % category_list[:-1]
    elif(len(category_list) <=0 and len(provider_list) > 0 ):
        category_mapping_user_providers_query = "select id,site_name from category_mapping where  id in (%s)" %  provider_list[:-1]
    else:
        category_mapping_user_providers_query =None
        category_mapping_all_providers_query = None
    if(category_mapping_user_providers_query is not None):
         category_mapping_cursor.execute(category_mapping_user_providers_query) 
         for (provider) in category_mapping_cursor:
            user_providers_list.append({'id':str(provider[0]), 'name':str(provider[1])})
    if(category_mapping_all_providers_query is not None):
         category_mapping_cursor.execute(category_mapping_all_providers_query)
         for (provider) in category_mapping_cursor:
            all_providers_list.append({'id':str(provider[0]), 'name':str(provider[1])})
       
    categories_cursor.close()
    category_mapping_cursor.close()
    if("kindle" not in request.headers.get('User-Agent')):
           #render signup template with javascript
           return render_template('signUp_JS.html', kindle_id=request.form['kindle_id'],
                           categories=user_categories_list, allCategories= all_categories_list,providers=user_providers_list,
                           allProviders= all_providers_list)
    else:
        #render template without javascript
        return render_template('signUp.html', kindle_id=request.form['kindle_id'],
                           categories=user_categories_list, allCategories= all_categories_list,providers=user_providers_list,
                           allProviders= all_providers_list)    
    
 
def getUpdatedProviders(cats,provs):
    category_mapping_cursor=db.cursor(buffered = True)
    categories_cursor=db.cursor(buffered = True)
    category_list = ""
    provider_list = ""
    for category in cats:
        category_list += category + ","  
    for provider in provs:
        provider_list += provider + ","  
    if(len(category_list ) <= 0 ):
         user_categories_list = []
         categories_all_name_fetch_query = "select * from categories"
    else:        
         categories_user_name_fetch_query = "select * from categories where id in (%s)" % category_list[:-1]
         categories_all_name_fetch_query = "select * from categories where id not in (%s)" % category_list[:-1]
         categories_cursor.execute(categories_user_name_fetch_query)
         user_categories_list=[]
         for (category) in categories_cursor:
            user_categories_list.append({'id':str(category[0]), 'name':str(category[1])})
         
    categories_cursor.execute(categories_all_name_fetch_query)
    all_categories_list=[]
    
    for (category) in categories_cursor:
        all_categories_list.append({'id':str(category[0]), 'name':str(category[1])})
    
     # get all providers selected by user
    category_mapping_user_providers_query =None
    category_mapping_all_providers_query = None
    all_providers_list = []
    user_providers_list = []
    if(len(category_list) <=0 and len(provider_list) <=0 ):
        category_mapping_all_providers_query = "select id,site_name from category_mapping"
    elif (len(category_list) > 0 and len(provider_list) >0 ):
        category_mapping_user_providers_query = "select id,site_name from category_mapping where category_id in (%s) and id in (%s)" % (category_list[:-1], provider_list[:-1])
        category_mapping_all_providers_query = "select id,site_name from category_mapping where category_id in (%s) and id not in (%s)" % (category_list[:-1], provider_list[:-1])
    elif(len(category_list) > 0 and len(provider_list) <=0):
        category_mapping_all_providers_query = "select id,site_name from category_mapping where category_id in (%s) " % category_list[:-1]
    elif(len(category_list) <=0 and len(provider_list) > 0 ):
        category_mapping_user_providers_query = "select id,site_name from category_mapping where  id in (%s)" %  provider_list[:-1]
    else:
        category_mapping_user_providers_query =None
        category_mapping_all_providers_query = None
    if(category_mapping_user_providers_query is not None):
         category_mapping_cursor.execute(category_mapping_user_providers_query) 
         for (provider) in category_mapping_cursor:
            user_providers_list.append({'id':str(provider[0]), 'name':str(provider[1])})
    if(category_mapping_all_providers_query is not None):
         category_mapping_cursor.execute(category_mapping_all_providers_query)
         for (provider) in category_mapping_cursor:
            all_providers_list.append({'id':str(provider[0]), 'name':str(provider[1])})
       
    categories_cursor.close()
    category_mapping_cursor.close()
    if("kindle" not in request.headers.get('User-Agent')):
           #render signup template with javascript
           return render_template('home_JS.html', kindle_id=request.form['kindle_id'],
                           categories=user_categories_list, allCategories= all_categories_list,providers=user_providers_list,
                           allProviders= all_providers_list, frequencies=getFrequencyDict(session['user']))
    else:
        #render template without javascript
        return render_template('home.html', kindle_id=request.form['kindle_id'],
                           categories=user_categories_list, allCategories= all_categories_list,providers=user_providers_list,
                           allProviders= all_providers_list, frequencies=getFrequencyDict(session['user']))

@app.route("/update" ,methods=['POST','GET'])
def update():
    if (request.method == 'POST'):
         user_cursor=db.cursor(buffered = True)
         #Do more validation
         if (session['logged_in'] ):
             category_list = ""
             provider_list = ""
             for provider in request.form.getlist('providers'):
                 provider_list += provider + ","      
             for category in request.form.getlist('categories'):
                 category_list += category + ","    
             user_update_query = "update user set kindle_id = '%s', frequency = '%s' , category_ids = '%s', providers_list = '%s' where email_id = '%s'" %(request.form['kindle_id'],request.form['frequency'],category_list[:-1], provider_list[:-1], session['user'])
             print user_update_query
             if(user_cursor.execute(user_update_query)):
                #redirect to login
                db.commit()
                user_cursor.close()
                return redirect(url_for('.home', username=session['user']))
             else:
                 user_cursor.close()
                 return("Unexpected Error")        
         else:
            return ("There was an error")
    else:
        return("Something isn't right")
    
    
    
@app.route("/resetpwd")
def resetpwd():
    return render_template('pwdReset.html')

@app.route("/unsubscribe")
def unsubscribe():
    try:
        user = session['user']
        unsubscribe_cursor=db.cursor(buffered = True)
        unsubscribe_query='update user set active = False where email_id = "%s"' % user
        unsubscribe_cursor.execute(unsubscribe_query)
        db.commit()
        if unsubscribe_cursor.rowcount:
            return render_template('confirm-unsubscribe.html', user=user)
        else:
            flash("Unable to unsubscribe user " + user)
            return redirect(url_for('.home', username=user))

    except KeyError:
        session['logged_in'] = False
        return redirect(url_for('.login'))
    

if __name__ == "__main__":
    app.run(debug=True)
