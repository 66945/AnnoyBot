import http.client
import urllib.parse

import random

headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain'
}

session = 0
userPassword = 0

def sendRequest(data):
    params = urllib.parse.urlencode(data)
    print(params)

    conn = http.client.HTTPSConnection("www.bicycletrip.org")
    conn.request('POST', '/robot/robot.php', params, headers)

    r = conn.getresponse()
    print(r.status, r.reason)

    text = r.read().decode('utf8')
    print(text)

    return text.split('\n')

def sendCommand(command):
    data = {
        'request': 'send_command',
        'session': session,
        'user_password': userPassword,
        'command': command
    }

    sendRequest(data)

def setup(s, up):
    global session
    global userPassword

    session = s
    userPassword = up

if __name__ == "__main__":
    setup(input('session: '), input('user password: '))

    while True:
        cmd = input('cmd: ')
        
        if cmd != 'exit':
            sendCommand(cmd)
        else:
            sendRequest({'request': 'end_session', 'session': session, 'user_password': userPassword})
