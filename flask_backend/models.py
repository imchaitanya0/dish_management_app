from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Dish(db.Model):
    dish_id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            'dish_id': self.dish_id,
            'dish_name': self.dish_name,
            'image_url': self.image_url,
            'is_published': self.is_published
        }