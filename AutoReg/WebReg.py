import json
import urllib
import urllib3
import requests
from bs4 import BeautifulSoup


STARTUP_URL = 'https://www.reg.uci.edu/cgi-bin/webreg-redirect.sh'
WEBREG_BASE_URL = 'https://webreg{}.reg.uci.edu/cgi-bin/wramia'
DUO_URL = 'https://login.uci.edu/duo/duo_auth.php'
PAGE_MAP = {
    'enrollQtrMenu': {
        'enrollmentMenu': 'Enrollment Menu',
        'waitlistMenu': 'Wait list Menu'
    },
    'enrollmentMenu': {
        'waitlistMenu': 'Go to Wait List Menu',
        'enrollQtrMenu': 'Return to Main Menu'
    },
    'waitlistMenu': {
        'enrollmentMenu': 'Go to Enrollment Menu',
        'enrollQtrMenu': 'Return to Main Menu'
    }

}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebReg():
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.verify = False
        self.active = False
        self.page = 'enrollQtrMenu'
        self.url = None


    def login(self, UCInetID: str, password: str) -> bool:
        # Initializing WebReg login session.
        redirect = self.session.get(STARTUP_URL)
        startup = self.session.get(redirect.url)

        # Parsing WebReg session info.
        session_url = self._parse_url(startup.text)
        self.num = self._get_between(session_url, 'webreg', '.reg')
        self.call = self._get_between(session_url, 'call=', '&')

        reg_data = {
            'ucinetid': UCInetID,
            'password': password, # There might be a chance to leak the user's password.
            'login_button': 'Logging in'
        }
        reg = self.session.post(session_url, data=reg_data) # https://login.uci.edu/ucinetid/webauth?return_url=https://webreg{}.reg.uci.edu:443/cgi-bin/wramia?page=login?call={}&info_text=Reg+Office+Home+Page&info_url=https://www.reg.uci.edu/

        # Requesting the user's DUO information and starting up the authorization session.
        duo_url = 'https://login.uci.edu' + self._parse_url(reg.text)
        init = self.session.get(duo_url)
        init_json = json.loads(self._get_between(init.text, 'init(', ');').replace('\'', '"'))

        # Preparing the main DUO authorization request.
        auth_url = f'https://{init_json["host"]}'
        auth_params = {
            'tx': init_json['sig_request'].split(':APP')[0],
            'parent': duo_url,
            'v': 2.8
        }
        auth = self.session.post(auth_url + '/frame/web/v1/auth?', params=auth_params)
        sid = urllib.parse.unquote(auth.url.split('sid=')[1])

        # Requesting DUO prompt by using "passcode" factor.
        prompt_data = {
            'sid': sid,
            'device': 'phone1',
            'factor': 'Passcode',
            'passcode': input('enter: '),
            'days_to_block': 'None'
        }
        prompt = self.session.post(auth_url + '/frame/prompt', data=prompt_data)

        # Requesting DUO prompt status check.
        status_data = {
            'sid': sid,
            'txid': prompt.json()['response']['txid']
        }
        status = self.session.post(auth_url + '/frame/status', data=status_data)
        status_json = status.json()

        if status_json['stat'] == 'OK' and status_json['response']['result'] == 'SUCCESS':
            success = self.session.post(auth_url + status_json['response']['result_url'], data={'sid': sid})
            wrapup_data = {
                'return_url': f'https://webreg{self.num}.reg.uci.edu:443/cgi-bin/wramia?page=login?call={self.call}&v=2.8',
                'sig_response': f'{success.json()["response"]["cookie"]}:APP{init_json["sig_request"].split(":APP")[1]}'
            }
            self.session.post(DUO_URL, data=wrapup_data)

            print('INFO', f'NUM: {self.num}, CALL: {self.call}')

            self.active = True
            self.url = WEBREG_BASE_URL.format(self.num)
            return True
        else:
            print(status_json)
            self.active = False
            self.url = None
            return False


    def logout(self):
        data = {
            'mode': 'exit',
            'submit': 'Logout'
        }
        self._webreg_request(data)
        self.active = False
        self.url = None


    def enrollment_window(self):
        self._navigate('enrollQtrMenu')
        data = {
            'mode': 'enrollmentWindow',
            'submit': 'Enrollment Window'
        }
        self._webreg_request(data)


    def fee_status(self):
        self._navigate('enrollQtrMenu')
        data = {
            'mode': 'feeStatus',
            'submit': 'Fee Status'
        }
        self._webreg_request(data)


    def study_list(self):
        self._navigate('enrollQtrMenu')
        data = {
            'mode': 'listSchedule',
            'submit': 'Study List'
        }
        self._webreg_request(data)


    def _navigate(self, page: str) -> None:
        if self.page != page:
            data = {
                'mode': page,
                'submit': PAGE_MAP[self.page][page]
            }
            self._webreg_request(data)


    def _webreg_request(self, data: dict) -> str:
        # Update `page` and `call`
        data['page'] = self.page
        data['call'] = self.call

        # add other handlers.
        res = self.session.post(self.url, data=data)
        html = BeautifulSoup(res.content, 'lxml')

        print(data['submit'])
        for c in ['WebRegErrorMsg', 'WebRegInfoMsg', 'DivLogoutMsg']:
            e = html.find('div', class_=c)
            print(c, e.text.strip() if e != None else None)
        print()

        if data['submit'] == 'Study List':
            e = html.find('table', class_='studyList')
            print('studyList', e.text.strip() if e != None else None)

        # print(res.text)
        return res.text


    def _parse_url(self, text: str) -> str:
        return text.split('url=', 1)[1].split('">')[0]


    def _get_between(self, text: str, token1: str, token2: str) -> str:
        return text.split(token1, 1)[1].split(token2)[0]
