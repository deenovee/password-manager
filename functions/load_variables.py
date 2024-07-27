import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet


class Variables:

    def check_passphrase(self):
        load_dotenv()
        # Check if PASSPHRASE variable exists
        passphrase = os.getenv('PASSPHRASE')

        if not passphrase:
            return ''

        return passphrase.encode()

    def check_key(self):
        load_dotenv()
        # Check if KEY variable exists
        key = os.getenv('KEY')
        if not key:
            # If KEY is missing, generate encryption key using Fernet
            key = Fernet.generate_key().decode()

            # Save key to .env file
            with open('.env', 'a') as f:
                f.write(f'KEY={key}\n')

        return key.encode()  # Encode key as bytes object

