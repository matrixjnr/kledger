from config.base import app, db, jwt
from models.models import User, Creditor, user_schema, creditors_schema, creditor_schema, Item, items_schema, item_schema, Tx, txs_schema
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import datetime


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('DB Created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DB Dropped!')

@app.cli.command('db_seed')
def db_seed():

    # Creditors
    cr1 = Creditor(full_name='Super Man', idnumber='34522811', phone='172345678', owner='12345678', debt='6050.00')
    cr2 = Creditor(full_name='Barry Allen', idnumber='54467811', phone='9887583876', owner='12345678', debt='7300.00')
    cr3 = Creditor(full_name='Wally West', idnumber='54378211', phone='345533876', owner='12345678', debt='360.00')
    cr4 = Creditor(full_name='Oliver Arrow', idnumber='20837811', phone='83876334255', owner='23456789', debt='0.00')
    cr5 = Creditor(full_name='Black Carnary', idnumber='24526811', phone='24546324424', owner='23456789', debt='50960.00')
    cr6 = Creditor(full_name='Atom Man', idnumber='13727811', phone='0969894636', owner='23456789', debt='0.00')

    db.session.add(cr1)
    db.session.add(cr2)
    db.session.add(cr3)
    db.session.add(cr4)
    db.session.add(cr5)
    db.session.add(cr6)

    # transactions

    tx1 = Tx(creditorid='34522811', owner='12345678', amount='1000.00')
    tx2 = Tx(creditorid='34522811', owner='12345678', amount='450.00')
    tx3 = Tx(creditorid='34522811', owner='12345678', amount='2000.00')
    tx4 = Tx(creditorid='54467811', owner='12345678', amount='5000.00')
    tx5 = Tx(creditorid='54467811', owner='12345678', amount='2500.00')
    tx6 = Tx(creditorid='54467811', owner='12345678', amount='1000.00')
    tx7 = Tx(creditorid='54378211', owner='12345678', amount='1000.00')
    tx8 = Tx(creditorid='20837811', owner='23456789', amount='1140.00')
    tx9 = Tx(creditorid='24526811', owner='23456789', amount='100000.00')
    tx10 = Tx(creditorid='24526811', owner='23456789', amount='400000.00')
    tx11 = Tx(creditorid='24526811', owner='23456789', amount='50000.00')
    tx12 = Tx(creditorid='24526811', owner='23456789', amount='250000.00')
    tx13 = Tx(creditorid='13727811', owner='23456789', amount='470.00')

    db.session.add(tx1)
    db.session.add(tx2)
    db.session.add(tx3)
    db.session.add(tx4)
    db.session.add(tx5)
    db.session.add(tx6)
    db.session.add(tx7)
    db.session.add(tx8)
    db.session.add(tx9)
    db.session.add(tx10)
    db.session.add(tx11)
    db.session.add(tx12)
    db.session.add(tx13)

    # Items in both shops

    it1 = Item(item_name='Dancing Suit', owner='12345678', borrower='54467811', price='2100.00', quantity='3')
    it2 = Item(item_name='Flash Ring', owner='12345678', borrower='54467811', price='10000.00', quantity='1')
    it3 = Item(item_name='Super Suit', owner='12345678', borrower='34522811', price='3500.00', quantity='2')
    it4 = Item(item_name='Cooking Oil', owner='12345678', borrower='34522811', price='125.00', quantity='20')
    it5 = Item(item_name='Sugar', owner='12345678', borrower='54378211', price='130.00', quantity='10')
    it6 = Item(item_name='Salt', owner='12345678', borrower='54378211', price='60.00', quantity='1')
    it7 = Item(item_name='Books', owner='23456789', borrower='20837811', price='70.00', quantity='2')
    it8 = Item(item_name='Rice', owner='23456789', borrower='20837811', price='100.00', quantity='10')
    it9 = Item(item_name='Car', owner='23456789', borrower='24526811', price='850000.00', quantity='1')
    it10 = Item(item_name='Unga', owner='23456789', borrower='24526811', price='120.00', quantity='8')
    it11 = Item(item_name='Body Oil', owner='23456789', borrower='13727811', price='220.00', quantity='1')
    it12 = Item(item_name='Diapers', owner='23456789', borrower='13727811', price='50.00', quantity='5')

    db.session.add(it1)
    db.session.add(it2)
    db.session.add(it3)
    db.session.add(it4)
    db.session.add(it5)
    db.session.add(it6)
    db.session.add(it7)
    db.session.add(it8)
    db.session.add(it9)
    db.session.add(it10)
    db.session.add(it11)
    db.session.add(it12)

    # Shop owners
    test_user = User(full_name='John Matrix', idnumber='12345678', phone='0798283876', password='test')
    test_user1 = User(full_name='Adan Abdi', idnumber='23456789', phone='0100000000', password='test1')

    db.session.add(test_user)
    db.session.add(test_user1)
    db.session.commit()
    print('DB Seeded!')


# Set jwt
@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'message': 'The {} token has expired'.format(token_type)
    }), 401


@app.route('/')
def index():
    response = {
        'message': 'Welcome to Kitabu API Server.',
        'version': '1.0.0',
        'author': 'John Simiyu',
        'email': 'jonnyeinstein@gmail.com'
    }

    return jsonify(response), 200


# Log In
@app.route('/get_token', methods=['POST'])
def get_token():
    if request.is_json:
        idnumber = request.json['idnumber']
        password = request.json['password']
    else:
        idnumber = request.form['idnumber']
        password = request.form['password']
    test = User.query.filter_by(idnumber=idnumber, password=password).first()
    if test:
        expires = datetime.timedelta(hours=864000)
        access_token = create_access_token(identity=idnumber, expires_delta=expires)
        return jsonify(expires='8640000', access_token=access_token)
    else:
        return jsonify(message='Wrong credentials!'), 401


# Register new User
@app.route("/register/user", methods=['POST'])
def register():
    data = request.get_json()
    if data['full_name'] and data['idnumber'] and data['phone'] and data['password']:
        existing_user = User.query.filter_by(idnumber=data['idnumber']).first()
        if existing_user is not None:
            response = {
                'message': 'User already exists'
            }
            return jsonify(response), 403

        new_user = User(full_name=data['full_name'], idnumber=data['idnumber'], phone=data['phone'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        response = {
            'message': 'New user registered'
        }
        return jsonify(response), 201
    else:
        response = {
            'status': 'error',
            'message': ['bad request body']
        }
        return jsonify(response), 400

# Register new Creditor
@app.route("/register/creditor", methods=['POST'])
@jwt_required
def registeru():
    data = request.get_json()
    owner = get_jwt_identity()
    if data['full_name'] and data['idnumber'] and data['phone']:
        existing_creditor = Creditor.query.filter_by(idnumber=data['idnumber']).first()
        if existing_creditor is not None:
            response = {
                'message': 'Creditor already exists'
            }
            return jsonify(response), 403

        new_creditor = Creditor(owner=owner, full_name=data['full_name'], idnumber=data['idnumber'], phone=data['phone'])
        db.session.add(new_creditor)
        db.session.commit()
        response = {
            'message': 'New creditor registered'
        }
        return jsonify(response), 202
    else:
        response = {
            'status': 'error',
            'message': ['bad request body']
        }
        return jsonify(response), 400


# View My Profile
@app.route("/user/details", methods=['GET'])
@jwt_required
def get_user_details():
    idnumber = get_jwt_identity()
    user = User.query.filter_by(idnumber=idnumber).first()
    if user is None:
        response = {
            'message': 'User does not exist'
        }
        return jsonify(response), 404
    result = user_schema.dump(user)
    return jsonify(result), 202


# View One Creditor Profile
@app.route("/creditor/<creditorid>", methods=['GET'])
@jwt_required
def get_creditor_details(creditorid):
    idnumber = get_jwt_identity()
    creditor = Creditor.query.filter_by(owner=idnumber, idnumber=creditorid).first()
    if creditor is None:
        response = {
            'message': 'Creditor does not exist'
        }
        return jsonify(response), 404
    result = creditor_schema.dump(creditor)

    return jsonify(result), 202


# View Creditors Profile
@app.route("/creditors", methods=['GET'])
@jwt_required
def get_creditors_details():
    idnumber = get_jwt_identity()
    creditor = Creditor.query.filter_by(owner=idnumber).all()
    if creditor is None:
        response = {
            'message': 'No Creditors Found'
        }
        return jsonify(response), 404
    result = creditors_schema.dump(creditor)
    return jsonify(result), 200


# Add new items to creditor
@app.route("/<creditorid>/add_item", methods=['POST'])
@jwt_required
def add_item(creditorid):
    data = request.get_json()
    idnumber = get_jwt_identity()
    creditor = Creditor.query.filter_by(owner=idnumber, idnumber=creditorid).first()
    if creditor:
        if data['item_name'] and data['price'] and data['quantity']:

            price = float(data['price'])
            quantity = float(data['quantity'])
            total = price * quantity
            creditor.debt = creditor.debt + total
            db.session.commit()

            new_item = Item(borrower=creditorid, item_name=data['item_name'], price=data['price'], quantity=data['quantity'], owner=idnumber)
            db.session.add(new_item)
            db.session.commit()

            response = {
                'message': 'Item added successfully to creditor.'
            }
            return jsonify(response), 202
        else:
            response = {
                'status': 'error',
                'message': 'bad request body'
            }
            return jsonify(response), 400
    else:
        response = {
            'status': 'error',
            'message': 'No Such Creditor or Create a new Creditor!'
        }
        return jsonify(response), 404


# View Items to a Creditor
@app.route("/<creditorid>/items", methods=['GET'])
@jwt_required
def get_creditor_items(creditorid):
    idnumber = get_jwt_identity()
    items = Item.query.filter_by(owner=idnumber, borrower=creditorid).all()
    if items:
        result = items_schema.dump(items)
    return jsonify(result), 202


# View loaned user items
@app.route("/items", methods=['GET'])
@jwt_required
def get_user_items():
    idnumber = get_jwt_identity()
    items = Item.query.filter_by(owner=idnumber).all()
    if items:
        result = items_schema.dump(items)
        return jsonify(result)
    else:
        return jsonify(message='No items found'), 404


# endpoint to update user
@app.route("/user", methods=["PUT"])
@jwt_required
def user_update():
    idnumber = get_jwt_identity()
    data = request.get_json()
    user = User.query.filter_by(idnumber=idnumber).first()
    new_name = data['full_name']
    new_phone = data['phone']

    user.full_name = new_name
    user.phone = new_phone

    db.session.commit()
    return user_schema.jsonify(user)

# Get transactions of Creditor
@app.route("/<creditorid>/payments", methods=['GET'])
@jwt_required
def get_creditor_payments(creditorid):
    idnumber = get_jwt_identity()
    payments = Tx.query.filter_by(owner=idnumber, creditorid=creditorid).all()
    if payments:
        result = txs_schema.dump(payments)
    return jsonify(result), 202

# Create payment
@app.route("/<creditorid>/pay", methods=['POST'])
@jwt_required
def create_payment(creditorid):
    idnum = get_jwt_identity()
    data = request.get_json()
    creditor = Creditor.query.filter_by(owner=idnum, idnumber=creditorid).first()
    if creditor:
        if data['amount']:

            new_tx = Tx(creditorid=creditorid, amount=data['amount'], owner=idnum)
            db.session.add(new_tx)
            db.session.commit()
            oldDebt = creditor.debt
            pay = data['amount']
            creditor.debt = oldDebt - pay
            db.session.commit()
            response = {
                'message': 'Transaction successfull.'
            }
            return jsonify(response), 202
        else:
            response = {
                'status': 'error',
                'message': 'bad request body'
            }
            return jsonify(response), 400
    else:
        response = {
            'status': 'error',
            'message': 'No Such Creditor or Create a new Creditor!'
        }
        return jsonify(response), 404


# endpoint to update creditor
@app.route("/creditor/<creditorid>", methods=["PUT"])
@jwt_required
def creditor_update(creditorid):
    userid = get_jwt_identity()
    # data = request.get_json()
    creditor = Creditor.query.get(idnumber=creditorid, owner=userid)
    if creditor:
        new_name = request.json['full_name']
        new_phone = request.json['phone']
        new_debt = request.json['debt']
        new_id = request.json['idnumber']

        creditor.full_name = new_name
        creditor.phone = new_phone
        creditor.idnumber = new_id
        creditor.debt = new_debt

        db.session.commit()
        return creditor_schema.jsonify(creditor), 202
    else:
        return jsonify(message='No such creditor'), 404


# endpoint to update item
@app.route("/<creditorid>/item", methods=["PUT"])
@jwt_required
def item_update(creditorid):
    userid = get_jwt_identity()
    item = Item.query.get(borrower=creditorid, owner=userid)
    if item:
        new_name = request.json['item_name']
        new_price = request.json['price']
        new_quantity = request.json['quantity']

        item.item_name = new_name
        item.price = new_price
        item.quantity = new_quantity

        db.session.commit()
        return item_schema.jsonify(item), 202
    else:
        return jsonify(message='No item found!'), 404


if __name__ == '__main__':
    app.run(port='7500')
