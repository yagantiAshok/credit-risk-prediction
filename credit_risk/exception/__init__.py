
import sys

def error_message_details(error,error_details:sys):
    " this function extracts filename and line number"
    _,_,exc_tb = error_details.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    file_no = exc_tb.tb_lineno
    error_message = f"error message occured in [{filename}] in line number [{file_no}] and the error message is [{str(error)}]"
    return error_message

class CustomException(Exception):
    def __init__(self,error,error_details:sys):
        super().__init__(error)
        self.error_message = error_message_details(error=error,error_details=error_details)
    def __str__(self):
        return self.error_message
