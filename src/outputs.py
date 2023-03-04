import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (BASE_DIR, DATETIME_FORMAT, DEFAULT, ENCODING, FILE,
                       PRETTY, RESULTS)

FILE_OUTPUT_INFO = 'Файл с результатами был сохранён: {file_path}'


def control_output(results, cli_args):
    OUTPUT.get(cli_args.output)(results, cli_args)


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / RESULTS
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding=ENCODING) as f:
        writter = csv.writer(f, dialect=csv.unix_dialect)
        writter.writerows(results)
    logging.info(FILE_OUTPUT_INFO.format(file_path=file_path))


OUTPUT = {
    PRETTY: pretty_output,
    FILE: file_output,
    DEFAULT: default_output,
}
