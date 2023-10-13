from dotenv import load_dotenv
import os

load_dotenv()

algorithum = os.environ.get("algorithum")

sender_email = os.environ.get("sender_email")
SECRET_KEY = os.environ.get("SECRET_KEY")
gst_number = os.environ.get("gst_number")
organisation_name = os.environ.get('company_name')