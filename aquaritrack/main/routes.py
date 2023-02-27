from flask import Blueprint, Flask, render_template, redirect, url_for, flash
from aquaritrack.models import *
from aquaritrack.main.forms import *

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
# Homepage - Displays the livestock and plants.
    all_tanks = Tank.query.all()
    print(all_tanks)
    return render_template('home.html', all_tanks=all_tanks)

# Tank Creation Page - This allows users to add their items before submitting them.
@main.route('/new_tank', methods=['GET', 'POST'])
def new_tank():
    form = TankForm()
    if form.validate_on_submit():
        new_tank = Tank(
            name=form.name.data,
            gallons=form.gallons.data,
            substrate=form.substrate.data,
            filtration=form.filtration.data
        )
        db.session.add(new_tank)
        db.session.commit()

        flash('New tank created!')
        return redirect(url_for('main.tank_detail', tank_id=new_tank.id))
        
    return render_template('new_tank.html', form=form)

# Tank Detail Page - Displays info about livestock and plants and allows users to edit the description
@main.route('/tank/<int:tank_id>', methods=['GET', 'POST'])
def tank_detail(tank_id):
    tank = Tank.query.get_or_404(tank_id)
    form = TankForm(obj=tank)
    if form.validate_on_submit():
        tank.name=form.name.data
        tank.gallons=form.gallons.data
        tank.substrate=form.substrate.data
        tank.filtration=form.filtration.data

        db.session.commit()
        
        flash('Tank updated!')
        return redirect(url_for('main.tank_detail', tank_id=tank.id))
    form.name.data = tank.name
    form.gallons.data = tank.gallons
    form.substrate.data = tank.substrate
    form.filtration.data = tank.filtration

    return render_template('tank_detail.html', tank=tank, form=form)

# Item Creation Page
@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        new_item = Item(
            species=form.species.data,
            quantity=form.quantity.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            tank=form.tank.data
        )
        db.session.add(new_item)
        db.session.commit()

        flash('New item created!')
        return redirect(url_for('main.item_detail', item_id=new_item.id))
    return render_template('new_item.html', form=form)

# Individual Item Page - Goes into further detail about each selected item.
@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = Item.query.get(item_id)
    form = ItemForm(obj=item)
    
    if form.validate_on_submit():
        item.species=form.species.data
        item.quantity=form.quantity.data
        item.category=form.category.data
        item.photo_url=form.photo_url.data
        item.tank=form.tank.data
        db.session.add(item)
        db.session.commit()
        flash('Your changes were successful!')
        return render_template('item_detail.html', item=item, form=form)

    return render_template('item_detail.html', item=item, form=form)
