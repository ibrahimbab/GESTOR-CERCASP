from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask_paginate import Pagination, get_page_parameter
from ..forms import ProgressForm
from ..models import Progress
from .. import db
from flask_babel import _

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

@progress_bp.route('/list')
@login_required
def list_progress():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    progress = Progress.query.paginate(page=page, per_page=per_page, error_out=False)
    pagination = Pagination(page=page, total=progress.total, per_page=per_page, css_framework='bootstrap5')
    return render_template('list_progress.html', progress=progress.items, pagination=pagination)

@progress_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_progress():
    form = ProgressForm()
    if form.validate_on_submit():
        progress = Progress(
            intern_id=form.intern_id.data, week=form.week.data,
            medical_note=form.medical_note.data, medical_evaluation=form.medical_evaluation.data,
            psycho_note=form.psycho_note.data, psychological_evaluation=form.psychological_evaluation.data,
            wellbeing_score=form.wellbeing_score.data, payment_status='pending'
        )
        db.session.add(progress)
        db.session.commit()
        flash(_('Progreso registrado.'), 'success')
        return redirect(url_for('progress.list_progress'))
    return render_template('add_progress.html', form=form)
