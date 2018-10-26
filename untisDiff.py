#!/usr/bin/env python3
import urllib.request, http.cookiejar
from bs4 import BeautifulSoup
KEY_FILE_PATH = 'PATH_TO_FILLED_KEYFILE_TEMPLATE'
SCHOOL_NAME = 'YOUR_SCHOOLNAME_HERE'
PRINT_PREVIEW_URL = 'URL_TO_PRINT_PREVIEW' 
jar = http.cookiejar.CookieJar()

def read_keyfile():
    # this loads our API keys into memory from an external file which is specified above
    try:
        contents = open(KEY_FILE_PATH, 'r').readlines()
        # extract just the text behind the equals sign
        API_KEY = contents[0].split("=",1)[1]
        USER_KEYS = contents[1].split("=",1)[1]
        # get rid of that pesky newline
        API_KEY = API_KEY.strip()
        # now we split along semicolons to get single keys in a list
        USER_KEYS = USER_KEYS.split(";")
        return API_KEY, USER_KEYS
    except:
        import sys
        e = sys.exc_info()[1]
        print(e)
        print("I couldn't load your credentials. Did you specify your keyfile?")
        sys.exit(1)


def get_timetable():
    import datetime
    print(datetime.datetime.today())
    print('Getting timetable...')
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    loginUrl = 'https://asopo.webuntis.com/WebUntis/?'
    targetUrl = PRINT_PREVIEW_URL
    now = datetime.datetime.today()
    targetUrl.format(now.strftime('%Y%m%d'))
    val = {'school' : SCHOOL_NAME}
    data = urllib.parse.urlencode(val)
    asciidata = data.encode('ascii')

    opener.open(loginUrl, asciidata)
    result = opener.open(targetUrl)
    return result.read()

def html_to_pickle(html):
    import pickle
    import sys
    soup = BeautifulSoup(html, 'html.parser')
    stuff = soup.find('div', {'id' : 'timetable'})
    data = []
    try:
        styling = soup.find_all('style')[1]
        rows = stuff.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        data.append(str(styling))
        pickle.dump(data, open('new.p', 'wb'))
        return True
    except IndexError:
        #no style, no timetable...
        print('Could not find a timetable. Leaving new.p on its last value.')    
        return False

def alert():
    from pyfcm import FCMNotification
    apiKey, userKeys = read_keyfile()
    print('Alert triggered, sending PUSH notification.')
    client = FCMNotification(api_key=apiKey)
    for user in userKeys:
        client.notify_single_device(registration_id=user, message_body='WebUntis has been updated!', message_title='Timetable')

alarm = False
html = get_timetable()
# make this 2 funcs. getTimetable and ToPickle
timetableExists = html_to_pickle(html)
if timetableExists:
    import os, hashlib
    md5 = hashlib.md5()
    if os.path.isfile('old.p'):
        old = open('old.p', 'rb').read()
    else:
        print('No old timetable found. This can happen on the first run.')
        old = ''
    new = open('new.p', 'rb').read()
    oldhash = hashlib.md5(old).hexdigest()
    newhash = hashlib.md5(new).hexdigest()
    print('old file: ' + oldhash)
    print('new file: ' + newhash)
    if (oldhash == newhash): 
        print('No changes.')
    else: 
        print('ALERT! TIMETABLE HAS CHANGED!')
        alarm = True
    os.remove('old.p')
    os.rename('new.p', 'old.p')
if alarm:
    alert()