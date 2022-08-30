from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length


class ProductSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(default='Empty Description')
    price = fields.Float(required=True)

    @validates('price')
    def validate_price(self, value):
        if value < 0:
            raise ValidationError("Price can't be less than 0")


class PaymentSchema(Schema):
    user_id = fields.Integer(required=True)
    bill_id = fields.Integer(required=True)
    amount = fields.Float(required=True)

    @validates('amount')
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError("Amount can't be less or equal 0")


class UserSchema(Schema):
    user_id = fields.Integer()
    login = fields.Str()
    account_id = fields.Integer()


class RegisterSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)


class BuyProductSchema(Schema):
    account_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)