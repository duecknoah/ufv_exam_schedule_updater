import urllib.request, urllib.error
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import json
import logging
import pickle
import unicodedata

def setup_exam_logger(logger):
    """Sets up the logger with the proper settings
    to be considered the logger for exam changes
    """
    logger.setLevel(logging.INFO)
    # File handler for logging messages to a file
    fh = logging.FileHandler('exam_changes.log')
    fh.setLevel(logging.INFO)
    # Create formatter, then add it to the handlers
    formatter = logging.Formatter('%(asctime)s :: %(message)s')
    fh.setFormatter(formatter)
    # Add handlers to the logger
    logger.addHandler(fh)

exam_logger = logging.getLogger('exam_changelog')
setup_exam_logger(exam_logger)

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
    """Converts the HTML table to a list.
    Each index is its own list containing
    course data values corresponding to the order of
    HEADINGS
    """

    data = []

    # Go through the rows in the table, sanitize the
    # text in the column and append it to the list
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [remove_ctrl_chars(ele.text.strip()) for ele in cols]
        data.append(cols)

    return data

def remove_ctrl_chars(str):
    """Removes control characters from a string and
    returns then it.

    Control characters are characters such as newlines '\n'
    where they are used to display the string differently.
    """
    return ''.join(ch for ch in str if unicodedata.category(ch)[0]!="C")

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
                crns.remove(crn)
                break
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
    """Compares two sets of exam data and
    Logs changes made to the exam data to the logger.

    Returns the data that was changed (changed_data)
    """
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    changed_data = []
    for crn_idx, (e_new, e_old) in enumerate(zip(exam_data, old_exam_data)):
        # We are iterating the dictionary which may become out of order.
        # So we iterate through the HEADINGS tuple and then use that as
        # the heading to look at for the category of the course
        for h in HEADINGS:
            # Get data from category
            d_old = e_old[h]
            d_new = e_new[h]

            # If the old exam data under this heading differs from the new,
            # log that it changed!
            if d_new != d_old:
                crn = SETTINGS['crns'][crn_idx]
                change_str = 'CRN {}: {} changed from {} to {}'.format(crn, h, d_old, d_new)
                changed_data.append(change_str)
                exam_logger.info(change_str)
    return changed_data

def save_exam_data(exam_data):
    """Saves most recent exam data for comparing to later"""
    pickle.dump(exam_data, open(LAST_CHECK_FILENAME, 'wb+'))

def check():
    """Checks and updates the user if any exam information
    has changed

    Returns any changed data in a list
    """
    with open('settings.json', 'r') as f:
        SETTINGS = json.load(f)

    # Course numbers you are taking
    myCRNs = SETTINGS['crns']
    my_exam_data = get_exam_data_for_crns(myCRNs)
    try:
        old_exam_data = pickle.load(open(LAST_CHECK_FILENAME, 'rb'))
        print_exams(my_exam_data)
        changed_data = compare_exam_data(my_exam_data, old_exam_data)
        save_exam_data(my_exam_data)
        return changed_data
    except (EOFError, FileNotFoundError):
        logging.debug('Error reading old exam data, assuming this is first check')
        print_exams(my_exam_data)
        save_exam_data(my_exam_data)
        return None

if __name__ == '__main__':
    print('Note: This script can automatically keep running by executing autorun.py instead.')
    check()