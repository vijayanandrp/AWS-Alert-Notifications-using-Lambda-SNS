import os
import sys
import logging

root_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(root_dir, 'data')
config_dir = os.path.join(data_dir, 'config')

config_format = '.json'

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

stream_handler = logging.StreamHandler(sys.stdout)
log_args = {
    "level": logging.DEBUG if os.environ.get("log_debug", "false") == "true" else logging.INFO,
    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "datefmt": "%d-%b-%y %H:%M",
    "handlers": [stream_handler]
}
logging.basicConfig(**log_args)

def get_logger(name):
    return logging.getLogger(name)
