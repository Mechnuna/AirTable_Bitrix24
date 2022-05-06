# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import requests
import json

from flask import Flask, render_template
from flask import request
from post_func import *
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv(".env")
ADD = "ONTASKADD"
UPDATE = "ONTASKUPDATE"
TOKEN = os.environ.get("TOKEN")
DELETE = "ONTASKDELETE"
ID_BEFORE = 'data[FIELDS_BEFORE][ID]'
ID_AFTER = 'data[FIELDS_AFTER][ID]'


@app.route('/api', methods=['GET', 'POST'])
def result():
	r = request.form
	print(r)
	event = r.getlist('event')[0]
	print("EVENT: ", event)
	if event == DELETE:
		idTask = r.getlist(ID_BEFORE)[0]
	else:
		idTask = r.getlist(ID_AFTER)[0]
	print("ID TASK: ", idTask)
	token = r.getlist('auth[application_token]')[0]
	print(token)
	if token == TOKEN:
		if event == DELETE:
			get_airtable(idTask, True)
		else:
			get_airtable(idTask)
	return render_template('index.html', task=idTask, event=event)


@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	app.run()

