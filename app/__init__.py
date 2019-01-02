# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

from flask import request, jsonify, abort

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Stocks

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/stocks/', methods=['POST', 'GET'])
    def stocks():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            price = str(request.data.get('price', ))
            stockNo = str(request.data.get('stockNo', ))
            description = str(request.data.get('description', ))
            if name:
                stock = Stocks(name=name, price=price, stockNo=stockNo, description=description)
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
                response.status_code = 201
                return response
        else:
            # GET
            stocks = Stocks.get_all()
            results = []

            for stock in stocks:
                obj = {
                    'id': stock.id,
                    'name': stock.name,
                    'price': stock.price,
                    'stockNo': stock.stockNo,
                    'description' : stock.description,
                    'date_created': stock.date_created,
                    'date_modified': stock.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

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

    return app