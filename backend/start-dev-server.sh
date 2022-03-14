
pip install -e . 
gunicorn -w 1 -k uvicorn.workers.UvicornWorker src.app.main:api --reload -b 0.0.0.0:8000