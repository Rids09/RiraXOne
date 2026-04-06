from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import datetime
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


# --- MAIN ROUTE (FIXED) ---
@app.route('/')
def home():
    return render_template('RiraXOne.html')


# --- STATIC HTML PAGES ---
@app.route('/<page>')
def serve_static_html(page):
    if page in ['flight.html', 'book.html', 'boarding.html', 'payment.html']:
        return app.send_static_file(page)
    return jsonify({'error': 'Not found'}), 404


# --- API ROUTE ---
@app.route('/search-flights')
def search_flights():
    source = request.args.get('source', '').upper()
    dest = request.args.get('destination', '').upper()

    if source not in INDIAN_CITIES or dest not in INDIAN_CITIES:
        return jsonify({'error': 'Invalid cities'}), 400

    return jsonify([])


if __name__ == '__main__':
    app.run(debug=True)