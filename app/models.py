# app/models.py

from app import db


class Stocks(db.Model):
    """This class represents the stocks table."""

    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Integer)
    stockNo = db.Column(db.Integer)
    description = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name, price, stockNo, description):
        """initialize with name."""
        self.name = name
        self.price = price
        self.stockNo = stockNo
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Stocks.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Stocks: {}>".format(self.name)