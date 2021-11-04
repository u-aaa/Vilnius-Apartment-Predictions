from app.app import db


class Predictions(db.Model):
    '''
    Predictions table model
    '''
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    division = db.Column(db.String)
    area = db.Column(db.Float)
    no_of_rooms = db.Column(db.Float)
    floor = db.Column(db.Float)
    no_of_floors = db.Column(db.Float)
    build_year = db.Column(db.Integer)
    building_type = db.Column(db.String)
    nearest_kindergarten = db.Column(db.Float)
    nearest_educational_institution = db.Column(db.Float)
    nearest_shop = db.Column(db.Float)
    public_transport_stop = db.Column(db.Float)
    price_per_month = db.Column(db.Float)

    def __repr__(self):
        return 'id: {}, division: {}, no_of_rooms: {}, area: {}, floor: {}, no_of_floors: {}, building_type: {}, ' \
               'build_year: {}, nearest_kindergarten: {}, nearest_educational_institution: {}, nearest_shop: {},' \
               'public_transport_stop: {}, price_per_month: {}'.format(self.id, self.division, self.no_of_rooms,
                                                                       self.area, self.floor, self.no_of_floors,
                                                                       self.building_type, self.build_year,
                                                                       self.nearest_kindergarten,
                                                                       self.nearest_educational_institution,
                                                                       self.nearest_shop, self.public_transport_stop,
                                                                       self.price_per_month)
