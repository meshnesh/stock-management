# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db


class StockTestCase(unittest.TestCase):
    """This class represents the stock test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.stock = {'name': 'Polo'}
        self.stock = {'price': 1500}
        self.stock = {'stockNo': 50}
        self.stock = {'description': 'Straight from the cotton miller'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
    
    def stock_creation(self):
        """This helper creates an event(POST request)"""
        stock = {
            'name': 'Polo',
            'price': 1500,
            'stockNo': 50,
            'description': 'Straight from the cotton miller'
        }

        res = self.client().post('/stocks/', data=stock)
        return res
    
    def test_stock_creation(self):
        """Test API can create an event (POST request)"""
        stock_creation = self.stock_creation()
        self.assertEqual(stock_creation.status_code, 201)
        self.assertIn('Polo', str(stock_creation.data))

    def test_api_can_get_all_stocks(self):
        """Test API can get a stock (GET request)."""
        self.stock_creation()
        res = self.client().get('/stocks/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Polo', str(res.data))

    def test_api_can_get_stock_by_id(self):
        """Test API can get a single stockItem by using it's id."""
        stock_creation = self.stock_creation()
        result_in_json = json.loads(stock_creation.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/stocks/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Polo', str(result.data))

    def test_stockItem_can_be_edited(self):
        """Test API can edit an existing stockItem. (PUT request)"""
        stock_creation = self.stock_creation()
        result_in_json = json.loads(stock_creation.data.decode('utf-8').replace("'", "\""))
        rv = self.client().put(
            '/stocks/1',
            data={
                "name": "Blue Shirts",
                'price': 2500,
                'stockNo': 150,
                'description': 'Made from the silks of south'
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/stocks/1')
        self.assertIn('Blue Shirts', str(results.data))

    def test_stocks_deletion(self):
        """Test API can delete an existing stockItem. (DELETE request)."""
        stock_creation = self.stock_creation()
        result_in_json = json.loads(stock_creation.data.decode('utf-8').replace("'", "\""))
        res = self.client().delete('/stocks/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/stocks/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()