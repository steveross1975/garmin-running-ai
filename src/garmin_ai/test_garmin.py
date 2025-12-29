import os

from dotenv import load_dotenv
from garminexport.garminclient import GarminClient

load_dotenv()
client = GarminClient(os.getenv("GARMIN_USERNAME"), os.getenv("GARMIN_PASSWORD"), "./data/fit/.garmin_session")
print("Available methods:", [m for m in dir(client) if not m.startswith('_')])
