import json
from dotenv import load_dotenv
from bitrix24 import *
import requests
import os

load_dotenv(".env")
AIRTABLE_ID = os.environ.get('AIRTABLE_ID')
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME')

gettask = f"https://api.airtable.com/v0/{AIRTABLE_ID}/{AIRTABLE_TABLE_NAME}?maxRecords=100&view=Grid%20view"
endpoint = f'https://api.airtable.com/v0/{AIRTABLE_ID}/{AIRTABLE_TABLE_NAME}'

headers = {
	"Authorization": "Bearer keyLgbuhgVncLROSM",
	"Content-Type": "application/json"
}
bx24 = Bitrix24('https://viantec.bitrix24.ru/rest/225/0v2d2xg0tq5q5og1/')

def add_data(mass, air_task_id = 0):
	keys = ['Название',"Дедлайн","Постановщик","Ответсвенный","Приоритет","id","Статус"]
	value = ['title', 'deadline','creator','responsible','description','id','priority','status']
	fields = {}
	j = 0
	for i in keys:
		if j > 1 and j < 4:
			if mass[value[j]]['name'] != None:
				fields[i]= mass[value[j]]['name']
		elif j == 2:
			t = mass['deadline'].find('T')
			if mass[value[j]] != None:
				fields[i] = mass[value[j]][:t]
		else:
			if mass[value[j]] != None:
				fields[i] = mass[value[j]]
		j += 1
	data = {
		"records": [{
		"fields" : fields}
			]}
	if air_task_id != 0:
		data = {
			"records": [{
			"id" : air_task_id,
			"fields": fields
		}]}
	return data


def push_task(id, air_task_id = 0):
	mass = bx24.callMethod('tasks.task.get', taskId=id)['task']
	print(mass)
	data = add_data(mass, air_task_id)
	# t = mass['deadline'].find('T')
	# data = {
	# 	"records": [
	# 		{
	# 			"fields": {
	# 				"Название": mass['title'],
	# 				"Дедлайн": mass['deadline'][:t],
	# 				"Постановщик": mass['creator']['name'],
	# 				"Ответсвенный": mass['responsible']['name'],
	# 				"Описание": mass['description'],
	# 				"id": mass['id'],
	# 				"Приоритет": mass['priority'],
	# 				"Статус": mass['status']
	# 			}
	# 		}
	# 	]
	# }
	# data_update = {
	# 	"records": [
	# 		{
	# 			"id": air_task_id,
	# 			"fields": {
	# 				"Название": mass['title'],
	# 				"Дедлайн": mass['deadline'][:t],
	# 				"Постановщик": mass['creator']['name'],
	# 				"Ответсвенный": mass['responsible']['name'],
	# 				"Описание": mass['description'],
	# 				"id": mass['id'],
	# 				"Приоритет": mass['priority'],
	# 				"Статус": mass['status']
	# 			}
	# 		}
	# 	]
	# }
	# print(data_update)
	r = requests.post(endpoint, json=data, headers=headers)
	print(r.status_code)
	print(r.text)


def delete_task(air_task_id):
	r = requests.request("DELETE", f'{endpoint}/{air_task_id[0]}', headers=headers)
	print("STATUS CODE REQUEST: ", r.status_code)
	print("TEXT REQUEST : ", r.text)


def get_airtable(id, delete = False):
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