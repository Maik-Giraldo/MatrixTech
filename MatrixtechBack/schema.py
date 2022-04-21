from flask_marshmallow import Marshmallow

ma = Marshmallow()

class Schema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'last_name', 'email', 'phone_number', 'city', 'country')


schema = Schema()
schemas = Schema(many = True)