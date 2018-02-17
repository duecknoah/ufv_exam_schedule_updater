from setuptools import setup
import json
import set_courses
from getpass import getpass

setup(name='ufv_exam_schedule_checker',
      version='0.1',
      description='',
      author='Noah Dueck',
      author_email='duecknoah@gmail.com',
      install_requires=[
          'bs4', 'PrettyTable'
      ],
      zip_safe=False)

settings_file = open('settings.json', 'w+')

json_data = {
    'crns': None
}

# CRNS input
print('Getting input for your course numbers (CRNs) ...')
json_data['crns'] = set_courses.input_courses()

# URL examination page input
json_data['url'] = input('URL of UFV Exam schedule page: ')
json_data['ifttt_event'] = input('IFTTT event name: ')
json_data['ifttt_secret_key'] = getpass('IFTTT secret key: ')

json.dump(json_data, settings_file)
settings_file.close()

print('Setup completed successfully')