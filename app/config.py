import dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR,'.env'))

def to_bool(s):
    r = False 
    if(s.lower() == "true"):
        r = True
    elif(s.lower() == "false"):
        r = False
    return r

class Config():
    DEBUG = to_bool(os.environ.get("DEBUG"))
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_ENABLE = os.environ.get("WTF_CSRF_ENABLE")
    PER_PAGE = int(os.environ.get("PER_PAGE"))