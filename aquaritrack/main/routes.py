from flask import Blueprint, Flask, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
# Homepage - Displays the livestock and plants.
    return render_template('base.html')


# Login Page - The user enters info, and we authenticate the info.

# Account Creation Page - The user creates their account and is led to the login page after.

# Tank Creation Page - This allows users to add their items before submitting them.

# Tank Detail Page - Displays info about livestock and plants and allows users to edit the description

# Individual Item Page - Goes into further detail about each selected item.