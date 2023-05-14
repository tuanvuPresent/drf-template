import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger



class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        log_record['lt'] = record.name
        log_record['ll'] = record.levelname
        log_record['tl'] = datetime.now().strftime(self.default_time_format)
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not record.msg:
            del log_record['message']


def get_logger(name):
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(CustomJsonFormatter())

    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    _logger.addHandler(log_handler)
    return _logger
