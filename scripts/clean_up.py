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

orgs = {
  "BALTO CITY COMMUNITY COLLEGE": "Baltimore City Community College",
  "BD-MD TCHR\u0026ST EMP SUPP RET PLN": "Maryland Teachers and State Employees Supplemental Retirement Plans",
  "BOARD OF PUBLIC WORKS": "Board Of Public Works",
  "CANAL PLACE PRESERV \u0026 DEV AUTH": "Canal Place Preservation and Development Authority",
  "COMPTROLLER OF MARYLAND": "Comptroller of Maryland",
  "DEPARTMENT OF AGRICULTURE": "Department of Agriculture",
  "DEPARTMENT OF GENERAL SERVICES": "Department of General Services",
  "DEPARTMENT OF STATE POLICE": "Department of State Police",
  "DEPARTMENT OF THE ENVIRONMENT": "Department of the Environment",
  "DEPARTMENT OF TRANSPORTATION": "Department of Transportation",
  "DEPARTMNT OF NATURAL RESOURCES": "Department of Natural Resources",
  "DEPT HOUSING \u0026 COMMUNITY DEV": "Department Housing and Community Development",
  "DEPT HOUSING AND COMMUNITY DEV": "Department Housing and Community Development",
  "DEPT OF AGRICULTURE": "Department of Agriculture",
  "DEPT OF ASSESSMENTS \u0026 TAXATION": "Deparment of Assessments and Taxation",
  "DEPT OF BUDGET AND MANAGEMENT": "Department of Budget and Management",
  "DEPT OF COMMERCE": "Department of Commerce",
  "DEPT OF ENVIRONMENT": "Department of Environment",
  "DEPT OF INFORMATION TECH": "Department of Information Technology",
  "DEPT OF JUVENILE SERVICES": "Department of Juvenile Services",
  "DEPT OF LABOR, LICENSING \u0026 REG": "Department of Labor, Licensing and Regulation",
  "DEPT OF NATURAL RESOURCES": "Department of Natural Resources",
  "DEPT OF NATURAL RESOURES": "Department of Natural Resoures",
  "DEPT OF PUB SAFETY \u0026 COR SERV": "Department of Public Safety and Correctional Services",
  "DEPT OF PUB SAFETY \u0026 COR SERVS": "Department of Public Safety and Correctional Services",
  "DEPT OF THE ENVIRONMENT": "Department of the Environment",
  "EXECUTIVE DEPARTMENT": "Executive Department",
  "EXECUTIVE DEPT": "Executive Department",
  "GENERAL ASSEMBLY OF MARYLAND": "General Assembly of Maryland",
  "GOVERNOR'S OFFICE FOR CHILDREN": "Governor's Office for Children",
  "HISTORIC ST. MARY'S CITY COMM": "Historic St. Mary's City Commission",
  "JUDICIARY": "Judiciary",
  "MARYLAND DEPARTMENT OF HEALTH": "Maryland Department of Health",
  "MARYLAND HIGHER EDUCATION COMM": "Maryland Higher Education Commission",
  "MARYLAND INSURANCE ADMIN": "Insurance Administration",
  "MARYLAND OFFICE OF PLANNING": "Office Of Planning",
  "MARYLAND SCHOOL FOR THE DEAF": "Maryland School for the Deaf",
  "MARYLAND TAX COURT": "Maryland Tax Court",
  "MARYLAND529": "Maryland 529",
  "MD AFRICAN AMERICAN MUSEUM": "Maryland African American Museum",
  "MD COMMISSION ON CIVIL RIGHTS": "Maryland Commission On Civil Rights",
  "MD DEPT OF HUMAN SERVICES": "Department of Human Services",
  "MD DEPT OF VETERANS AFFAIRS": "Maryland Department of Veterans Affairs",
  "MD ENERGY ADMINISTRATION": "State Energy Administration",
  "MD FOOD CENTER AUTHORITY": "Maryland Food Center Authority",
  "MD HEALTH BENEFIT EXCHANGE": "Health Benefit Exchange",
  "MD INS FOR EMERG MED SERV SYS": "Maryland Institute for Emergency Medical Services Systems",
  "MD PUBLIC BROADCASTING COM": "Maryland Public Broadcasting Commission",
  "MD ST BRD OF CONTRACT APPEALS": "State Board of Contract Appeals",
  "MD STADIUM AUTHORITY": "Maryland Stadium Authority",
  "MD UNINSURED EMPLOYERS' FUND": "Maryland Uninsured Employers' Fund",
  "MILITARY DEPARTMENT": "Military Department",
  "MORGAN STATE UNIVERSITY": "Morgan State University",
  "OFFICE OF ADMNSTRTV HEARINGS": "Office Of Administrative Hearings",
  "OFFICE OF PEOPLE'S COUNSEL": "Office Of People's Counsel",
  "OFFICE OF STATE PROSECUTOR": "Office of State Prosecutor",
  "OFFICE OF THE ATTORNEY GENERAL": "Office Of the Attorney General",
  "OFFICE OF THE PUBLIC DEFENDER": "Office of the Public Defender",
  "OFFICE ON AGING": "Office on Aging",
  "PROPERTY TAX ASSMTS APPEAL BDS": "Property Tax Assessment Appeals Boards",
  "PUBLIC SERVICE COMMISSION": "Public Service Commission",
  "REGISTER OF WILLS": "Register of Wills",
  "SECRETARY OF STATE": "Secretary of State",
  "ST ADM BOARD OF ELECTION LAWS": "State Board Of Elections",
  "ST. MARY'S COLLEGE OF MARYLAND": "St. Mary's College of Maryland",
  "STATE ARCHIVES": "State Archives",
  "STATE DEPARTMENT OF EDUCATION": "State Department of Education",
  "STATE LOTTERY AGENCY": "State Lottery Agency",
  "STATE RETIREMENT AGENCY": "State Retirement Agency",
  "STATE TREASURER": "State Treasurer",
  "STATE UNIVERSITIES \u0026 COLLEGES": "State Universities and Colleges",
  "SUBSEQUENT INJURY FUND": "Subsequent Injury Fund",
  "UNIVERSITY OF MARYLAND": "University of Maryland",
  "WORKERS' COMPENSATION COM": "Workers' Compensation Commision",
}


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

    for f in [fix_null, fix_org, fix_subtitle, fix_term]:
        objs = map(f, objs)

    objs = sorted(objs, key=sort_key)

    with open(outname, 'w') as fo:
        dw = csv.DictWriter(fo, fieldnames)
        dw.writeheader()
        for obj in objs:
            dw.writerow(obj)


def not_zero(row):
    return not all(
        row[col] == '0'
        for col in [
            'annual_salary', 'regular_earnings', 'overtime_earnings',
            'other_earnings', 'ytd_gross_earnings'
        ]
        if row[col]
    )


def fix_null(row):
    for col in row:
        if row[col] == 'NULL':
            row[col] = 'NULL '

    return row


def fix_org(row):
    row['organization'] = orgs[row['organization']]

    return row


def fix_subtitle(row):
    subtitle = row['subtitle'].replace(row['agency'], '').strip(' -')
    row['subtitle'] = subtitle

    return row


date_re = re.compile(r'(\d\d?)\D(\d\d?)\D(\d\d?)')


def fix_term(row):
    term_date = ''  # Default to remove zeros
    term_match = date_re.match(row['term_date'])
    if term_match:
        month, day, year = term_match[1], term_match[2], term_match[3]
        year = '19' + year if year > '18' else '20' + year
        term_date = f'{year}-{month.zfill(2)}-{day.zfill(2)}'

    row['term_date'] = term_date

    return row


def sort_key(obj):
    return (
        obj['last_name'],
        obj['first_name'],
        obj['middle_initial'],
        obj['ytd_gross_earnings'],
    )


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
