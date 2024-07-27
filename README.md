# Password-Manager
Password generator and manager

# Usage
git clone https://www.github.com/deenovee/password-manager.git

cd password-manager

python3 -m venv venv

. venv\Scripts\Activate

pip3 install -r requirements.txt

python3 main.py

# Powershell
To use the powershell script to run the password manager replace the path with the correct path for the python script then create a desktop icon for the powershell script.

# Data Protection
All passwords and emails are encrypted using Fernet and decrypted when ViewFrame is called. The phrases and pins used to generate passwords are also encrypted using Fernet and only decrypted during the process of creating a password. The passphrase used to unlock the app at runtime is hashed using bcrypt and saved in .env as a hashed string. When the user enters the passphrase the hash of the entry is compared with the hashed string in the .env file. 


