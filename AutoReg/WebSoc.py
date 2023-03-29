import re
import json
import requests
import xmltodict
from bs4 import BeautifulSoup
from collections import defaultdict


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


    def get_option_info(self) -> dict:
        text = requests.get(WEBSOC_BASE_URL).content
        html = BeautifulSoup(text, 'lxml')

        def parse_option(name: str) -> list[dict]:
            return [(e['value'], e.text.replace(u'\xa0', u'')) for e in html.find('select', {'name': name}).find_all('option')]

        option_info = {
            'SelectedYearTerm': html.find('select', {'name': 'YearTerm'}).find('option', selected=True)['value'],
            'YearTerm': parse_option('YearTerm'),
            'Dept': parse_option('Dept'),
            'Division': parse_option('Division'),
            'ClassType': parse_option('ClassType'),
            'Days': [None, 'MWF', 'TuTh', 'W'],
            'FullCourses': parse_option('FullCourses'),
            'CancelledCourses': parse_option('CancelledCourses'),
            'Submit': ['XML', 'Display Web Results', 'Display Text Results']
        }
        return option_info


    def set_option(self, key: str, value: any) -> None:
        if key in self.options:
            self.options[key] = value
        else:
            raise AssertionError(f'WebSoc.set_option: "{key}" is not a valid option.')


    def set_course_codes(self, codes: set[int]) -> None:
        self.set_option('CourseCodes', ', '.join([str(c) for c in codes]))


    def get_websoc_request(self) -> bytes:
        return requests.get(WEBSOC_BASE_URL, params=self._remove_none(self.options)).content


    def get_raw_xml_course_info(self) -> str:
        options = self.options.copy()
        options['Submit'] = 'XML'
        return requests.get(WEBSOC_BASE_URL, params=self._remove_none(options)).content


    def get_raw_json_course_info(self) -> dict:
        xml_data = self.get_raw_xml_course_info()
        return xmltodict.parse(xml_data)


    def get_course_info(self) -> list[dict]:
        json_data = self.get_raw_json_course_info()['websoc_results']
        if 'course_list' not in json_data: return []
        json_data = json_data['course_list']
        course_list = list()

        def make_list(element: any) -> list:
            return element if type(element) == list else [element]

        def make_defdict_list(element: any) -> list:
            if type(element) == list:
                return [defaultdict(lambda: None, e) for e in element]
            else:
                return [defaultdict(lambda: None, element)]
        
        def safe_get(dictionary: dict, key: str, default_value: any) -> any:
            return dictionary[key] if key in dictionary else default_value

        for school in make_defdict_list(json_data['school']):
            for dept in make_defdict_list(school['department']):
                for course in make_defdict_list(dept['course']):
                    for section in make_defdict_list(course['section']):
                        final = defaultdict(lambda: None, section['sec_final'] if 'sec_final' in section else {})
                        enrollment = section['sec_enrollment']
                        section_info = {
                            'code': int(section['course_code']),
                            'dept': {
                                'school': school['@school_name'],
                                'code': dept['@dept_code'],
                                'name': dept['@dept_name']
                            },
                            'course': {
                                'case': dept['@dept_case'],
                                'number': course['@course_number'],
                                'title': course['@course_title'],
                                'type': section['sec_type'],
                                'section': section['sec_num'],
                                'unit': section['sec_units'],
                                'prereq': safe_get(course, 'course_prereq_link', '')
                            },
                            'instructors': make_list(section['sec_instructors']['instructor']),
                            'meeting': [{
                                'days': meet['sec_days'],
                                'time': meet['sec_time'],
                                'bldg': meet['sec_bldg'],
                                'room': meet['sec_room'],
                                'room_link': meet['sec_room_link'],
                            } for meet in make_list(section['sec_meetings']['sec_meet'])],
                            'final': {
                                'date': final['sec_final_date'],
                                'day': final['sec_final_day'],
                                'time': final['sec_final_time']
                            },
                            'enrollment': {
                                'enrolled': int(enrollment['sec_enrolled']),
                                'max': int(enrollment['sec_max_enroll'])
                            },
                            'waitlist': {
                                'current': int(enrollment['sec_waitlist']) if not (enrollment['sec_waitlist'] == 'n/a' or 'off' in enrollment['sec_waitlist']) else 0,
                                'max': int(enrollment['sec_wait_cap'])
                            },
                            'status': section['sec_status'],
                            'restrictions': section['sec_restrictions'],
                            'comment': self._remove_tags(safe_get(section, 'sec_comment', ''))
                        }
                        course_list.append(section_info)
        return course_list


    def _remove_none(self, data: dict) -> dict:
        copy = data.copy()
        for key, value in data.items():
            if value == None:
                del copy[key]
        return copy


    def _remove_tags(self, text: str) -> str:
        pattern = re.compile('<.*?>')
        return re.sub(pattern, '', text)


    def save_file(self, text: str, filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)


    def save_json(self, src: dict, filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(src, f)
