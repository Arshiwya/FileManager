from errors import ErrorCode


class ReportCode:
    SUCCESS = 100
    UNSUCCESSFUL = 200


class Report:
    report_text = None

    def __init__(self, status_code=None):
        self.status_code = status_code

        if self.status_code == ReportCode.SUCCESS:
            self.report_text = "موفقیت آمیز"

        elif self.status_code == ReportCode.UNSUCCESSFUL:
            self.report_text = "ناموفق"


class ErrorReport(Report):
    error_code = None
    error_response_text = None

    def __init__(self, status_code, error_code):
        super(ErrorReport, self).__init__(status_code=status_code)
        self.error_code = error_code
        self.get_error_response_text()

    def get_error_response_text(self):
        if self.error_code == ErrorCode.SQLITE_CONSTRAINT_UNIQUE:
            error_text = "این کاربر قبلا ثبت شده است ."
            self.error_response_text = error_text
