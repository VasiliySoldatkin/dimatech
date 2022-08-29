migrate:
	alembic -c ./db/alembic/alembic.ini upgrade head \
	&& alembic -c ./db/alembic/alembic.ini revision --autogenerate