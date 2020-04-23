from Date import db
from Date import User

db.create_all()
a = db.select(["* FROM user"])
db.session.commit()
a = db.session.execute(a)
print(a)

temp.all()
Out[4]: [<User 'admin'>]
print(temp.all())
[<User 'admin'>]
a = temp.all()
type(a[0])
Out[7]: Date.User
a[0].id
Out[8]: 1
a[0].username
Out[9]: 'admin'

temp = User.query.filter_by(id="1")
