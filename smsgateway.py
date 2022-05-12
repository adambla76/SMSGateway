#!/usr/bin/env python3
#
#
#  Bramka SMS do odbierania/wysyłania wiadomości na RPi
#
#   (c) AdamBla76@gmail.com
#
#


import sim800l
from time import sleep
from flask import *
from multiprocessing import Process, Queue
from datetime import datetime
import logging
import re
import os


app = Flask(__name__)
modem=sim800l.SIM800L('/dev/ttyUSB0',38400)
queue = Queue()
logger = logging.getLogger('smsgateway')
sms=""
code=""
cash=""
rx=""
rx_ts = datetime.timestamp(datetime.now())


def UCS2decoder(msg):

    if msg[-1]=='\n':
        msg = msg[:-1]
    try:
        t=""
        for i in range(0,len(msg),4):
            ch=msg[i:i+4]
            t+=chr(int(ch,16))
        return t
    except:
        return msg

def UCS2encoder(msg):
    if msg[-1]=='\n':
        msg = msg[:-1]
    
    t=""
    for i in msg:
        ch=''
        x=hex(ord(i)).lstrip('0x')
        for i in range(4-len(x)):
            ch+='0'
        t+=ch + x
    return t
     

def retrive_sms():
    global rx_ts
    frame = modem.read_sms(1)
    modem.delete_sms(1)

    if frame != None:
        #print(frame)
        frame = [UCS2decoder(t) for t in frame] 
        cid,dt,msg = frame[0], frame[1] + "  " + frame[2], frame[3]
        #print(frame)
        if '#reboot' in msg.lower() and '730500500' in cid:
            logger.info('SMS command: #reboot')
            print("Siup i reboot!")
            modem.send_sms(UCS2encoder(cid),UCS2encoder('Reboot in progress...'))
            #modem.send_sms(cid,UCS2encoder('Reboot in progress...'))
            sleep(2)
            os.system('sudo shutdown -r now')
        elif '#refresh' in msg.lower() and '730500500' in cid:
            logger.info('SMS command: #refresh')
            print("Restart Flask service")
            sleep(1)
            os.system('sudo systemctl restart smsgateway.service')
        elif msg[0] == '?' and '730500500' in cid:
            logger.info('SMS command: help')
            print("send help")
            msg = '#reboot -> reboot RPI'+chr(10)+'#info -> status'+chr(10)+'#refresh -> restart web service'
            modem.send_sms(UCS2encoder(cid),UCS2encoder(msg))
            #modem.send_sms(cid,UCS2encoder(msg))

        elif '#info' in msg.lower() and '730500500' in cid:
            logger.info('SMS command: #info')
            print("info query!")
            modem.send_sms(UCS2encoder(cid),UCS2encoder("Thanks I'm fine my Lord!"))
            #modem.send_sms(cid,UCS2encoder("Thanks I'm fine my Lord!"))
        elif '#test' in msg.lower() and '730500500' in cid:
            logger.info('SMS command: #info')
            print("info query!")
            modem.send_sms(UCS2encoder(cid),UCS2encoder("ING Bank Slaski. Logujesz sie do Mojego ING. Kod do autoryzacji: 12341234** 2020.09.04 ** 09:24:52."))
            #modem.send_sms(cid,UCS2encoder("ING Bank Slaski. Logujesz sie do Mojego ING. Kod do autoryzacji: 12341234** 2020.09.04 ** 09:24:52."))
        else:
            print("CalledID:",cid,"  DateTime:",dt,"  Msg:",msg)
            rx_ts = datetime.timestamp(datetime.now())
            msg = re.sub('(?<!\d)\d{8}(?!\d)', 'xxxxxxxx', msg)
            logger.info('SMS from '+ cid +' : ' + msg)
            queue.put(frame)

def print_empty():
    return True

@app.route('/')
def index():
    global sms,code,cash,rx_ts
  
    ts = datetime.timestamp(datetime.now()) 
    if (ts - rx_ts) > 300:
        sms = "" 
        rx_ts = ts

    if not queue.empty():
        rx = queue.get()
        sms = rx[3]
        if re.search('w Moim ING',sms):
            try:
                code = re.findall('\s(?<!\d)(\d{8})(?!\d)', sms)[0]
            except:
                code = ""
            
            try:
                cash = re.findall('\s(?<!\d)(\d+[.]\d{2})[.]?\s',sms)[0]
            except:
                cash = ""
        else:
            code = "waiting ..."
            cash = ""
            if len(rx[0])>0:
                code = ""
                sms = "SMS from " + rx[0] + "</br>" + sms
                #sms = "received SMS:</br>" + sms 
                   
    else:
        if len(sms)==0:
            code = ""
            cash = ""
            sms = "waiting for SMS"
        
    page  = '<!DOCTYPE html> <html lang="en">\n'
    page += '<head><meta name="viewport" content="width=device-width,initial-scale=1.0, user-scalable=no">\n'
    page += '<title>SMS Gateway</title>\n'
    page += '<meta http-equiv="refresh" content="5">\n'
    page += '<meta charset="utf-8">\n'
    page += '<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n'
    page += 'body{margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;}\n'
    page += 'p {font-size: 24px;color: #444444;margin-bottom: 10px;}\n'
    page += 'a {text-decoration: none;}\n'
    page += 'a:active {color: red !important;}\n'
    page += '</style>\n'
    page += '<script>function copyText(e){var t=document.createElement("input");t.setAttribute("value",document.getElementById(e).innerHTML),document.body.appendChild(t),t.select(),document.execCommand("copy"),document.body.removeChild(t)}</script>\n'
    page += '</head>\n'
    page += '<body style="background-color: black;">\n'
    page += '<div id="webpage">\n'
    
    if len(code)>0:
        page += '<p style="text-align: center; font-size:170px; color:yellow; margin-top: 50px;">'
        page += 'KOD: '
        page += '<a href="javascript:void(0)" id="mycode" onclick="copyText(\'mycode\')" style="text-align: center; font-size:170px; color:yellow; margin-top: 50px; ">' + code + '</a>\n'
        page += '</p>\n'

    if len(cash)>0:
        page += '<p style="text-align: center; font-size:170px; color:yellow; margin-top: 50px;">'
        page += 'KWOTA: ' + cash
        page += '</p>\n'

    page += '<p style="text-align: center; font-size:80px; color:yellow; margin-top:50px;">'
    page += sms
    page += '</p>\n'
    page += '</div>\n'
    page += '</body>\n'
    page += '</html>\n'
    
    
    return page




def mainloop():
    while True:
        modem.check_incoming()
        sleep(1)


hdlr = logging.FileHandler('/var/log/smsgateway.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

modem.setup()
modem.callback_msg(retrive_sms)
modem.callback_no_carrier(print_empty)
modem.read_and_delete_all()

print('\nSMSGateway has been restarted\n')
logger.info('SMSGateway has been restarted')
modem.send_sms(UCS2encoder('+48730500500'),UCS2encoder('SMSGateway has been restarted'))

p = Process(target=mainloop, args=())
p.start()
app.run(debug=False, host='0.0.0.0', port=8888 )
