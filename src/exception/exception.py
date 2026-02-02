from src.logging.logger import logging
import os
import sys

def get_message_error(error , error_detail : sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    lineno  = exc_tb.tb_lineno
    error_message = f"Error Occured File_Name -> {file_name} Line_Number -> {lineno} Message -> {str(error)}"

    return error_message


class CustomException(Exception):
    def __init__(self , error , error_detail : sys):
        super().__init__()
        self.error_message = get_message_error(error = error , error_detail = error_detail)

    def __str__(self):
        return self.error_message
    

if __name__ == "__main__":
    try:
        1/0
    except Exception as e:
        logging.info("Error")
        raise CustomException(e,sys)