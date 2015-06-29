#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2015/06/28
# Author  : @Arlefreak hi@arlefreak.com
# Link    : arlefreak.com
# Version : 0.0.1

import requests
import json

class Bot:
    def __init__(self, token = ''):
        self.token    = token
        self.url      = 'https://api.telegram.org/bot%s/' % self.token
        self.timeout  = 1.0
        self.user     = User()

    def CheckSettings(self):
        return self.GetMe()
    def GenericApiFunction(self,name=None, _params=None):
        url = self.url + name
        request = {}
        if(None):
            return
        else:
            try:
                return requests.get(url,params=_params).json().get('result', None)
            except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError) as e:
                print("Error" + str(e))
                return None
    def GetMe(self):
        me = self.GenericApiFunction('getMe')
        if(me):
            self.user = User(me)
        return me
    def SendMessage(self, _id, _text, _webPage = None, _replyTo = None, _replyMarkup = None):
        d = dict(chat_id=_id,text=_text, disable_web_page_preview=_webPage, reply_to_message_id = _replyTo, reply_markup = _replyMarkup )
        msg = self.GenericApiFunction('sendMessage',d)
        return msg
    def ForwardMessage(self, _id, _from, _msg):
        d = dict(chat_id = _id, from_chat_id = _from, reply_markup = _replyMarkup)
        msg = self.GenericApiFunction('forwardMessage',d)
        return msg
    def SendPhoto(self, _id, _photo, _caption = None, _replyTo = None, _replyMarkup = None):
        d = dict(chat_id = _id, photo = _photo, caption = _caption, reply_to_message_id = _replyTo, reply_markup = _replyMarkup)
        msg = self.GenericApiFunction('sendPhoto',d)
        return msg
    def SendAudio(self, _id, _audio, _replyTo = None, _replyMarkup = None):
        d = dict(chat_id = _id, audio = _audio, reply_to_message_id = _replyTo, reply_markup = _replyMarkup)
        msg = self.GenericApiFunction('sendAudio',d)
        return msg
    def SendDocument(self, _id, _document, _replyTo = None, _replyMarkup = None):
        d = dict(chat_id = _id, document = _document, reply_to_message_id = _replyTo, reply_markup = _replyMarkup)
        msg = self.GenericApiFunction('sendDocument',d)
        return msg
    def SendSticker(self, _id, _sticker, _replyTo = None, _replyMarkup = None):
        d = dict(chat_id = _id, sticker = _sticker, reply_to_message_id = _replyTo, reply_markup = _replyMarkup)
        msg = self.GenericApiFunction('sendSticker',d)
        return msg
    def SendVideo(self, _id, _video, _replyTo = None, _replyMarkup = None):
        d = dict(chat_id = _id, video = _video, reply_to_message_id = _replyTo, reply_markup = _replyMarkup)
        msg = self.GenericApiFunction('sendVideo',d)
        return msg
    def SendLocation(self, _id, _latitude, _longitude, _replyTo = None, _replyMarkup = None):
        d = dict(chat_id = _id, latitude = _latitude, longitud = _longitude, reply_to_message_id = _replyTo, reply_markup = _replyMarkup)
        msg = self.GenericApiFunction('sendLocation',d)
        return msg
    def SendChatAction(self, _id, _action):
        d = dict(chat_id = _id, action = _action)
        msg = self.GenericApiFunction('sendChatAction',d)
        return msg
    def GetUserProfilePhotos(self, _id, _offset = None, _limit = None):
        d = dict(user_id = _id, offset = _offset, limit = _limit)
        msg = self.GenericApiFunction('getUserProfilePhotos', d)
        return msg
    def GetUpdates(self, _offset=None, _limit = None, _timeout = None):
        d = dict(offset = _offset, limit = _limit, timeout = _timeout)
        msg = self.GenericApiFunction('getUpdates', d)
        return msg
    def SetWebhook(_url):
        d =  dict(url = _url,)
        msg = self.GenericApiFunction('setWebhook')
        return msg

class User:
    def __init__(self, dictionary = {}):
        self.id         = 0
        self.first_name = ""
        self.last_name  = ""
        self.username   = ""
        for k, v in dictionary.items():
            setattr(self,k,v)

class GroupChat:
    def __init__(self, dictionary = {}):
        self.id    = 0
        self.title = ''
        for k, v in dictionary.items():
            setattr(self,k,v)

class Message:
    def __init__(self, dictionary = {}):
        self.message_id            = 0
        self.from_user             = {}
        self.date                  = 0
        self.chat                  = {}
        self.forward_from          = {}
        self.forward_date          = 0
        self.reply_to_message      = {}
        self.text                  = ''
        self.audio                 = {}
        self.document              = {}
        self.photo                 = []
        self.sticker               = {}
        self.video                 = {}
        self.contact               = {}
        self.location              = {}
        self.new_chat_participant  = {}
        self.left_chat_participant = {}
        self.new_chat_title        = ''
        self.new_chat_photo        = []
        self.delete_chat_photo     = True
        self.delete_chat_created   = True
        for k, v in dictionary.items():
            if(k == 'chat'):
                v = User(v)
            setattr(self,k,v)

class PhotoSize:
    def __init__(self, dictionary = {}):
        self.file_id   = ''
        self.width     = 0
        self.height    = 0
        self.file_size = 0
        for k, v in dictionary.items():
            setattr(self,k,v)

class Audio:
    def __init__(self, dictionary = {}):
        self.file_id    = ''
        self.duration   = 0
        self.mimme_type = ''
        self.file_size  = 0
        for k, v in dictionary.items():
            setattr(self,k,v)

class Document:
    def __init__(self, dictionary = {}):
        self.file_id    = ''
        self.thumb      = {}
        self.file_name  = ''
        self.mimme_type = ''
        self.file_size  = 0
        for k, v in dictionary.items():
            setattr(self,k,v)

class Sticker:
    def __init__(self, dictionary = {}):
        self.file_id   = ''
        self.width     = 0
        self.height    = 0
        self.thumb     = {}
        self.file_size = 0
        for k, v in dictionary.items():
            setattr(self,k,v)

class Video:
    def __init__(self, dictionary = {}):
        self.file_id    = ''
        self.width      = 0
        self.height     = 0
        self.duration   = 0
        self.thumb      = {}
        self.mimme_type = ''
        self.file_size  = ''
        self.caption    = ''
        for k, v in dictionary.items():
            setattr(self,k,v)

class Contact:
    def __init__(self, dictionary = {}):
        self.phone_number = ''
        self.first_name   = ''
        self.last_name    = ''
        self.user_id      = ''
        for k, v in dictionary.items():
            setattr(self,k,v)

class Location:
    def __init__(self, dictionary = {}):
        self.longitud = 0.0
        self.latitude = 0.0
        for k, v in dictionary.items():
            setattr(self,k,v)

class Update:
    def __init__(self, dictionary = {}):
        self.update_id = 0
        self.message   = None
        for k, v in dictionary.items():
            if(k == 'message'):
                v = Message(v)
            if(k == 'update_id'):
                v = int(v)
            setattr(self,k,v)

class InputFile:
    def __init__(self, dictionary = {}):
        for k, v in dictionary.items():
            setattr(self,k,v)

class UserProfilePhotos:
    def __init__(self, dictionary = {}):
        self.total_count = 0
        self.photos      = []
        for k, v in dictionary.items():
            setattr(self,k,v)

class ReplyKeyboardMarkup:
    def __init__(self, dictionary = {}):
        self.keyboard          = []
        self.resize_keyboard   = True
        self.one_time_keyboard = True
        self.selective         = True
        for k, v in dictionary.items():
            setattr(self,k,v)

class ReplyKeyboardHide:
    def __init__(self, dictionary = {}):
        for k, v in dictionary.items():
            setattr(self,k,v)
        self.hide_keyboard = True
        self.selective     = True
        for k, v in dictionary.items():
            setattr(self,k,v)

class ForceReply:
    def __init__(self, dictionary = {}):
        for k, v in dictionary.items():
            setattr(self,k,v)
        self.force_reply = True
        self.selective   = None
        for k, v in dictionary.items():
            setattr(self,k,v)
