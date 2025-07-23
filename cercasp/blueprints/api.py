from flask import Blueprint, jsonify
from flask_restful import Resource, Api
from flask_login import login_required
from ..models import Intern
from .. import api

api_bp = Blueprint('api', __name__, url_prefix='/api')

class InternAPI(Resource):
    @login_required
    def get(self, intern_id):
        intern = Intern.query.get_or_404(intern_id)
        return jsonify({'id': intern.id, 'name': intern.name, 'age': intern.age})

api.add_resource(InternAPI, '/intern/<int:intern_id>')
