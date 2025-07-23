from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from ..forms import InventoryForm
from ..models import MedInventory
from .. import db
from flask_babel import _

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/list')
@login_required
def list_inventory():
    items = MedInventory.query.all()
    return render_template('inventory.html', items=items)

@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_inventory():
    form = InventoryForm()
    if form.validate_on_submit():
        item = MedInventory(
            name=form.name.data, quantity=form.quantity.data,
            expiration_date=form.expiration_date.data
        )
        db.session.add(item)
        db.session.commit()
        flash(_('Item de inventario agregado.'), 'success')
        return redirect(url_for('inventory.list_inventory'))
    return render_template('add_inventory.html', form=form)  # Assume similar template
