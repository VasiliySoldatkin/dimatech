from sanic.router import Router
from .payment import payment_webhook, buy_product, get_transaction_history
from .admin import get_users_with_accounts, control_user
from .users import get_accounts_and_history
from .products import ProductsView
from .exceptions import validation_error_handler, db_error_handler
from sanic.handlers import ErrorHandler
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
# Сделать через blueprint

router = Router()
error_handler = ErrorHandler()
error_handler.add(ValidationError, validation_error_handler)
error_handler.add(IntegrityError, db_error_handler)

router.add('/payment/webhook', ['POST'], payment_webhook)

router.add('/products/<product_id:int>', ['PATCH', 'GET', 'DELETE'], ProductsView.as_view())
router.add('/products', ['GET', 'POST'], ProductsView.as_view())
router.add('/users', ['GET'], get_users_with_accounts)
router.add('/buy_product/<product_id:int>', ['POST'], buy_product)
router.add('/accounts/<account_id:int>/transactions', ['GET'], get_transaction_history)
router.add(r'/user/<user_id:int>/<activation:disable|enable>', ['POST'], control_user)
router.add('/my/accounts', ['GET'], get_accounts_and_history)