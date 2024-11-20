import os
import time
import urllib3
import requests


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
s = requests.Session()


def notifyLinux(title: str, text: str):
    os.system(f"notify-send --expire-time=0 \"{title}\" \"{text}\"")

def notifyMac(title: str, text: str):
    os.system(f'osascript -e \'display notification "{text}" with title "{title}"\'')

def playSoundMac(sound: str):
    os.system(f'afplay /System/Library/Sounds/{sound}')


def getCourseInfo(ids: list[str]):
    payload = {
        'YearTerm': '2025-03',
        'ShowFinals': 'on',
        'Breadth': 'ANY',
        'Dept': 'ALL',
        'Division': 'ANY',
        'CourseCodes': ', '.join(ids),
        'ClassType': 'ALL',
        'FullCourses': 'ANY',
        'CancelledCourses': 'Exclude',
        'Submit': 'Display Text Results'
    }
    res = s.request('POST', 'https://www.reg.uci.edu/perl/WebSoc', data=payload, verify=False)
    
    if res.status_code == 200:
        return res.text
    else:
        print(f'Error! (code: {res.status_code})')
        return ''


while True:
    text = getCourseInfo(['34340'])

    print(text)

    if 'OPEN' in text:
        print('There is a spot available!')
        notifyLinux('Open Course Found!', 'There is a spot available!')
        # optionally, add playSound()
    else:
        print('No spot available... :(')
    time.sleep(20)
