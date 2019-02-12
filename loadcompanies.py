import json
from acsystem.models import Countries
from acsystem import db

with open('acsystem/countries.json') as c:
    cdata = json.load(c)

for i in cdata['countries']:
     print(i['name'])
     country = Countries(name=i['name'])
     db.session.add(country)
     db.session.commit()
