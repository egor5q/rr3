# -*- coding: utf-8 -*-
import os
import telebot
import time
import telebot
import random
from telebot import types
from pymongo import MongoClient
import threading

client1=os.environ['database']
client=MongoClient(client1)
db=client.channelsbase
users=db.users
channels=db.channels

   
bot=telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])   
    
@bot.message_handler(commands=['start'])
def start(m):
    if users.find_one({'id':m.from_user.id}) is None:
         users.insert_one(createuser(m.from_user.id,m.from_user.first_name,m.from_user.username))
    if m.from_user.id==m.chat.id:
        sendmenu(m.chat.id, m.from_user.id)
        
   
@bot.message_handler(commands=['addchannel'])
def addchannel(m):
    x=users.find_one({'id':m.from_user.id})
    if x['isadmin']==1:
        users.update_one({'id':m.from_user.id},{'$set':{'addingchannel':1}})
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('❌Отмена'))
        bot.send_message(m.chat.id, '''Напишите следующие данные о канале в таком формате (одним сообщением):\n\n
👤Рекламодатель;
📺Канал;
📊Подписчиков;
💶Цена;
💳Скидка (в процентах);
📗Тематика (Музыка/Блоги);
🔁Взаимный пиар;
📋Условия.

''',reply_markup=kb)
        
        
@bot.message_handler(commands=['delchannel'])
def addchannel(m):
    x=users.find_one({'id':m.from_user.id})
    if x['isadmin']==1:
        users.update_one({'id':m.from_user.id},{'$set':{'removingchannel':1}})
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('❌Отмена'))
        bot.send_message(m.chat.id, 'Чтобы удалить канал, напишите его юзернейм (@канал).',reply_markup=kb)


def sendmenu(chatid,userid):     
    users.update_one({'id':userid},{'$set':{'currentindex':0}})
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton('📮ПРОДАТЬ РЕКЛАМУ'))
    kb.add(types.KeyboardButton('МУЗЫКА'),types.KeyboardButton('БЛОГИ'))
    kb.add(types.KeyboardButton('КАНАЛЫ1'),types.KeyboardButton('КАНАЛЫ2'))
    kb.add(types.KeyboardButton('КАНАЛЫ3'),types.KeyboardButton('КАНАЛЫ4'))
    bot.send_message(chatid, '🏡Главное меню',reply_markup=kb)
        
        
@bot.message_handler()
def channelselect(m):
  if users.find_one({'id':m.from_user.id}) is not None:
    x=channels.find_one({})
    user=users.find_one({'id':m.from_user.id})
    if m.text=='▶':
        users.update_one({'id':user['id']},{'$inc':{'currentindex':3}})
        user=users.find_one({'id':m.from_user.id})
        y=x[user['currenttheme']]
        text=showchannels(user,y)
        kb=types.ReplyKeyboardMarkup()
        kb.add(types.KeyboardButton('◀'),types.KeyboardButton('▶'))
        if text!='':
            bot.send_message(m.chat.id, text, reply_markup=kb, resize_keyboard=True)
        else:
            users.update_one({'id':user['id']},{'$set':{'currentindex':0}})
            user=users.find_one({'id':m.from_user.id})
            y=x[user['currenttheme']]
            text=showchannels(user,y)
            kb=types.ReplyKeyboardMarkup()
            kb.add(types.KeyboardButton('◀'),types.KeyboardButton('▶'))
            bot.send_message(m.chat.id, text, reply_markup=kb,resize_keyboard=True)
            
    if m.text=='◀':
        users.update_one({'id':user['id']},{'$inc':{'currentindex':-3}})
        user=users.find_one({'id':m.from_user.id})
        if user['currentindex']<0:
            users.update_one({'id':user['id']},{'$set':{'currentindex':0}})
        user=users.find_one({'id':m.from_user.id})
        y=x[user['currenttheme']]
        text=showchannels(user,y)
        kb=types.ReplyKeyboardMarkup()
        kb.add(types.KeyboardButton('◀'),types.KeyboardButton('▶'))
        bot.send_message(m.chat.id, text, reply_markup=kb,resize_keyboard=True)
        
        
    if m.text=='МУЗЫКА':
        print('2')
        y=x['music']
        channel=0
        text=''
        users.update_one({'id':m.from_user.id},{'$set':{'currenttheme':'music'}})
        users.update_one({'id':m.from_user.id},{'$set':{'currentindex':0}})
        user=users.find_one({'id':m.from_user.id})
        
        text+=showchannels(user,y)
        
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('◀'),types.KeyboardButton('▶'))
        bot.send_message(m.chat.id, text, reply_markup=kb)
        
    if m.text=='Блоги':
        print('2')
        y=x['blogs']
        channel=0
        text=''
        users.update_one({'id':m.from_user.id},{'$set':{'currenttheme':'blogs'}})
        users.update_one({'id':m.from_user.id},{'$set':{'currentindex':0}})
        user=users.find_one({'id':m.from_user.id})
        
        text+=showchannels(user,y)
        
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('◀'),types.KeyboardButton('▶'))
        bot.send_message(m.chat.id, text, reply_markup=kb)
        
    if m.text=='❌Отмена':
        if user['addingchannel']==1:
            users.update_one({'id':m.from_user.id},{'$set':{'addingchannel':0}})
            bot.send_message(m.chat.id, 'Добавление канала отменено.')
            sendmenu(m.chat.id, m.from_user.id)
        if user['removingchannel']==1:
            users.update_one({'id':m.from_user.id},{'$set':{'removingchannel':0}})
            bot.send_message(m.chat.id, 'Удаление канала отменено.')
            sendmenu(id)
            
    user=users.find_one({'id':m.from_user.id})
    if user['addingchannel']==1:
      try:
        y=m.text.split('\n')
        print(y)
        reklamodatel=y[0]
        channel=y[1]
        subs=int(y[2])
        cost=int(y[3])
        discount=int(y[4])
        theme=nametotheme(y[5].lower())
        piar=y[6]
        conditions=y[7]
        #try:
        reklamodatel+=''
        channel+=''
        subs+=0
        cost+=0
        discount+=0
        theme+=''
        piar+=''
        conditions+=''
        channels.update_one({},{'$push':{theme:createchannel(reklamodatel,channel,subs,cost,discount,theme,piar,conditions)}})
        bot.send_message(m.chat.id, 'Канал успешно добавлен!')
        users.update_one({'id':m.from_user.id},{'$set':{'addingchannel':0}})
        sendmenu(m.chat.id, m.from_user.id)
      except:
           bot.send_message(m.chat.id, 'Неправильно введены аргументы для добавления канала!')
            
    if user['removingchannel']==1: 
        chn=None
        for ids in x:
          if ids!='_id':
            for idss in ids:
                print(ids)
                print(idss)
                if ids[idss]['channel']==m.text:
                    chn=ids[idss]
        if chn!=None:
            channels.remove({chn['theme']+'.channel':chn['channel']})
            bot.send_message(m.chat.id, 'Канал успешно удалён!')
        else:
            bot.send_message(m.chat.id, 'Такого канала не существует!')
        
    
        
           
                
def createchannel(reklamodatel,channel,subs,cost,discount,theme,piar,conditions):
    fcost=round(cost-(cost*(discount*0.01)),1)
    return{'reklamodatel':reklamodatel,
           'channel':channel,
           'subs':subs,
           'cost':cost,
           'discount':discount,
           'finalcost':fcost,
           'theme':theme,
           'piar':piar,
           'conditions':conditions
          }
    print(fcost)
                
    
def showchannels(user, y):
    channel=user['currentindex']
    text=''
    i=channel+3
    while channel<i:
      print('channel '+str(channel))
      print('i: '+str(i))
      try:
        ch=y[channel]
        text+='👤Рекламодатель: '+ch['reklamodatel']+'\n'
        text+='📺Канал: '+ch['channel']+'\n'
        text+='📊Подписчиков: '+str(ch['subs'])+'\n'
        text+='💶Цена: '+str(ch['cost'])+'\n'
        text+='💳Скидка: '+str(ch['discount'])+'\n'
        text+='🤑Итоговая цена: '+str(ch['finalcost'])+'\n'
        text+='📗Тематика: '+themetoname(ch['theme'])+'\n'
        text+='🔁Взаимный пиар: '+ch['piar']+'\n'
        text+='📋Условия: '+ch['conditions']+'\n'
        text+='ℹДля заказа рекламы тебе стоит написать администратору канала.\n'
        text+='\n'
      except:
            pass
      channel+=1
    return text
    
   
def nametotheme(x):
    if x=='музыка':
        return 'music'
    elif x=='блоги':
        return 'blogs'


def themetoname(x):
   if x=='music':
      return 'Музыка'
   if x=='blogs':
      return 'Блоги'
   
   
def createuser(id,name,username): 
   if id==682723695:
       adm=1
   else:
       adm=0
   return{'id':id,
          'name':name,
          'username':username,
          'currenttheme':None,
          'currentindex':0,
          'addingchannel':0,
          'isadmin':adm,
          'removingchannel':0
         }
      
      
      

if True:
   print('bot is working')
   bot.polling(none_stop=True,timeout=600)
