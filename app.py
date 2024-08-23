from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(100), nullable=False)
    first_nations_name = db.Column(db.String(100))
    scientific_name = db.Column(db.String(100), nullable=False)
    first_nations_uses = db.Column(db.String(500))
    description = db.Column(db.String(500))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    kml_file = db.Column(db.LargeBinary)
    conservation_status = db.Column(db.String(100))
    image = db.Column(db.LargeBinary)

    def to_dict(self):
        return {
            'id': self.id,
            'common_name': self.common_name,
            'first_nations_name': self.first_nations_name,
            'scientific_name': self.scientific_name,
            'first_nations_uses': self.first_nations_uses,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'conservation_status': self.conservation_status,
            'kml_file': base64.b64encode(self.kml_file).decode('utf-8') if self.kml_file else None,
            'image': base64.b64encode(self.image).decode('utf-8') if self.image else None
        }

with app.app_context():
    db.create_all()

@app.route('/api/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants])

@app.route('/api/plants', methods=['POST'])
def create_plant():
    data = request.form

    kml_file = request.files.get('kml_file')
    image = request.files.get('image')

    new_plant = Plant(
        common_name=data.get('common_name'),
        first_nations_name=data.get('first_nations_name'),
        scientific_name=data.get('scientific_name'),
        first_nations_uses=data.get('first_nations_uses'),
        description=data.get('description'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        conservation_status=data.get('conservation_status'),
        kml_file=kml_file.read() if kml_file else None,
        image=image.read() if image else None
    )

    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.to_dict()), 201

@app.route('/api/plants/<int:plant_id>', methods=['GET', 'PUT'])
def update_or_get_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)

    if request.method == 'GET':
        return jsonify(plant.to_dict())

    if request.method == 'PUT':
        data = request.form
        kml_file = request.files.get('kml_file')
        image = request.files.get('image')

        plant.common_name = data.get('common_name', plant.common_name)
        plant.first_nations_name = data.get('first_nations_name', plant.first_nations_name)
        plant.scientific_name = data.get('scientific_name', plant.scientific_name)
        plant.first_nations_uses = data.get('first_nations_uses', plant.first_nations_uses)
        plant.description = data.get('description', plant.description)
        plant.latitude = data.get('latitude', plant.latitude)
        plant.longitude = data.get('longitude', plant.longitude)
        plant.conservation_status = data.get('conservation_status', plant.conservation_status)
        plant.kml_file = kml_file.read() if kml_file else plant.kml_file
        plant.image = image.read() if image else plant.image

        db.session.commit()
        return jsonify(plant.to_dict())

@app.route('/api/plants/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    db.session.delete(plant)
    db.session.commit()
    return jsonify({'message': 'Plant deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)
