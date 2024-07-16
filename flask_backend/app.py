from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from models import db, Dish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dishmanager:dishes123@localhost/dish_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

db.init_app(app)

@app.route('/api/dishes', methods=['GET'])
def get_dishes():
    dishes = Dish.query.order_by(Dish.dish_id).all()
    return jsonify([dish.to_dict() for dish in dishes])

@app.route('/api/dishes/<int:id>/toggle-publish', methods=['PUT'])
def toggle_publish(id):
    dish = Dish.query.get_or_404(id)
    dish.is_published = not dish.is_published
    db.session.commit()
    socketio.emit('dish_updated', dish.to_dict())
    return jsonify(dish.to_dict())

def populate_database():
    dishes = [
        Dish(dish_id=1, dish_name="Jeera Rice", image_url="https://nosh-assignment.s3.ap-south-1.amazonaws.com/jeera-rice.jpg", is_published=True),
        Dish(dish_id=2, dish_name="Paneer Tikka", image_url="https://nosh-assignment.s3.ap-south-1.amazonaws.com/paneer-tikka.jpg", is_published=True),
        Dish(dish_id=3, dish_name="Rabdi", image_url="https://nosh-assignment.s3.ap-south-1.amazonaws.com/rabdi.jpg", is_published=True),
        Dish(dish_id=4, dish_name="Chicken Biryani", image_url="https://nosh-assignment.s3.ap-south-1.amazonaws.com/chicken-biryani.jpg", is_published=True),
        Dish(dish_id=5, dish_name="Alfredo Pasta", image_url="https://nosh-assignment.s3.ap-south-1.amazonaws.com/alfredo-pasta.jpg", is_published=True)
    ]
    
    for dish in dishes:
        existing_dish = Dish.query.get(dish.dish_id)
        if not existing_dish:
            db.session.add(dish)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        populate_database()
    socketio.run(app, debug=True)