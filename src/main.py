import bakapi
import credentials
import getpass
import sys

argv = sys.argv

SCHOOL_EP = 'https://gymstola.bakalari.cz'

if '--me' in argv:
    uname = credentials.myname
    passwd = credentials.mypasswd
else:
    uname = input('Name please: ')
    passwd = getpass.getpass('Password please: ') #input('Password please: ')

user = bakapi.BakapiUser(url=SCHOOL_EP, username=uname, password=passwd)
response = user.send_request('/api/3/marks')

subjects_raw = response.json()

for subject in subjects_raw.get('Subjects'):
    marks_raw = subject.get('Marks')

    invalids = []
    for i, mark_raw in enumerate(marks_raw):
        try:
            value = mark_raw.get('MarkText')
            value = value.replace('-', '.5')
            value = float(value)
            
            mark_raw['MarkText'] = value
        except:
            invalids.append(i)
        
    for index in sorted(invalids, reverse=True):
        del marks_raw[index]

    mark_weights = [(float(mark.get('MarkText')), float(mark.get('Weight'))) for mark in marks_raw]
    marks, weights = zip(*mark_weights)
    weighted_marks = [mark * weight for mark, weight in mark_weights]
    average = sum(weighted_marks) / sum(weights)
    rounded_average = round(average, 2)
    # subject['Average'] = average5
    
    print(subject.get('Subject').get('Name'), rounded_average)
