import urllib.request
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import json
import logging

HEADINGS = (
    'COURSE', 'SECTION', 'CRN', 'Date',
    'TIME', 'Location', 'INSTRUCTOR', 'INFO'
)

def load_exam_table():
    """Grabs the exam table from
    the exam url and returns it
    """
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    # The web page with the exam schedule
    html_doc = urllib.request.urlopen(settings['url'])

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
        settings = json.load(f)

    exam_table = load_exam_table()
    all_c_data = table_to_list(exam_table)
    course_data_as_list = get_exam_data_from(settings['crns'], all_c_data)

    return _convert_exams_to_dict_format(course_data_as_list)

def save_exam_data(exams):
    """Saves the exam """

if __name__ == '__main__':

    with open('settings.json', 'r') as f:
        settings = json.load(f)

    # Course numbers you are taking
    myCRNs = settings['crns']
    my_course_data = get_exam_data_for_crns(myCRNs)
    print_exams(my_course_data)