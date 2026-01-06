from app import app
from services.data_service import collect_and_store

with app.app_context():
    collect_and_store()
    print("System monitoring data saved")
