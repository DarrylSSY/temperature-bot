from datetime import date, datetime
import random
import requests
import pytz
import csv
import schedule
import time

timezone = pytz.timezone("Asia/Singapore")

def main():

	schedule.every().day.at("07:50").do(load_subscribers)
	schedule.every().day.at("08:00").do(automate_temp,'AM')
	schedule.every().day.at("15:50").do(load_subscribers)
	schedule.every().day.at("16:00").do(automate_temp,'PM')
	while True:
		schedule.run_pending()
		time.sleep(60)  # wait one minute

def send_temp(groupCode, day, meridies, memberId, temperature,pin,name):

	url = 'https://temptaking.ado.sg/group/MemberSubmitTemperature'
	data = {'groupCode': groupCode, 'date': day, 'meridies': meridies, 'memberId': memberId, 'temperature': temperature,'pin': str(pin)}
	x = requests.post(url, data)
	print("Attempting to submit temperature of " + str(temperature) + " to " + meridies + " of " + str(day) + " for member " + str(name))
	print(x.text)

def automate_temp(meridies):
	with open('subscribers.csv', newline='') as csvfile:
		file = csv.reader(csvfile, delimiter=',')
		subscribers = []
		next(file)
		for user in file:
			subscribers.append(user)
	d = datetime.now()
	d_aware = timezone.localize(d)
	d_aware.tzinfo

	day = date.strftime(d, '%d/%m/%Y')
	for subscriber in subscribers:
		temperature = float("36." + str(random.randrange(10)))
		send_temp(subscriber[1], day, meridies, subscriber[2], temperature, str(subscriber[3]),str(subscriber[4]))

def load_subscribers():
	response = requests.get(
		'https://docs.google.com/spreadsheet/ccc?key=1pc3XGJYDntAeQ3k94hICj1WIaE7vnkoZHitAysxY-es&output=csv')
	assert response.status_code == 200, 'Wrong status code'
	with open('subscribers.csv', "wb") as f:
		f.write(response.content)




main()
