from dotenv import load_dotenv
import os

load_dotenv()

class Env:

    def __init__(self):
        self.LinkedIn_USER_NAME = os.getenv('LinkedIn_USER_NAME')
        self.LinkedIn_PASSWORD = os.getenv('LinkedIn_PASSWORD')
        self.MINIMUM_ACCEPTABLE_PAY = os.getenv('MINIMUM_ACCEPTABLE_PAY')
        self.URL = os.getenv('URL')
        self.CHATGPT_API_KEY = os.getenv('CHATGPT_API_KEY')
        self.TOTAL_YEARS_OF_EXPERIENCE = os.getenv('TOTAL_YEARS_OF_EXPERIENCE')
