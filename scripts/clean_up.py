import csv
import re

date_re = re.compile(r'(\d\d?)\D(\d\d?)\D(\d\d?)')
inname = 'data/cy2017-md.csv'
outname = 'data/cy2017-md-updated.csv'
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


print()

with open(inname) as fi, open(outname, 'w') as fo:
    dr = csv.DictReader(fi)
    dw = csv.DictWriter(fo, fieldnames)
    dw.writeheader()
    #
    for i, row in enumerate(dr):
        print("%s" % "\\|/-"[i%4], end='\r')
        if all(row[col] == '0' for col in [
            'annual_salary', 'regular_earnings', 'overtime_earnings', 'other_earnings', 'ytd_gross_earnings'
        ]):
            continue
        #
        if row['last_name'] == 'NULL':
            row['last_name'] = '"NULL"'
        #
        subtitle = row['subtitle'].replace(row['agency'], '').strip(' -')
        row['subtitle'] = subtitle
        #
        term_date = ''
        term_match = date_re.match(row['term_date'])
        if term_match:
            month, day, year = term_match[1], term_match[2], term_match[3]
            year = '19' + year if year > '18' else '20' + year
            term_date = f'{year}-{month.zfill(2)}-{day.zfill(2)}'
        #
        row['term_date'] = term_date
        dw.writerow(row)

print()
