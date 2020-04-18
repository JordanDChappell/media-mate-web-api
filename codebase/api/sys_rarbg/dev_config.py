import os
from cryptography.fernet import Fernet

# Set up environment secret values and Fernet encryption
SECRET = os.getenv('SECRET')
f = Fernet(SECRET)

config = {
  'version': '/v1.0',
  'password': (f.decrypt(b"gAAAAABelQM6BT_HTPzQUNWcxNQ7ViNPg596ulitO4Y2nAAzRTjSpBNHzoOdq2KB_HIAoEXqm3WnHdwi96JuYC9lwtdX_Y_STw==")).decode('utf-8')
}