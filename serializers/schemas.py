from marshmallow import Schema, fields, validates, ValidationError


class ProductSchema(Schema):
    title = fields.String(required=True)
    price = fields.Float(required=True)


class PaymentSchema(Schema):
    user_id = fields.Integer(required=True,  # проверить, правильно ли будет выводиться error_message в случае с String
                             error_messages={"required": {"user_id": "user_id is required", "code": 400}})
    bill_id = fields.Integer(required=True,
                             error_messages={"required": {"bill_id": "bill_id is required", "code": 400}})
    amount = fields.Float(required=True,
                          error_messages={"required": {"amount": "amount is required", "code": 400}})

    @validates('amount')
    def validate_amount(self, value):
        # Проверить можно ли как-то передавать dict в ValidationError (мб через data)
        if value <= 0:
            raise ValidationError("Amount can't be less or equal 0")


class UserSchema(Schema):
    user_id = fields.Integer()
    login = fields.Str()  # Должен быть уникальным и не более 100
    account_id = fields.Integer()


class RegisterSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)


class BuyProductSchema(Schema):
    account_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    amount = fields.Float(required=True)
