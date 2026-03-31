import json

filename = 'users_information.json'
file2 = 'login.json'

users_information = {}
login = {}

try:
	with open(filename) as f:
		users_information = json.load(f)
except FileNotFoundError as e:
	print(e)
try:
	with open(file2) as f:
		login = json.load(f) 
except FileNotFoundError as e:
	print(e)

def deposit(amount=0):
	for user in users_information:
		if not login[user]:
			return False
		new_balance = users_information[user]['balance'] = users_information[user].get('balance',0) + amount
		users_information[user]['balance'] = new_balance
		return True

def banking_pin(pin = '0000'):
	pin = str(pin)
	if pin == '1234':
		print(f'"{pin}" is not a safe password, choose another')
		return False
	if len(pin) != 4:
		print('pin must be exactly 4 numbers')
		return False
	if not pin.isdigit():
		return False
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

print(users_information)
print(login)