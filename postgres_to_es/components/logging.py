import logging
import sys

log = logging.getLogger()
log.setLevel(logging.INFO)
handler_file = logging.FileHandler('main.log', mode='w')
handler_stdout = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
)
handler_file.setFormatter(formatter)
handler_stdout.setFormatter(formatter)
log.addHandler(handler_file)
log.addHandler(handler_stdout)
