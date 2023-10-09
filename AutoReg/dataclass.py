from .constants import Mode, GradeOption


class Course:
    def __init__(
            self,
            course_code: str | int,
            mode: Mode,
            grade_option: GradeOption = GradeOption.GRADE,
            var_units: str | int = '',
            auth_code: str | int = '',
        ) -> None:
        self.course_code = course_code
        self.mode = mode
        self.grade_option = grade_option
        self.var_units = var_units
        self.auth_code = auth_code


    def as_dict(self) -> dict:
        return {            
            'button': 'Send Request',
            'mode': self.mode.value,
            'courseCode': str(self.course_code),
            'gradeOption': self.grade_option.value,
            'varUnits': str(self.var_units),
            'authCode': str(self.auth_code),
        }
