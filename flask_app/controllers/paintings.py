from flask_app import app, render_template, request, redirect,bcrypt, flash, session
from flask_app.models.painting import Painting
from flask_app.models.user import User


# Display painting dashboard
@app.route('/paintings')
def paintings():
    if 'user_id' not in session:
        return redirect('/logout')
    data = { 'id' : session['user_id'] }
    return render_template('paintings.html', user = User.get_by_user_id(data) , all_paintings = Painting.get_all())

# Display information for an individual painting
@app.route('/paintings/<int:id>')
def paintings_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = { 'id' : int(id) }
    print(Painting.get_by_id(data))
    return render_template('paintings_show.html', user_name = session['first_name'], painting = Painting.get_by_id(data))

# Display form to create new painting
@app.route('/paintings/new')
def paintings_new():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('paintings_new.html', user_id = session['user_id'])

# Create new painting and redirect to painting dashbaord
@app.route('/new_painting',methods=['POST'])
def new_painting():
    print(request.form)
    if not Painting.validate_painting(request.form):
        return redirect('/paintings/new')
    Painting.save(request.form)
    return redirect('/paintings')

# Display form to edit an existing painting
@app.route('/paintings/<int:id>/edit')
def paintings_edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = { 'id' : id }
    return render_template('paintings_edit.html', painting = Painting.get_by_id(data))

# Edit an existing painting and redirect to painting dashboard
@app.route('/edit_painting', methods=['POST'])
def edit():
    print(request.form)
    if not Painting.validate_painting(request.form):
        painting_id = request.form['id']
        return redirect(f'/paintings/{painting_id}/edit')
    Painting.edit(request.form)
    return redirect('/paintings')

# Buy an existing painting and update its quantity and purchased numbers
@app.route('/buy_painting/<int:painting_id>/<int:quantity>/<int:purchased>')
def buy(painting_id, quantity, purchased):
    user_data = {
        'user_id' : session['user_id'],
        'painting_id' : painting_id 
    }
    book_data = {
        'id' : painting_id,
        'quantity' : quantity - 1,
        'num_purchased' : purchased + 1
    }
    User.make_purchase(user_data)
    Painting.buy(book_data)
    return redirect(f'/paintings/{painting_id}')

# Delete a painting given its id
@app.route('/paintings/<int:id>/destroy')
def delete(id):
    data = { 'id' : id }
    Painting.delete(data)
    return redirect('/paintings')