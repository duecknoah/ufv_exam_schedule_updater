import urllib.request, urllib.error
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import json
import logging
import pickle

logging.basicConfig(filename='exam_changes.log', level=logging.INFO,
                    format='%(asctime)s :: %(message)s')

HEADINGS = (
    'COURSE', 'SECTION', 'CRN', 'Date',
    'TIME', 'Location', 'INSTRUCTOR', 'INFO'
)
LAST_CHECK_FILENAME = 'last_check.dat'
SETTINGS_FILE = 'settings.json'
with open(SETTINGS_FILE, 'r') as f:
    SETTINGS = json.load(f)

def load_exam_table():
    """Grabs the exam table from
    the exam url and returns it
    """
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    # The web page with the exam schedule
    try:
        html_doc = urllib.request.urlopen(settings['url'])
    except (urllib.error.URLError, urllib.error.HTTPError) as urlerr:
        print('Unable to load URL: {}\n{}\nquiting...'.format(settings['url'], urlerr))
        exit(1)

    soup = BeautifulSoup(html_doc, 'lxml')
    return soup.find('table')

def table_to_list(table):
    """Converts the HTML table to a list"""

    data = []

    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    return data

def get_exam_data_from(crns, all_course_data, crn_index=2):
    """
    Finds and returns the course #'s (CRNs) matching
    in 'all_course_data'.
    Where all_course_data is a list
    courses is a list

    crns: a list of the users course numbers
    all_course_data: a list of all the table information
    crn_index: the index in all_course_data where the CRN is
    """

    c_data = []
    for d in all_course_data:
        for crn in crns:
            if d[crn_index] == crn:
                c_data.append(d)
    return c_data

def print_exams(courses):
    """Prints all info for your courses' exams"""
    t = PrettyTable(HEADINGS)

    for c in courses:
        row = []
        for h in HEADINGS:
            row.append(c[h])
        t.add_row(row)
    print(t)

def _convert_exams_to_dict_format(courses_as_list):
    # Convert the format:
    # [['CIS 221', 'AB1' ...], ['COMP 251', ...]]
    # to
    # [{'COURSE': 'CIS 221', 'SECTION': 'AB1', ...}, {'COURSE': 'COMP 251', ...}]
    course_data_as_dict_in_list = []

    for c in courses_as_list:
        c_data = {}
        for h_idx, h in enumerate(HEADINGS):
            c_data[h] = c[h_idx]
        course_data_as_dict_in_list.append(c_data)

    return course_data_as_dict_in_list

def get_exam_data_for_crns(crns):
    """Returns the course data from the course numbers
    as a list,
    where each element is a dict of course info.

    crns: a list of course numbers to get data for

    Note:
        This will load the url in settings and extract table data.
        If you already have all the table data,
        use get_course_data_from(...) instead.
    """

    with open('settings.json', 'r') as f:
        SETTINGS = json.load(f)

    exam_table = load_exam_table()
    all_c_data = table_to_list(exam_table)
    course_data_as_list = get_exam_data_from(SETTINGS['crns'], all_c_data)

    return _convert_exams_to_dict_format(course_data_as_list)

def compare_exam_data(exam_data, old_exam_data):
    """Logs changes made to the exam data"""
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    for crn_idx, (e_new, e_old) in enumerate(zip(exam_data, old_exam_data)):
        for cat_idx, (cat_new, cat_old) in enumerate(zip(e_new, e_old)):
            if cat_old != cat_new:
                logging.error('column {} shouldn\'t have changed from {} to {}, skipping...'.format(cat_idx, cat_old, cat_new))
                continue

            # Get data from category
            d_old = e_old[cat_old]
            d_new = e_new[cat_new]

            if d_new != d_old:
                crn = SETTINGS['crns'][crn_idx]
                logging.info('CRN {}: {} changed from {} to {}'.format(crn, cat_new, d_old, d_new))

def save_exam_data(exam_data):
    """Saves most recent exam data for comparing to later"""
    pickle.dump(exam_data, open(LAST_CHECK_FILENAME, 'wb+'))

def check():
    """Checks and updates the user if any exam information
    has changed
    """
    with open('settings.json', 'r') as f:
        SETTINGS = json.load(f)

    # Course numbers you are taking
    myCRNs = SETTINGS['crns']
    my_exam_data = get_exam_data_for_crns(myCRNs)
    try:
        old_exam_data = pickle.load(open(LAST_CHECK_FILENAME, 'rb'))
        print_exams(my_exam_data)
        compare_exam_data(my_exam_data, old_exam_data)
        save_exam_data(my_exam_data)
    except (EOFError, FileNotFoundError):
        logging.debug('Error reading old exam data, assuming this is first check')
        print_exams(my_exam_data)
        save_exam_data(my_exam_data)
        return


if __name__ == '__main__':
    print('Note: This script can automatically keep running by executing autorun.py instead.')
    check()