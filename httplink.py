import http.client
import urllib.parse

import random

headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain'
}
robotPassword = 'Hmitditw'

session = 0
userPassword = 0

def sendRequest(data):
    params = urllib.parse.urlencode(data)

    conn = http.client.HTTPSConnection("www.bicycletrip.org")
    conn.request('POST', '/robot/robot.php', params, headers)

    r = conn.getresponse()
    text = r.read().decode('utf8')

    return text.split('\n')

def getUsers():
    data = {
        'request': 'get_users',
        'robot_password': robotPassword
    }

    return sendRequest(data)

def start(user):
    global session
    global userPassword

    session = random.randint(1000, 9999)
    userPassword = random.randint(1000, 9999)

    data = {
        'request': 'start_session',
        'name': user,
        'robot_password': robotPassword,
        'session': session,
        'user_password': userPassword
    }

    print(data)

    return sendRequest(data)

def stop():
    data = {
        'request': 'end_session',
        'session': session,
        'user_password': userPassword
    }

    return sendRequest(data)

def getCommand():
    data = {
        'request': 'get_command',
        'session': session,
        'user_password': userPassword
    }

    return sendRequest(data)


if __name__ == "__main__":
    start('Dad')
    input()
    for i in range(10):
        print(getCommand())
    input()
    stop()