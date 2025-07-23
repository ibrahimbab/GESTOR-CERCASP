from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask_paginate import Pagination, get_page_parameter
from ..forms import PaymentForm
from ..models import Payment
from .. import db
from flask_babel import _

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')

@payments_bp.route('/list')
@login_required
def list_payments():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    payments = Payment.query.paginate(page=page, per_page=per_page, error_out=False)
    pagination = Pagination(page=page, total=payments.total, per_page=per_page, css_framework='bootstrap5')
    return render_template('list_payments.html', payments=payments.items, pagination=pagination)

@payments_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        payment = Payment(
            intern_id=form.intern_id.data, week_number=form.week_number.data,
            expected_amount=form.expected_amount.data, paid_amount=form.paid_amount.data,
            payment_date=form.payment_date.data, status='paid' if form.paid_amount.data >= form.expected_amount.data else 'pending',
            pending_amount=form.expected_amount.data - form.paid_amount.data
        )
        db.session.add(payment)
        db.session.commit()
        flash(_('Pago registrado.'), 'success')
        return redirect(url_for('payments.list_payments'))
    return render_template('add_payment.html', form=form)
