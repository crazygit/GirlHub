# -*- coding: utf-8 -*-

from flask_restplus import Namespace, Resource, fields, reqparse
from girls.models import Girl as GirlModel
from girls.lib.validation import page_validator, per_page_validor

ns_girl = Namespace('Beautiful Girl', description='shine your eyes', path='/')

brief_girl = ns_girl.model(
    'Girl', {
        "title": fields.String,
        "cover": fields.String,
    }
)
girl_list = ns_girl.model('GirlList', {
    'girls': fields.List(fields.Nested(brief_girl), attribute='items'),
    'has_next': fields.Boolean,
    'has_prev': fields.Boolean,
    'total': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,

})


@ns_girl.route('/girl')
class Girl(Resource):
    @ns_girl.marshal_list_with(girl_list)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', default=1, type=page_validator)
        parser.add_argument('per_page', default=10, type=per_page_validor)
        args = parser.parse_args()
        return GirlModel.query.order_by(GirlModel.created_on.desc()).paginate(page=args['page'],
                                                                              per_page=args['per_page'],
                                                                              error_out=False)
