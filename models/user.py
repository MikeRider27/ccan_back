import datetime

from db import db, BaseModel
from utils import sha1_pass


class UserModel(BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    user = db.Column(db.String(100), nullable=False, unique=True)
    state = db.Column(db.String(1), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    administrator = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(50))
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))

    # Relationship
    # hospital = db.relationship(HospitalModel, secondary='user_hospital')
    # role = db.relationship(RoleModel, secondary='user_hospital')
    role_list = db.relationship('UserRoleModel')

    def __init__(self, id, user, state, password, firstname, lastname, administrator, email, role_list,
                 date_create=None, user_create=None, date_modify=None, user_modify=None):
        self.id = id
        self.user = user
        self.state = state
        self.password = sha1_pass(password)
        self.firstname = firstname
        self.lastname = lastname
        self.administrator = administrator
        self.email = email
        self.role_list = role_list
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'user': self.user,
            'state': self.state,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'administrator': self.administrator,
            'email': self.email,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
        }

        if jsondepth > 0:
            # if self.hospital:
            #     json['hospital'] = [x.json(jsondepth) for x in self.hospital].pop()
            # if self.role:
            #     json['role'] = [x.json() for x in self.role].pop()
            if self.role_list:
                json['role_list'] = [x.json(jsondepth) for x in self.role_list]
            else:
                json['role_list'] = [{}]
        
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_user(cls, user):
        return cls.query.filter_by(user=user).first()