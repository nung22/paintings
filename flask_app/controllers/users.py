from flask_app import app, render_template, request, redirect, bcrypt, session, flash
from flask_app.models.user import User

# Redirect From Index To users Page
@app.route('/')
def index():
    return render_template('index.html')

# Create new user object
@app.route('/register',methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pass)
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : hashed_pass
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    return redirect('/paintings')

# Log user in and redirect to painting dashboard
@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Credentials.")
        return redirect('/')
    pass_valid = bcrypt.check_password_hash(user.password, request.form['password'])
    if not pass_valid:
        flash("Invalid Credentials.")
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/paintings')

# Logs user out and clears session data
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
