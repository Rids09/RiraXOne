from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import datetime
import random
import time
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Configuration ---
app.config['SECRET_KEY'] = 'RiraXOne_Secret_99'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///riraxone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --- Database Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create DB
with app.app_context():
    db.create_all()

# --- Mock Data ---
INDIAN_CITIES = {
    'DEL': 'New Delhi', 'BOM': 'Mumbai', 'BLR': 'Bengaluru',
    'MAA': 'Chennai', 'HYD': 'Hyderabad', 'CCU': 'Kolkata',
    'PNQ': 'Pune', 'AMD': 'Ahmedabad'
}

MOCK_BOOKINGS = {}

# --- Auth Routes ---
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        username=data.get('username', data['email'].split('@')[0]),
        email=data['email'],
        password=hashed_pw
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Success'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token, 'username': user.username})

    return jsonify({'error': 'Invalid credentials'}), 401


# --- MAIN PAGE ---
@app.route('/')
def home():
    return render_template('RiraXOne.html')


# --- STATIC PAGES ---
@app.route('/<page>')
def serve_static_html(page):
    if page in ['flight.html', 'book.html', 'boarding.html', 'payment.html']:
        return send_from_directory('static', page)
    return jsonify({'error': 'Page not found'}), 404


# --- Flight Logic ---
def generate_flight(flight_number, source_code, dest_code, departure_time, price):
    return {
        'id': f'F{random.randint(1000, 9999)}',
        'flight_number': flight_number,
        'airline': random.choice(['Air India', 'IndiGo', 'SpiceJet', 'Vistara']),
        'source_code': source_code,
        'source_city': INDIAN_CITIES.get(source_code),
        'dest_code': dest_code,
        'dest_city': INDIAN_CITIES.get(dest_code),
        'departure_time': departure_time,
        'duration': f'{random.randint(1, 4)}h {random.randint(0, 59)}m',
        'price': price,
        'stops': random.choice(['Direct', '1 Stop'])
    }


def get_mock_flights(source_code, dest_code, travel_date):
    flights = []
    base_price = random.randint(3000, 15000)

    for i in range(1, 5):
        hour = 6 + i * 3
        flights.append(generate_flight(
            f'{random.choice(["AI", "6E", "UK"])}{random.randint(100, 999)}',
            source_code,
            dest_code,
            f'{hour:02d}:00',
            base_price + random.randint(-500, 500)
        ))

    return flights


# --- API: Search Flights ---
@app.route('/search-flights')
def search_flights():
    source = request.args.get('source', '').upper()
    dest = request.args.get('destination', '').upper()
    date = request.args.get('date')

    if source not in INDIAN_CITIES or dest not in INDIAN_CITIES or source == dest:
        return jsonify({'error': 'Invalid cities'}), 400

    flights = get_mock_flights(source, dest, date)
    return jsonify(flights)


# --- API: Create Booking ---
@app.route('/create-booking', methods=['POST'])
def create_booking():
    data = request.json

    flight_id = data.get('flight_id')
    passengers = data.get('passengers', 1)

    source_code = data.get('source_code', random.choice(list(INDIAN_CITIES.keys())))
    dest_code = data.get('dest_code', random.choice([k for k in INDIAN_CITIES if k != source_code]))

    mock_flight = generate_flight(
        f'M{random.randint(100, 999)}',
        source_code,
        dest_code,
        data.get('departure_time', '10:00'),
        random.randint(5000, 15000)
    )

    total_amount = mock_flight['price'] * passengers
    pnr = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    booking_id = str(int(time.time() * 1000)) + str(random.randint(100, 999))

    booking_details = {
        'booking_id': booking_id,
        'pnr': pnr,
        'flight_id': flight_id,
        'from_code': source_code,
        'from_city': INDIAN_CITIES.get(source_code),
        'to_code': dest_code,
        'to_city': INDIAN_CITIES.get(dest_code),
        'travel_date': data.get('date', '2025-12-25'),
        'departure_time': mock_flight['departure_time'],
        'passengers': passengers,
        'class': data.get('class', 'Economy'),
        'total_amount': total_amount,
        'currency': 'INR',
        'status': 'PENDING_PAYMENT',
        'airline_name': 'RiraXOne Airlines'
    }

    MOCK_BOOKINGS[booking_id] = booking_details
    return jsonify(booking_details), 200


# --- API: Get Booking ---
@app.route('/booking/<booking_id>')
def get_booking(booking_id):
    booking = MOCK_BOOKINGS.get(booking_id)

    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    return jsonify(booking)


# --- API: Pay Booking ---
@app.route('/pay-booking', methods=['POST'])
def pay_booking():
    data = request.json
    booking_id = data.get('booking_id')

    booking = MOCK_BOOKINGS.get(booking_id)

    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    booking['status'] = 'CONFIRMED'
    return jsonify({'message': 'Payment successful', 'booking_id': booking_id}), 200


if __name__ == '__main__':
    app.run(debug=True)
