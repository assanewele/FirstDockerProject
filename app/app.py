from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle de la voiture
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    colour = db.Column(db.String(50), nullable=False)

# Initialisation de la base de données
with app.app_context():
    db.create_all()

# Route pour enregistrer une voiture
@app.route('/car-api/post-car', methods=['POST'])
def add_car():
    data = request.json
    new_car = Car(brand=data['brand'], colour=data['colour'])
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"message": "Car added successfully!"}), 201

# Route pour lister toutes les voitures
@app.route('/car-api/get-cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    output = []
    for car in cars:
        car_data = {'brand': car.brand, 'colour': car.colour}
        output.append(car_data)
    return jsonify(output), 200

@app.route('/')
def hello():
    html_content = ("<h1><p>Welcome to car api !<h1> "
                    "<h4> With this api, you can register a car by giving its brand"
                    " and its color. <br> You can also get cars registered.</p><p>The endpoints are <br> <span style=\"color:blue\"> /car-api/post-car </span> <br>"
                    "and <br> <span style=\"color:blue\"> /car-api/get-cars</span> .</p>"
                    "These are samples of requests: <br>"
                    "<span style=\"color:blue\">curl -X POST http://127.0.0.1:5000/car-api/post-car  -H \"Content-Type: application/json\" -d '{\"brand\": \"Toyota\", \"colour\": \"Red\"}' </span> <br> " 
                    " <span style=\"color:blue\">curl http://127.0.0.1:5000/car-api/get-cars</span></h4>")
    return html_content

@app.route('/car-api/health/ready')
def readiness():
    return jsonify({"status": "ready"}), 200

@app.route('/car-api/health/live')
def liveness():
    return jsonify({"status": "alive"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
