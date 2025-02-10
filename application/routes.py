from application import app
from flask import render_template, request, redirect, flash, url_for

from bson import ObjectId

from .forms import TodoForm ,RegisterForm, LoginForm , QueryForm , ReplyForm
from application import db
from datetime import datetime
from werkzeug.security import generate_password_hash ,check_password_hash



@app.route("/")
def index():
   
    return render_template("index.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        form = RegisterForm(request.form)
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        result=db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password,
            "date_registered": datetime.utcnow()
        })

        user_id = str(result.inserted_id)  # Get the inserted MongoDB ID

        flash("Registration successful", "success")
        return redirect(url_for("home", id=user_id))
    else:
        form = RegisterForm()
    return render_template("register.html", form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        email = form.email.data
        password = form.password.data

        user = db.users.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            user_id = str(user["_id"])  # Convert MongoDB ID to string
            flash("Login successful", "success")
            return redirect(url_for("home", id=user_id))  # Redirect with user ID
        else:
            flash("Invalid email or password", "danger")
    else:
         form = LoginForm()
    return render_template("login.html",form=form)



@app.route('/profile/<id>')
def profile(id):
    # Render user profile page
    user_details = db.users.find_one({"_id": ObjectId(id)})
    return render_template('profile.html', user=user_details)


@app.route('/logout')
def logout():
    # Perform logout action
    flash("Loged out succesfully", "success")
    return render_template('index.html')



@app.route("/home/<id>")
def home(id):
    latest_news = []
    for item in db.news.find().sort("date_published", -1):
        item["_id"] = str(item["_id"])  # Convert MongoDB ID to string
        latest_news.append(item)

    user_details = db.users.find_one({"_id": ObjectId(id)})  # Fetch user details

    return render_template("home.html", latest_news=latest_news, user=user_details)

    

@app.route("/community/<id>")
def community(id):
    # Fetch Queries
    user_queries = db.queries.find({"questioner_id": id})  # User's queries
    other_queries = db.queries.find({"questioner_id": {"$ne": id}})  # Other users' queries

    user_details = db.users.find_one({"_id": ObjectId(id)})
    return render_template("community.html", user_queries=user_queries, other_queries=other_queries,user=user_details)





@app.route("/post_query/<id>", methods=['POST', 'GET'])
def post_query(id):
    form = QueryForm()
    
    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        domain = form.domain.data

        db.queries.insert_one({  
            "questioner_id": id,
            "title": title,
            "description": description,
            "domain": domain,
            "date_posted": datetime.utcnow(),
            "replies": []  # Empty list to store future replies
        })

        flash("Query posted successfully", "success")
        return redirect(url_for("community", id=id))
    
    return render_template("post_query.html", form=form)



@app.route("/reply/<query_id>/<id>", methods=["GET", "POST"])
def reply(query_id,id):
    query = db.queries.find_one({"_id": ObjectId(query_id)})
    if not query:
        flash("Query not found!", "danger")
        return redirect(url_for('community', id=id))

    form = ReplyForm()
    replyer = db.users.find_one({"_id": ObjectId(id)})
    username = replyer.get("username", "Unknown User")  

    if form.validate_on_submit():
        reply_data = {
            "replyer": username, 
            "text": form.reply_text.data,
            "timestamp": datetime.utcnow() 
        }
        db.queries.update_one({"_id": ObjectId(query_id)}, {"$push": {"replies": reply_data}})
        flash("Reply posted successfully!", "success")
        return redirect(url_for('community', id=id))

    return render_template("reply.html", form=form, query=query)









@app.route("/one")
def get_todos():
    todos = []
    for todo in db.todos_flask.find().sort("date_created", -1):
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(todo)

    return render_template("view_todos.html", todos = todos)
    

@app.route("/add_todo", methods = ['POST', 'GET'])
def add_todo():
    if request.method == "POST": 
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        # db.collection_name 
        db.todos_flask.insert_one({
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        })
        flash("Todo successfully added", "success")
        return redirect("/")
    else:
        form = TodoForm()
    return render_template("add_todo.html", form = form)


@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todos_flask.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo successfully deleted", "success")
    return redirect("/")


@app.route("/update_todo/<id>", methods = ['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todos_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully updated", "success")
        return redirect("/")
    else:
        form = TodoForm()

        todo = db.todos_flask.find_one_or_404({"_id": ObjectId(id)})
        print(todo)
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completd", None)

    return render_template("add_todo.html", form = form)


