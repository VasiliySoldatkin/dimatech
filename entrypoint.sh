set -e;
make
python3 main.py
exec "$@"