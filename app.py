#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests
import time
import sys

vk_l = 'https://api.vk.com/method/'
vk_t = '&access_token=' + '779d5aa3302cc6c775706d8b927ea893775c3a78276c397031b4781e88e4d8734efa3739573ac56535210' + '&v=' + '5.52'

vkStat = ''
vkStatOld = ''
msgTs = 0
msgPts = 0
leavs = []

def getParams():
	global msgTs
	global msgPts
	try:
		r = requests.get(vk_l + 'messages.getLongPollServer?need_pts=1' + vk_t).json()
		time.sleep(0.4)
		try:
			msgTs = r['response']['ts']
			print('new ts = ' + str(msgTs))
			msgPts = r['response']['pts']
		except:
			try:
				print("Ошибка на стороне VK (метод getParams): " + r['error']['error_msg'])
			except:
				print(r)
	except:
		print('Ошибка подключения к VK (getParams)')
		
def listenMsg():
	global msgTs
	global msgPts
	global leavs
	try:
		r = requests.get(vk_l + 'messages.getLongPollHistory?ts=' + str(msgTs) + '&pts=' + str(msgPts) + vk_t).json()
		time.sleep(0.4)
		try:
			try:
				for i in r['response']['messages']['items']:
					if i['chat_id']:
						if str(i['user_id']) == '122734122':
							if str(i['body'].lower()) == 'leave':
								print('add leave chat ' + str(i['chat_id']))
								leavs.append(i['chat_id'])
							else:
								try:
									if str(i['action']) == 'chat_invite_user':
										if str(i['action_mid']) == '122734122':
											for k in leavs:
												if k == i['chat_id']:
													print('remove leave chat ' + str(i['chat_id']))
													leavs.remove(i['chat_id'])
								except:
									pass
			except:
				print('Ошибка при переборе сообщений')
			try:
				for k in r['response']['messages']['items']:
					if i['chat_id']:
						for j in leavs:
							if j == k['chat_id']:
								getOut(k['chat_id'], '122734122')
								time.sleep(0.4)
			except:
				print('Ошибка при переборе и выхода из беседы')
			try:
				if msgPts != r['response']['new_pts']:
					msgPts = r['response']['new_pts']
			except:
				print('Ошибка при обновлении pts')
		except:
			print('Ошибка в методе listenMsg')
			try:
				print("Ошибка на стороне VK: (метод listenMsg)" + str(r['error']['error_msg']))
			except:
				pass
	except:
		print('Ошибка подключения к VK (listenMsg)')
		raise
	
def getOut(cid, uid):
	try:
		print('Выход из беседы ' + str(cid))
		r = requests.get(vk_l + 'messages.removeChatUser?chat_id=' + str(cid) + '&user_id=' + str(uid) + vk_t).json()
	except:
		print('Ошибка подключения к VK (getOut)')

getParams()
while True:
	listenMsg()