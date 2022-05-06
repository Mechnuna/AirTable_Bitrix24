import json
from dotenv import load_dotenv
from bitrix24 import *
import requests
import os

load_dotenv(".env")
AIRTABLE_ID = os.environ.get('AIRTABLE_ID')
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME')
BITRIX_LINK = os.environ.get('BITRIX_LINK')

gettask = f"https://api.airtable.com/v0/{AIRTABLE_ID}/{AIRTABLE_TABLE_NAME}?maxRecords=100&view=Grid%20view"
endpoint = f'https://api.airtable.com/v0/{AIRTABLE_ID}/{AIRTABLE_TABLE_NAME}'

headers = {
	"Authorization": f"Bearer {AIRTABLE_API_KEY}",
	"Content-Type": "application/json"
}
bx24 = Bitrix24(BITRIX_LINK)


def print_request(r):
	print("STATUS CODE REQUEST: ", r.status_code)
	print("TEXT REQUEST : ", r.text)


def add_data(mass, air_task_id=0):
	keys = ['Название', "Дедлайн", "Постановщик", "Ответсвенный", "Описание", "id", "Приоритет", "Статус"]
	value = ['title', 'deadline', 'creator', 'responsible', 'description', 'id', 'priority', 'status']
	fields = {}
	j = 0
	for i in keys:
		if 1 < j < 4:
			fields[i] = mass[value[j]]['name']
		elif j == 1:
			if mass[value[j]] != None:
				t = mass['deadline'].find('T')
				fields[i] = mass[value[j]][:t]
		else:
			fields[i] = mass[value[j]]
		j += 1
	data = {
		"records": [{
			"fields": fields}
		]}
	if air_task_id != 0:
		data["records"][0]["id"] = air_task_id
	return data


def push_task(id, air_task_id=0):
	mass = bx24.callMethod('tasks.task.get', taskId=id)['task']
	print(mass)
	data = add_data(mass, air_task_id)
	print("DATA", data)
	if air_task_id != 0:
		r = requests.patch(endpoint, json=data, headers=headers)
	else:
		r = requests.post(endpoint, json=data, headers=headers)
	print_request(r)


def delete_task(air_task_id):
	r = requests.request("DELETE", f'{endpoint}/{air_task_id[0]}', headers=headers)
	print_request(r)


def get_airtable(id, delete=False):
	r = requests.get(gettask, headers=headers)
	js = json.loads(r.text)['records']
	for i in range(len(js)):
		if js[i]['fields']['id'] == str(id):
			if delete:
				delete_task([js[i]['id']])
			else:
				push_task(int(id), js[i]['id'])
			break
	else:
		push_task(int(id), 0)


get_airtable(13243)
