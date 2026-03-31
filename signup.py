import json

users_information = {}
login = {}

filename = 'users_information.json'
session_file = 'login.json'
try:
	with open(filename) as f:
		users_information = json.load(f)
except FileNotFoundError as e:
	print(e)

try:
	with open(session_file) as f:
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
	with open(filename, 'W') as f:
		json.dump(users_information,f, indent=4)
	with open(session_file, 'W') as f:
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

def deposit(users_information,login, username, amount=0):
	if not login[username]:
		print('please log in first!')
		return False

	pin_code = users_information[username].get('pin')

	if not pin_code:
		print('pin not set.')
		pin_prompt = input('create pin: y/n? ').lower()
		create_banking_pin(users_information,username, pin_prompt)
		return False

	trial = 3
	while trial > 0:
		entered_pin = input('enter your 4 digits pin to confirm: ')
		if entered_pin != pin_code:
			print(f'incorrect pin!!. {trial} more trials')
			trial -= 1
			print('')
			if trial == 0:
				print('pin does not match!!. ACCESS DENIED!!')
				break
				return False
		break		
	new_balance = users_information[username].get('balance',0) + int(amount)
	users_information[username]['balance'] = new_balance
	
	with open(filename, 'a') as f:
		json.dump(users_information, f, indent=4)
	print(" DEPOSIT SUCCESSFUL")

def create_banking_pin(users_information, username, pin = '0000'):
	if not login[username]:
		print('please log in first!')
		return False

	pin = input('create a 4 digit pin: ')
	if pin == '1234':
		print(f'"{pin}" is not a safe password, choose another')
		return False
	if len(pin) != 4:
		print('pin must be exactly 4 numbers')
		return False
	if not pin.isdigit():
		return False
	
	users_information[username]["pin"] = pin

	with open(filename,'a') as f:
		json.dump(users_information, f, indent=4)

	print('pin created successfully')
	return True

def transfer(users_information, amount, userA, userB):
	if not login[userA]:
		print('please log in first!')
		return False

	if userB not in users_information:
		print('user does not exist')
		return False

	pin_code = users_information[userA].get('pin')
	if not pin_code:
		print('pin not set.')
		return False

	amount = int(amount)

	trial = 3
	while trial > 0:
		entered_pin = input(f'enter your 4 digits pin to confirm the transfer of {amount} to {userB}: ')
		print('')

		if entered_pin != pin_code:
			print(f'incorrect pin!!' '{trial}\' more trials')
			print('')

			trial -= 1
		print('pin does not match!!. ACCESS DENIED!!')
		return False

	new_balance = users_information[userA].get('balance', 0) - amount
	if new_balance < 0:
		return False

	users_information[userB] = users_information[userB].get('balance', 0) + amount

	users_information[userA]['balance'] = new_balance
	# print(users_information)
	
	with open(filename,'a') as f:
		json.dump(users_information, f, indent=4)
	print('transfer successful.')
	return True

def main():

	print('||----HAFIZ TEST BANKING-----||')
	print(' ')
	option = ('''options:
		option 1: login 
		option 2: signup
		option 3: quit
		''')
	print(option)
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

			if login.get(username):
				print(f'Welcome {(username).upper()}')
				print('')

				print('what would you like to do today?: ')
				icons = ('''options:
					option 1: 'transfer'
					option 2: 'check balance'
					option 3: 'deposit'
					option 4: log out
					''')
				print(icons)

				while True:
					print(icons)
					choice = input("--choose option:\n ")
					if choice == '1':
						print('--TRANSFER--')
						amount = input(' enter transfer amount: ')
						receipient = input('enter receipient\'s username: ')
						print('')

						transfer(users_information, amount, username, receipient)

					elif choice == '2':
						print('--BALANCE--')
						print(f'your available balance is {users_information[username].get('balance')}'.capitalize())
						print('')
					
					elif choice == '3':
						print('--DEPOSIT--')
						amount = input(' enter Deposit amount: ')
						print('')
						balance = deposit(users_information, login, username, amount)
						print(balance)

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