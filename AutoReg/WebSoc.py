import json
import requests
import xml.dom.minidom as xml
from bs4 import BeautifulSoup


WEBSOC_BASE_URL = 'https://www.reg.uci.edu/perl/WebSoc/'


class WebSoc():
    def __init__(self) -> None:
        self.options = {
            'YearTerm': None,
            'Breadth': 'ANY',
            'ShowFinals': 'on',
            'Dept': 'ALL',
            'CourseCodes': None,
            'CourseNum ': None,
            'Division': 'ALL',
            'InstrName ': None,
            'CourseTitle': None,
            'ClassType ': 'ALL',
            'Units': None,
            'Days': None,
            'StartTime': None,
            'EndTime': None,
            'FullCourses': 'ANY',
            'CancelledCourses': 'Exclude',
            'Submit': 'XML'
        }


    def get_option_info(self) -> dict:
        return


    def set_option(self, key: str, value: any) -> None:
        if key in self.options:
            self.options[key] = value
        else:
            raise AssertionError(f'WebSoc.set_option: "{key}" is not a valid option.')


    def set_course_codes(self, codes: list[int]) -> None:
        self.set_option('CourseCodes', ', '.join([str(c) for c in codes]))


    def get_websoc_request(self) -> bytes:
        return requests.get(WEBSOC_BASE_URL, params=self._remove_none(self.options)).content


    def get_course_info(self) -> dict:
        # options = self.options.copy()
        # options['Submit'] = 'XML'
        # data = requests.get(WEBSOC_BASE_URL, params=self._remove_none(options)).content
        data = open('./DataSamples/sample.xml', 'r').read()
        doc = xml.parseString(data)
        print(doc.tagName)
        return 


    def _remove_none(self, data: dict) -> dict:
        copy = data.copy()
        for key, value in data.items():
            if value == None:
                del copy[key]
        return copy
