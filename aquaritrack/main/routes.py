from flask import Blueprint, Flask, render_template, redirect, url_for, flash
from aquaritrack.models import *
from aquaritrack.main.forms import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
# Homepage - Displays the livestock and plants.
    return render_template('base.html')


# Login Page - The user enters info, and we authenticate the info.

# Tank Creation Page - This allows users to add their items before submitting them.
@main.route('/new_tank', methods=['GET', 'POST'])
def create_tank():
    form = TankForm()
    if form.validate_on_submit():
        new_tank = Tank(
            name=form.name.data,
            gallons=form.gallons.data,
            substrate=form.substrate.data
        )
        db.session.add(new_tank)
        db.session.commit()

        flash('New tank created!')
        return redirect(url_for('base'))
    return render_template('new_tank.html', form=form)
# Tank Detail Page - Displays info about livestock and plants and allows users to edit the description
@main.route('/tank/<int:tank_id>', methods=['GET', 'POST'])
def tank_detail(tank_id):
    tank = Tank.query.get_or_404(tank_id)
    form = TankForm()
    if form.validate_on_submit():
        tank.name=form.name.data
        tank.gallons=form.gallons.data
        tank.substrate=form.substrate.data
        db.session.commit()
        
        flash('Tank updated!')
        return redirect(url_for('main.tank_detail', tank_id=tank.id, form=form))
    form.name.data = tank.name
    form.gallons.data = tank.gallons
    form.substrate.data = tank.substrate
    return render_template('tank_detail.html', tank=tank, form=form)
# Item Creation Page
@main.route('/new_item', methods=['GET', 'POST'])
def create_item():
    form = ItemForm()
    if form.validate_on_submit():
        new_item = Item(
            species=form.species.data,
            quantity=form.quantity.data,
            category=form.category.data,
            photo_url=form.photo_url.data
        )
        db.session.add(new_item)
        db.session.commit()

        flash('New item created!')
        return redirect(url_for('main.index'))
    return render_template('new_item.html', form=form)
# Individual Item Page - Goes into further detail about each selected item.