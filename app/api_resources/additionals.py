from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Additional

class AdditionalsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ids', required=True)

    def get(self):
        args = AdditionalsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            if args['ids'] != 'all':
                return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        if args['ids'] == 'all':
            return make_response(jsonify(
                {'result': {'additionals': [additional.to_dict() 
                for additional in session.query(Additional).all()]}}
                ), 200)

        session = get_db_session()
        additionals = []
        for a_id in ids:
            additional = session.query(Additional).filter(Additional.id == a_id).first()
            if additional:
                additionals.append(additional)
        if not additionals:
            return make_response(jsonify({'result': {'additionals': 'not found'}}), 404)

        return make_response(jsonify(
            {'result': {'additionals': [additional.to_dict() for additional in additionals]}}), 200)

    def delete(self):
        args = AdditionalsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except TypeError:
            return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        for a_id in ids:
            additional = session.query(Additional).filter(Additional.id == a_id).first()
            if additional:
                session.delete(additional)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
