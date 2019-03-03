import json
from acsystem.models import FixedGroup, Group
from acsystem import db, create_app
app = create_app()
app.app_context().push()
with open('acsystem/fixedgroup.json') as c:
    cdata = json.load(c)

for i in cdata['fixedgroups']:
     print(i['name'])
    #  group = FixedGroup(name=i['name'], under=i['under'])
     group = Group(name=i['name'], under=i['under'], company_id = 0 )
     db.session.add(group)
     db.session.commit()