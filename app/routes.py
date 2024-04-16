from flask import request, jsonify
from app import app, db
from app.models import User, Train, Booking
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({'message': 'Incomplete data provided'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Incomplete data provided'}), 400

    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity={'username': username, 'role': user.role, 'id': user.id})

    return jsonify({'access_token': access_token, 'role': user.role, 'id': user.id}), 200

@app.route('/trains', methods=['POST'])
@jwt_required()
def add_train():
    current_user = get_jwt_identity()
    role = current_user.get('role', None)

    if role != 'admin':
        return jsonify({'message': 'Only admins can add trains'}), 403

    data = request.get_json()
    required_fields = ['train_name', 'train_no', 'source', 'destination', 'total_seats']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    train_name = data['train_name']
    train_no = data['train_no']
    source = data['source']
    destination = data['destination']
    total_seats = data['total_seats']
    seats_left = data['total_seats']

    if not isinstance(total_seats, int) or total_seats <= 0:
        return jsonify({'message': 'Total seats must be a positive integer'}), 400

    existing_train = Train.query.filter_by(train_id=train_name).first()
    if existing_train:
        return jsonify({'message': 'Train with the same name already exists'}), 409

    new_train = Train(train_id=train_name, train_no=train_no, source=source, destination=destination, total_seats=total_seats, seats_left=seats_left)
    db.session.add(new_train)
    db.session.commit()

    return jsonify({'message': 'Train added successfully'}), 201

@app.route('/availability', methods=['GET'])
def get_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return jsonify({'message': 'Both source and destination are required parameters'}), 400

    trains = Train.query.filter_by(source=source, destination=destination).all()

    availability = []
    for train in trains:
        availability.append({
            'train_Name': train.train_id,
            'train_No': train.train_no,
            'available_seats': train.seats_left
        })

    return jsonify({'availability': availability}), 200

@app.route('/book', methods=['POST'])
@jwt_required()
def book_seat():
    current_user = get_jwt_identity()
    user_id = current_user['id']

    data = request.get_json()
    required_fields = ['train_no', 'num_seats']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    train_no = data['train_no']
    num_seats = data['num_seats']

    train = Train.query.filter_by(train_no=train_no).first()

    if not train:
        return jsonify({'message': 'Train not found'}), 404

    if num_seats > train.seats_left:
        return jsonify({'message': 'Insufficient seats available on the train'}), 400

    train.seats_left -= num_seats

    booking = Booking(user_id=user_id, train_id=train.id, no_of_seats_booked=num_seats)

    db.session.add(booking)
    db.session.commit()

    return jsonify({'message': f'{num_seats} seat(s) booked successfully on train {train.train_id}'}), 200

@app.route('/booking/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking_details(booking_id):
    current_user = get_jwt_identity()
    user_id = current_user['id']

    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()

    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    train = Train.query.get(booking.train_id)

    booking_details = {
        'id': booking.id,
        'user_id': booking.user_id,
        'train_id': booking.train_id,
        'train_no': train.train_id,
        'train_name': train.train_no,
        'no_of_seats_booked': booking.no_of_seats_booked
    }

    return jsonify({'booking_details': booking_details}), 200
