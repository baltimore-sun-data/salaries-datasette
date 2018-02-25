import csv
import os
import re

from csvs_to_sqlite.cli import cli as csvs_cli

fieldnames = [
  "first_name",
  "middle_initial",
  "last_name",
  "suffix",
  "system",
  "organization",
  "subtitle",
  "agency",
  "class_code",
  "pay_rate",
  "ytd_gross_earnings",
  "annual_salary",
  "regular_earnings",
  "overtime_earnings",
  "other_earnings",
  "term_date",
]

def main():
    output_db = 'data/salaries.db'
    tables = [
        ('static/csv/cy2017-md.csv', 'data/cy2017-md.csv', '2017 Maryland state salaries'),
    ]

    try:
        os.unlink(output_db)
    except FileNotFoundError:
        pass
    else:
        print('Removed old database')

    for iname, oname, table in tables:
        print(f'{table}: processing csv')
        process_csv(iname, oname)

        print(f'{table}: creating database')
        create_db(output_db, oname, table)

        # Remove temporary file
        os.unlink(oname)

    print('Done.')


def process_csv(inname, outname):
    with open(inname) as fi:
        dr = csv.DictReader(fi)
        objs = list(dr)

    for f in [not_zero]:
        objs = filter(f, objs)

    for f in [fix_null, fix_subtitle, fix_term]:
        objs = map(f, objs)

    with open(outname, 'w') as fo:
        dw = csv.DictWriter(fo, fieldnames)
        dw.writeheader()
        for obj in objs:
            dw.writerow(obj)


def not_zero(row):
    return not all(
        row[col] == '0' for col in [
            'annual_salary', 'regular_earnings', 'overtime_earnings',
            'other_earnings', 'ytd_gross_earnings'
    ])


def fix_null(row):
    for col in row:
        if row[col] == 'NULL':
            row[col] = '"NULL"'

    return row


def fix_subtitle(row):
    subtitle = row['subtitle'].replace(row['agency'], '').strip(' -')
    row['subtitle'] = subtitle

    return row


date_re = re.compile(r'(\d\d?)\D(\d\d?)\D(\d\d?)')


def fix_term(row):
    term_match = date_re.match(row['term_date'])
    if term_match:
        month, day, year = term_match[1], term_match[2], term_match[3]
        year = '19' + year if year > '18' else '20' + year
        term_date = f'{year}-{month.zfill(2)}-{day.zfill(2)}'
        row['term_date'] = term_date

    return row


def create_db(output_db, csvfile, table):
    csvs_cli.main([
        '-t', table,
        '-f', 'first_name',
        '-f', 'middle_initial',
        '-f', 'last_name',
        '-f', 'suffix',
        '-f', 'organization',
        '-f', 'subtitle',
        csvfile, output_db,
    ], standalone_mode=False)


if __name__ == "__main__":
    main()
