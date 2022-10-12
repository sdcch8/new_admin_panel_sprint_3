import logging
from time import sleep

from components.etl import ETL
from settings import UPDATE_INTERVAL

log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler('main.log', mode='w')
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def main() -> None:
    while True:
        etl = ETL()
        row_count = 0
        for batch in etl.extract():
            batch = etl.transform(batch)
            etl.load(batch)
            row_count += len(batch)
        log.info(f'ETL is finished, {row_count} rows processed')
        sleep(UPDATE_INTERVAL)


if __name__ == '__main__':
    main()
