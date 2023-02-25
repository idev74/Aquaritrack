from flask import Blueprint

auth = Blueprint('auth', __name__)

# Account Creation Page - The user creates their account and is led to the login page after.
@auth.route('/new_user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash('New user created!')
        return redirect(url_for('base'))
    return render_template('new_user.html', form=form)
