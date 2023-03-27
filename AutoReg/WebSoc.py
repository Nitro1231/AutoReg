import json
import requests
import xmltodict
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


    def get_option_info(self) -> dict:
        text = requests.get(WEBSOC_BASE_URL).content
        html = BeautifulSoup(text, 'lxml')

        def parse_option(name: str) -> list[dict]:
            return [{e['value']: e.text.replace(u'\xa0', u'')} for e in html.find('select', {'name': name}).find_all('option')]

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


    def set_course_codes(self, codes: list[int]) -> None:
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


    # Known Bug:
    # There is an error when parsing discussion classes as they don't have a final exam,
    # but the program is still trying to parse them.
    def get_course_info(self) -> list[dict]:
        json_data = self.get_raw_json_course_info()['websoc_results']
        if 'course_list' not in json_data:
            return []
        json_data = json_data['course_list']
        # xml_data = open('./DataSamples/sample.xml', 'r').read()
        # json_data = xmltodict.parse(xml_data)['websoc_results']['course_list']
        course_list = list()

        def make_list(element: any) -> list:
            return element if type(element) == list else [element]

        def iter_school(school_data: dict) -> None:
            school_name = school_data['@school_name']

            def iter_dept(dept_data: dict) -> None:
                dept_code = dept_data['@dept_code']
                dept_case = dept_data['@dept_case']
                dept_name = dept_data['@dept_name']

                def iter_course(course_data: dict) -> None:
                    course_number = course_data['@course_number']
                    course_title = course_data['@course_title']
                    course_prereq = course_data['course_prereq_link']
                    
                    def iter_section(section_data: dict) -> None:
                        meeting = section_data['sec_meetings']['sec_meet']
                        final = section_data['sec_final']
                        enrollment = section_data['sec_enrollment']
                        section_info = {
                            'code': int(section_data['course_code']),
                            'dept': {
                                'school': school_name,
                                'code': dept_code,
                                'name': dept_name
                            },
                            'course': {
                                'case': dept_case,
                                'number': course_number,
                                'title': course_title,
                                'type': section_data['sec_type'],
                                'section': section_data['sec_num'],
                                'unit': int(section_data['sec_units']),
                                'prereq': course_prereq
                            },
                            'instructors': make_list(section_data['sec_instructors']['instructor']),
                            'meeting': {
                                'days': meeting['sec_days'],
                                'time': meeting['sec_time'],
                                'bldg': meeting['sec_bldg'],
                                'room': meeting['sec_room'],
                                'room_link': meeting['sec_room_link'],
                            },
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
                                'current': int(enrollment['sec_waitlist'] if enrollment['sec_waitlist'] != 'n/a' else 0),
                                'max': int(enrollment['sec_wait_cap'])
                            },
                            'status': section_data['sec_status'],
                            'restrictions': section_data['sec_restrictions'],
                            'comment': section_data['sec_comment'] if 'sec_comment' in section_data else None
                        }
                        course_list.append(section_info)

                    for section in make_list(course_data['section']):
                        iter_section(section)

                for course in make_list(dept_data['course']):
                    iter_course(course)

            for dept in make_list(school_data['department']):
                iter_dept(dept)

        for school in make_list(json_data['school']):
            iter_school(school)
        
        return course_list


    def _remove_none(self, data: dict) -> dict:
        copy = data.copy()
        for key, value in data.items():
            if value == None:
                del copy[key]
        return copy


w = WebSoc()

w.set_course_codes([34010, 34040, 35870, 35880, 34080, 33010, 34100, 34041])
w.set_option('YearTerm', '2023-14')
# w.set_option('Dept', 'COMPSCI')
w.set_option('Submit', 'Display Text Results')

print(w.get_websoc_request().decode('utf-8'))
print()
print(w.get_raw_xml_course_info().decode('utf-8'))
print()
print(json.dumps(w.get_raw_json_course_info()))
print()
print(json.dumps(w.get_course_info()))

# print(w._remove_none(w.options))
# print(w.get_websoc_request())

# print(str(w.get_option_info()).replace(',', '\n'))