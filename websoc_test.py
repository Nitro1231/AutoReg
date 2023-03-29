import unittest
from AutoReg import WebSoc


class WebSocTest(unittest.TestCase):
    def test_init_class_test(self) -> None:
        options = {
            'YearTerm': None,
            'ShowComments': 'on',
            'ShowFinals': 'on',
            'Online': None,
            'Breadth': 'ANY',
            'Dept': 'ALL',
            'CourseNum': None,
            'Division': 'ANY',
            'CourseCodes': None,
            'InstrName': None,
            'CourseTitle': None,
            'ClassType': 'ALL',
            'Units': None,
            'Days': None,
            'StartTime': None,
            'EndTime': None,
            'MaxCap': None,
            'FullCourses': 'ANY',
            'FontSize': None,
            'CancelledCourses': 'Exclude',
            'Bldg': None,
            'Room': None,
            'Submit': 'XML'
        }
        w = WebSoc.WebSoc()
        self.assertTrue(w != None)
        self.assertEqual(w.options, options)

    def test_change_option(self) -> None:
        options = {
            'YearTerm': '2023-14',
            'ShowComments': 'on',
            'ShowFinals': 'off',
            'Online': None,
            'Breadth': 'ANY',
            'Dept': 'ALL',
            'CourseNum': None,
            'Division': 'ANY',
            'CourseCodes': '12345, 67890, 12333, 30303, 77777, 44444',
            'InstrName': None,
            'CourseTitle': None,
            'ClassType': 'ALL',
            'Units': 4,
            'Days': None,
            'StartTime': None,
            'EndTime': None,
            'MaxCap': None,
            'FullCourses': 'ANY',
            'FontSize': None,
            'CancelledCourses': 'Exclude',
            'Bldg': None,
            'Room': None,
            'Submit': 'XML'
        }
        w = WebSoc.WebSoc()
        w.set_option('YearTerm', '2023-14')
        w.set_option('ShowFinals', 'off')
        w.set_option('Units', 4)
        self.assertRaises(AssertionError, w.set_option, 'NotValidOption1', True)
        w.set_course_codes([12345, 67890, 12333, 30303, 77777, 44444])
        self.assertRaises(AssertionError, w.set_option, 'NotValidOption2', False)
        self.assertEqual(w.options, options)

    def test_remove_none(self) -> None:
        options = {
            'YearTerm': '2023-14',
            'ShowComments': 'on',
            'ShowFinals': 'None',
            'Breadth': 'ANY',
            'Dept': 'ALL',
            'Division': 'ANY',
            'CourseCodes': '12345, 67890, 12333, 30303, 77777, 44444',
            'ClassType': 'ALL',
            'FullCourses': 'ANY',
            'CancelledCourses': 'Exclude',
            'Submit': 'XML'
        }
        w = WebSoc.WebSoc()
        w.set_option('YearTerm', '2023-14')
        w.set_option('ShowFinals', 'None')
        w.set_course_codes([12345, 67890, 12333, 30303, 77777, 44444])
        self.assertEqual(w._remove_none(w.options), options)


if __name__ == '__main__':
    unittest.main()
