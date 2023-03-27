import json
import requests
import xml.dom.minidom as xml
from bs4 import BeautifulSoup


WEBSOC_BASE_URL = 'https://www.reg.uci.edu/perl/WebSoc/'


class WebSoc():
    def __init__(self) -> None:
        self.options = {
            'YearTerm': None,                   #***Term: 'year-type'
            'ShowComments': 'on',               #   Show course comments: 'on' or None
            'ShowFinals': 'on',                 #   Show finals schedule: 'on' or None
            'Online': None,                     #   Show online and virtual classes only: None or 'on'
            'Breadth': 'ANY',                   # * General Education (Breadth): 'ANY', ...
            'Dept': 'ALL',                      # * Department Name: 'ALL', ...
            'CourseNum': None,                  #   Course Number or Range: None, H2A, 5, 10-20 (multiple entries ok)
            'Division': 'ANY',                  #***Course Level: 'ANY', '0xx', '1xx', or '2xx'
            'CourseCodes': None,                # * Course Code or Range: 14200, 29000-29100
            'InstrName': None,                  # * Instructor: None
            'CourseTitle': None,                #   Course Title Contains: None
            'ClassType': 'ALL',                 #***Course Type: 'ALL', ...
            'Units': None,                      #   Units: 3, 4, or VAR
            'Days': None,                       #   Days: None, or one from MWF, TuTh, W
            'StartTime': None,                  #   Starting Time After: None
            'EndTime': None,                    #   Ending Time Before: None
            'MaxCap': None,                     #   Maximum Capacity: None, or something like '>50', '<20'
            'FullCourses': 'ANY',               #***Courses Full Option: 'ANY', ...
            'FontSize': None,                   #   Web Font Size Percentage: None, or any int type value
            'CancelledCourses': 'Exclude',      #***Cancelled Courses: 'Exclude', 'Include', or 'only'
            'Bldg': None,                       #   Building code: None, or one from https://www.reg.uci.edu/addl/campus/
            'Room': None,                       #   Room: None, or room number
            'Submit': 'XML'                     #***Return type: 'XML', 'Display Web Results', or 'Display Text Results'
        }


    def _parse_option(self, html: BeautifulSoup, name: str) -> list[dict]:
        return [{e['value']: e.text.replace(u'\xa0', u'')} for e in html.find('select', {'name': name}).find_all('option')]


    def get_option_info(self) -> dict:
        text = requests.get(WEBSOC_BASE_URL).content
        html = BeautifulSoup(text, 'lxml')
        option_info = {
            'SelectedYearTerm': html.find('select', {'name': 'YearTerm'}).find('option', selected=True)['value'],
            'YearTerm': self._parse_option(html, 'YearTerm'),
            'Dept': self._parse_option(html, 'Dept'),
            'Division': self._parse_option(html, 'Division'),
            'ClassType': self._parse_option(html, 'ClassType'),
            'Days': [None, 'MWF', 'TuTh', 'W'],
            'FullCourses': self._parse_option(html, 'FullCourses'),
            'CancelledCourses': self._parse_option(html, 'CancelledCourses'),
            'Submit': ['XML', 'Display Web Results', 'Display Text Results']
        }
        return option_info


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


# w = WebSoc()

# w.set_course_codes([34010, 34040])
# w.set_option('YearTerm', '2023-14')
# w.set_option('Submit', 'Display Text Results')

# print(w._remove_none(w.options))
# print(w.get_websoc_request())

# print(str(w.get_option_info()).replace(',', '\n'))