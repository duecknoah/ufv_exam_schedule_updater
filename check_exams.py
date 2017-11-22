import urllib.request
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import json

def table_to_list(table):
    """Converts the HTML table to a list"""

    data = []

    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    return data

def get_course_data(crns, all_course_data, crn_index=2):
    """
    Finds and returns the course #'s (CRNs) matching
    in 'all_course_data'.
    Where all_course_data is a list
    courses is a list
    """

    c_data = []
    for d in all_course_data:
        for crn in crns:
            if d[crn_index] == crn:
                c_data.append(d)
    return c_data

def print_exams(headings, courses):
    """Prints all info for your courses' exams"""
    t = PrettyTable(headings)

    for c in courses:
        t.add_row(c)
    print(t)

if __name__ == '__main__':

    with open('settings.json', 'r') as f:
        settings = json.load(f)
    # Course numbers you are taking
    myCRNs = settings['crns']
    # The web page with the exam schedule
    html_doc = urllib.request.urlopen(settings['url'])

    soup = BeautifulSoup(html_doc, 'lxml')
    table = soup.find('table')

    # Make heading names reference the column index they refer to
    # Ex. {'COURSE': 0, 'SECTION': 1, 'CRN': 2}
    headings_text = table.find('tr').get_text().strip().split('\n')
    headings = {}
    for i, hName in enumerate(headings_text):
        headings[hName] = i

    all_c_data = table_to_list(table)
    my_course_data = get_course_data(myCRNs, all_c_data, headings['CRN'])
    print_exams(headings_text, my_course_data)