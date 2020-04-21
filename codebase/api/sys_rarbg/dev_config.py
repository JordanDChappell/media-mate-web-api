import os
from cryptography.fernet import Fernet

# Set up environment secret values and Fernet encryption
SECRET = os.getenv('SECRET')
f = Fernet(SECRET)

config = {
  'version': '/v1.0',
  'password': (f.decrypt(b"gAAAAABelQM6BT_HTPzQUNWcxNQ7ViNPg596ulitO4Y2nAAzRTjSpBNHzoOdq2KB_HIAoEXqm3WnHdwi96JuYC9lwtdX_Y_STw==")).decode('utf-8'),

  # TMDb API connection details
  'tmdbHost': 'https://api.themoviedb.org',
  'tmdbBaseUrl': '/3',
  'tmdbApiKey': (f.decrypt(b'gAAAAABenmgRCvuOcUKRL4awmDNviD47Yu4Jn41likGuKqgXgJ_cBWRgjPxlpEKR8UoPrAxyOb-l8sTgCH9K-imKl2R_Uc87prav7rTWAbnc1UzWcsC0hqp1v_ysULdL--7oN2xMttZ5')).decode('utf-8'),

  # TMDb poster path details
  'tmdbPosterBasePath': 'https://image.tmdb.org/t/p/',
  'tmdbPosterSize': 'w342'
}