from sanic.router import Router
from .payment import payment_webhook, buy_product, get_transaction_history
from .admin import UsersView
from .users import get_accounts_and_history, get_products
from .products import ProductsView
from .exceptions import validation_error_handler, db_error_handler
from sanic.handlers import ErrorHandler
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sanic import Blueprint

router = Router()
error_handler = ErrorHandler()

error_handler.add(ValidationError, validation_error_handler)
error_handler.add(IntegrityError, db_error_handler)

# Зачисление средств
router.add('/payment/webhook', ['POST'], payment_webhook)
# Покупка товара
router.add('/buy_product/<product_id:int>', ['POST'], buy_product)

# Admin endpoints
admin_bp = Blueprint('admin', url_prefix='/admin')
# Все пользователи и их счета
admin_bp.add_route(UsersView.as_view(), '/users', ['GET'])
# Включить/отключить юзера
admin_bp.add_route(UsersView.as_view(), r'/user/<user_id:int>/<activation:disable|enable>', ['POST'])
# Изменение товара
admin_bp.add_route(ProductsView.as_view(), '/products/<product_id:int>', ['PATCH', 'GET', 'DELETE'])
# Получение всех товаров и добавление товара
admin_bp.add_route(ProductsView.as_view(), '/products', ['GET', 'POST'])


my_bp = Blueprint('my', url_prefix='/my')
# Просмотр баланса и получение истории транзакций
my_bp.add_route(get_accounts_and_history, '/accounts', ['GET'])
my_bp.add_route(get_transaction_history, '/accounts/<account_id:int>/transactions', ['GET'])
my_bp.add_route(get_products, '/products', ['GET'])
