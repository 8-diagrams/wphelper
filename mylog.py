import logging
import logging.handlers
import datetime
import concurrent_log

"""
logger = logging.getLogger('mylogger')

logger.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler('./backlog/main_all.log', when='midnight', interval=1, backupCount=60, atTime=datetime.time(0, 0, 0, 0), encoding='utf-8')
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

f_handler = logging.FileHandler('./backlog/main_error.log', encoding='utf-8')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)
"""

log_conf = {
            'version': 1,
            'formatters': {
                'default': {
                    'format': '%(asctime)s - %(process)d-%(threadName)s - '
                              '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    'datefmt': "%Y-%m-%d %H:%M:%S"
                },
            },
            'handlers': {
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.ConcurrentTimedRotatingFileHandler',
                    'backupCount': 60,
                    'when': 'midnight',
                    'delay': True,
                    'filename': 'backlog/main_all.log',
                    'encoding': 'utf-8',
                    'formatter': 'default',
                }
            },
            'root': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }

import os
file_path = os.path.split(log_conf.get("handlers").get("file").get("filename"))[0]
if not os.path.exists(file_path):
    os.makedirs(file_path)
logging.config.dictConfig(log_conf)
logger = logging.getLogger(__name__)
