from flask import Blueprint, render_template
from flask_login import login_required
 # Eliminado import incorrecto de 'cached'
from ..models import Intern, Payment, Progress
from ..ml_model import predict_risk
from .. import cache
from flask_babel import _
import matplotlib.pyplot as plt
import io
import base64

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
@cache.cached(timeout=600)
def dashboard():
    total_interns = Intern.query.count()
    pending_payments = Payment.query.filter_by(status='pending').count()
    high_risk = [i for i in Intern.query.all() if predict_risk(i.id) > 0.5]
    # Gráfica con estilo personalizado
    scores = [p.wellbeing_score for p in Progress.query.all() if p.wellbeing_score]
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6,4))
    n, bins, patches = ax.hist(scores, bins=10, color='#1e2a38', edgecolor='#bfa14a', alpha=0.95)
    ax.set_facecolor('#101014')
    fig.patch.set_facecolor('#101014')
    ax.spines['bottom'].set_color('#bfa14a')
    ax.spines['top'].set_color('#bfa14a')
    ax.spines['right'].set_color('#bfa14a')
    ax.spines['left'].set_color('#bfa14a')
    ax.tick_params(axis='x', colors='#bfa14a')
    ax.tick_params(axis='y', colors='#bfa14a')
    ax.set_title('Distribución de Bienestar', color='#bfa14a', fontsize=14, pad=15)
    ax.set_xlabel('Puntuación de Bienestar', color='#bfa14a')
    ax.set_ylabel('Cantidad', color='#bfa14a')
    for patch in patches:
        patch.set_alpha(0.85)
        patch.set_edgecolor('#1976d2')
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    return render_template('dashboard.html', total_interns=total_interns, pending_payments=pending_payments, high_risk=len(high_risk), chart=chart)

@dashboard_bp.route('/')
@login_required
@cache.cached(timeout=600)
def home():
    return render_template('dashboard.html')
