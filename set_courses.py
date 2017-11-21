"""Gets users input for their course numbers (CRNs), then storing it in
the settings.json file for further use.
"""
import json

def input_courses():
    """Gets user input for course numbers, returns a list of the crns entered"""
    do_start = input("Warning: This will reset any set CRNs from before, continue?\nyes(y) no(n): ")

    if (do_start == 'y' or do_start == 'yes'):
        uin = ''
        i = 1
        crns = []

        print('Enter your course numbers (CRNs), type \'done\' to finish.')
        while True:
            uin = input('CRN #{}: '.format(i))

            if uin == 'done':
                break

            try:
                # Validate that it is a number, but
                # store it as a string
                crn = int(uin)
                crns.append(str(crn))
                i += 1
            except ValueError:
                print('Please enter a valid course number (CRN)')
        print(crns)
        print('{} courses entered.'.format(i - 1))
        return crns
    else:
        print("Cancelling ...")
        return None

if __name__ == '__main__':
    course_data = input_courses()

    # Update CRNS in settings.json
    if course_data is not None:
        with open('settings.json') as settings_file:
            current_settings = json.load(settings_file)

        current_settings.update({'crns: ': course_data})

        with open('settings.json', 'w') as settings_file:
            json.dump(course_data, settings_file)
        print('Saved, done.')