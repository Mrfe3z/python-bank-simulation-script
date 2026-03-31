import json

users_information = {}
login = {}

filename = 'users_information.json'
try:
	with open(filename) as f:
		users_information = json.load(f)
except FileNotFoundError as e:
	print(e)

try:
	with open('login.json') as f:
		login = json.load(f)
except FileNotFoundError as e:
	print(e)

def valid_password(password):
	if len(password) < 8:
		print('password can not be less than 8 characters')
		return False

	has_upper, has_lower, has_num = False, False, False
	for char in password:
		if char.isupper():
			has_upper = True
		if char.islower():
			has_lower = True
		if char.isdigit():
			has_num = True

	return has_upper and has_lower and has_num

def signup(users_information, login, username, password, firstname, lastname, balance = 0):
	if username in users_information:
		print('sorry that username already exists')
		return False

	if not valid_password(password):
		print('enter a valid password')
		return False

	users_information[username] = {

	'password': password,
	'firstname': firstname.upper(),
	'lastname': lastname.upper(),
	'balance': balance
	
	}

	login[username] = False
	with open(filename, 'w') as f:
		json.dump(users_information,f, indent=4)
	with open('login.json', 'w') as f:
		json.dump(login, f, indent=4)

def log_in(users_information, username, password):
	if username not in users_information:
		print('new user detected, please provide the following details')
		firstname = input('enter first name: ')
		lastname = input('enter last name: ')
		signup(users_information, login, username, password, firstname, lastname)
		
		return False

	if users_information[username]['password'] != password:
		print('invalid or wrong password!, try again')
		return False

	login[username] = True

def deposit(amount=0):
	for user in users_information:
		if not login[user]:
			return False
		new_balance = users_information[user]['balance'] = users_information[user].get('balance',0) + amount
		users_information[user]['balance'] = new_balance
		return True

def create_banking_pin(pin = 0000):
	for user in users_information:
		if not login[user]:
			return False

		pin = str(pin)
		if pin == '1234':
			print(f'"{pin}" is not a safe password, choose another')
			return False
		if len(pin) != 4:
			print('pin must be exactly 4 numbers')
			return False
		if not pin.isdigit():
			return False
		users_information[user]["pin"] = pin
		return True


def transfer(amount, userA, userB):
	for user in users_information:
		if not login[user]:
			return False
		if userB not in users_information:
			print('user does not exist')
			return False

		new_balance = users_information[userA].get('balance', 0) - amount
		if new_balance < 0:
			return False

		users_information[userB] = users_information[userB].get('balance', 0) + amount

		users_information[userA]['balance'] = new_balance
		print(users_information)
		return True

def main():
	print('||----HAFIZ TEST BANKING-----||')
	print(' ')
	print('''options:
		option 1: login 
		option 2: signup
		option 3: quit
		''')
	# choice = input("choose option:\n ")

	while True:
		choice = input("choose option:\n ")
		if choice == '1':
			print('||--LOG-IN--||')
			print('')
			username = input('enter username: ')
			password = input('enter password: ')
			print('')
			log_in(users_information, username, password)
			if login[username]:
				print(f'Welcome {(username).upper()}')
				print('')

				print('what would you like to do today?: ')
				print('''options:
					option 1: 'transfer'
					option 2: 'check balance'
					option 3: 'deposit'
					option 4: log out
					''')

				while True:
					choice = input("--choose option:\n ")
					if choice == '1':
						print('--TRANSFER--')
						amount = input(' enter transfer amount: ')
						receipient = input('enter receiver\'s username: ') 
					elif choice == '2':
						print('--BALANCE--')
						print(f'your available balance is {users_information[username].get('balance')}'.capitalize())
					elif choice == '4':
						print('--DEPOSIT--')
						amount = input('enter deposit amount:')
					elif choice == '4':
						print('logged out successfully')
						login[username] = False
						break


		

		elif choice == '2':
			print('||--SIGN-UP--||')
			print(' ')

			print('enter the following to create an account')

			username = input('enter username: ')
			password = input('enter password: ')
			firstname = input('enter first name: ')
			lastname = input('enter last name: ')

			main = signup(users_information, login, username, password, firstname, lastname)

		elif choice == '3':
			print('THANKS FOR BANKING WITH US. GOODBYE!')
			break
	print(users_information, login)

if __name__ == '__main__':
	main()