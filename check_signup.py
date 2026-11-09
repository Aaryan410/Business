from getpass import getpass

from backend.accounts import create_account

username = input("Choose a username: ")
password = getpass("Choose a password: ")

try: 
    account = create_account(username, password)
    print(f"Created account for {account['username']}")
except ValueError as error:
    print(error)