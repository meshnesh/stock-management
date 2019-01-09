# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# For password hashing
from flask_bcrypt import Bcrypt

from flask import request, jsonify, abort, make_response

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Stocks, User

    app = FlaskAPI(__name__, instance_relative_config=True)

    # overriding Werkzeugs built-in password hashing utilities using Bcrypt.
    bcrypt = Bcrypt(app)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/stocks/', methods=['POST', 'GET'])
    def stocks():
        # get the access token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authed
                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    price = str(request.data.get('price', ''))
                    stockNo = str(request.data.get('stockNo', ''))
                    description = str(request.data.get('description', ''))

                    if name:
                        stock = Stocks(
                            name=name, price=price,
                            stockNo=stockNo, description=description, created_by=user_id)
                        stock.save()
                        response = jsonify({
                            'id': stock.id,
                            'name': stock.name,
                            'price': stock.price,
                            'stockNo': stock.stockNo,
                            'date_created': stock.date_created,
                            'date_modified': stock.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                # GET
                # get all the bucketlists for this user
                stocks = Stocks.get_all(user_id)
                results = []

                for stock in stocks:
                    obj = {
                        'id': stock.id,
                        'name': stock.name,
                        'price': stock.price,
                        'stockNo': stock.stockNo,
                        'date_created': stock.date_created,
                        'date_modified': stock.date_modified,
                        'created_by': stock.created_by
                    }
                    results.append(obj)

                return make_response(jsonify(results)), 200

            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401

    @app.route('/stocks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def stockItem_manipulation(id, **kwargs):
     # retrieve a stockItem using it's ID
        stock = Stocks.query.filter_by(id=id).first()
        if not stock:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            stock.delete()
            return {
            "message": "StockItem {} deleted successfully".format(stock.id) 
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            price = str(request.data.get('price', ))
            stockNo = str(request.data.get('stockNo', ))
            description = str(request.data.get('description', ))
            stock.name = name
            stock.price = price
            stock.stockNo = stockNo
            stock.description = description
            stock.save()
            response = jsonify({
                'id': stock.id,
                'name': stock.name,
                'price': stock.price,
                'stockNo': stock.stockNo,
                'description': stock.description,
                'date_created': stock.date_created,
                'date_modified': stock.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': stock.id,
                'name': stock.name,
                'price': stock.price,
                'stockNo': stock.stockNo,
                'description': stock.description,
                'date_created': stock.date_created,
                'date_modified': stock.date_modified
            })
            response.status_code = 200
            return response

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app