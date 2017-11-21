from setuptools import setup
import json
import set_courses

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
    'email': None,
    'crns': None
}
# Email input
json_data['email'] = input('Email to be notified for changes: ')

# CRNS input
print('Getting input for your course numbers (CRNs) ...')
json_data['crns'] = set_courses.input_courses()

# URL examination page input
json_data['url'] = input('URL of UFV Exam schedule page: ')

json.dump(json_data, settings_file)
settings_file.close()

print('Setup completed successfully')