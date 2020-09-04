import json
from datetime import date, datetime
import random
import requests
import pytz
import csv
import schedule
import time

timezone = pytz.timezone("Asia/Singapore")

def main():
	groupCode = ""

	with open('subscribers.csv', newline='') as csvfile:
		file = csv.reader(csvfile, delimiter=',')
		for subscribers in file:
			subscribers = subscribers


	d = datetime.now()
	d_aware = timezone.localize(d)
	d_aware.tzinfo

	day = date.strftime(d, '%d/%m/%Y')
	schedule.every().day.at("08:00").do(automate_temp,'AM', subscribers, groupCode, day)
	schedule.every().day.at("16:00").do(automate_temp,'PM', subscribers, groupCode, day)
	schedule.every().day.at("20:00").do(automate_temp,'PM', subscribers, groupCode, day)

	while True:
		schedule.run_pending()
		time.sleep(60)  # wait one minute

def send_temp(groupCode, day, meridies, memberId, temperature,pin):
	url = 'https://temptaking.ado.sg/group/MemberSubmitTemperature'
	data = {'groupCode': groupCode, 'date': day, 'meridies': meridies, 'memberId': memberId, 'temperature': temperature,'pin': pin}
	x = requests.post(url, data)
	print(x.text)

def automate_temp(meridies, subscribers, groupCode, day):
	for subscriber in subscribers:
		temperature = float("36." + str(random.randrange(10)))
		send_temp(groupCode, day, meridies, subscriber, temperature, "0000")

main()