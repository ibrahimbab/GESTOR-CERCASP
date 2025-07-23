from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask_paginate import Pagination, get_page_parameter
from ..forms import InternForm
from ..models import Intern
from ..utils import log_action
from .. import db
from flask_babel import _

interns_bp = Blueprint('interns', __name__, url_prefix='/interns')

@interns_bp.route('/list')
@login_required
def list_interns():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    interns = Intern.query.paginate(page=page, per_page=per_page, error_out=False)
    pagination = Pagination(page=page, total=interns.total, per_page=per_page, css_framework='bootstrap5')
    return render_template('list_interns.html', interns=interns.items, pagination=pagination)

@interns_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_intern():
    form = InternForm()
    if form.validate_on_submit():
        intern = Intern(
            name=form.name.data, age=form.age.data, gender=form.gender.data,
            entry_date=form.entry_date.data, initial_drug=form.initial_drug.data,
            wellbeing_score=form.wellbeing_score.data, weekly_fee=form.weekly_fee.data,
            consent_signed=form.consent_signed.data
        )
        intern.set_contact(form.contact_name.data, form.contact_number.data)
        db.session.add(intern)
        db.session.commit()
        log_action('Agregó interno', details=f'ID: {intern.id}')
        flash(_('Interno agregado exitosamente.'), 'success')
        return redirect(url_for('interns.list_interns'))
    return render_template('add_intern.html', form=form)

@interns_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_intern(id):
    intern = Intern.query.get_or_404(id)
    form = InternForm(obj=intern)
    contact_name, contact_number = intern.get_contact()
    form.contact_name.data = contact_name
    form.contact_number.data = contact_number
    if form.validate_on_submit():
        intern.name = form.name.data
        intern.age = form.age.data
        intern.gender = form.gender.data
        intern.entry_date = form.entry_date.data
        intern.initial_drug = form.initial_drug.data
        intern.wellbeing_score = form.wellbeing_score.data
        intern.weekly_fee = form.weekly_fee.data
        intern.consent_signed = form.consent_signed.data
        intern.set_contact(form.contact_name.data, form.contact_number.data)
        db.session.commit()
        log_action('Editó interno', details=f'ID: {id}')
        flash(_('Interno actualizado.'), 'success')
        return redirect(url_for('interns.list_interns'))
    return render_template('edit_intern.html', form=form)
