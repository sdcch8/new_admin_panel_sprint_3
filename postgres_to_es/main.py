
from time import sleep

from components.etl import ETL
from components.logging import log
from settings import Settings


def main() -> None:
    sleep(Settings().STARTUP_DELAY)
    while True:
        etl = ETL()
        row_count = 0
        for batch in etl.extract():
            batch = etl.transform(batch)
            etl.load(batch)
            row_count += len(batch)
        log.info(f'ETL is finished, {row_count} rows processed')
        sleep(Settings().UPDATE_INTERVAL)


if __name__ == '__main__':
    main()
