import datetime
import logging
from enum import Enum

from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from dao.patient_dao import PatientDao
from db import db, BaseModel
from models.area import AreaModel
from models.city import CityModel
from models.country import CountryModel
from models.document_type import DocumentTypeModel
from models.gender import GenderModel
from models.parameter import ParameterModel
from utils import decrypt_data, get_encrypt_db, get_treatment_plan_dates
import uuid
from sqlalchemy.dialects.postgresql import UUID

class OriginsCode(Enum):
    SIGAP = 'SIGAP'
    HIS = 'HIS'
    SECCUMA = 'SECCUMA'
    SICIAP = 'SICIAP'
    CCAN_CITY_SOFT = 'CCAN'


class PatientModel(BaseModel):
    __tablename__ = 'patient'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    document_number = db.Column(db.String(50), nullable=False)
    state_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id), nullable=False)
    vital_state_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id), nullable=False)
    birthdate = db.Column(db.Date)
    address = db.Column(db.String(500))
    gender_id = db.Column(db.BigInteger, db.ForeignKey(GenderModel.id), nullable=False)
    phone = db.Column(db.String(100))
    document_type_id = db.Column(db.BigInteger, db.ForeignKey(DocumentTypeModel.id), nullable=False)
    country_id = db.Column(db.BigInteger, db.ForeignKey(CountryModel.id), nullable=False)
    area_id = db.Column(db.BigInteger, db.ForeignKey(AreaModel.id), nullable=False)
    city_id = db.Column(db.BigInteger, db.ForeignKey(CityModel.id), nullable=False)
    nationality_id = db.Column(db.BigInteger, db.ForeignKey(CountryModel.id), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    civil_status_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    responsible_firstname = db.Column(db.String)
    responsible_lastname = db.Column(db.String)
    responsible_relationship = db.Column(db.String)
    responsible_phone = db.Column(db.String(50))
    number_card = db.Column(db.BigInteger)
    origin = db.Column(db.String, default=OriginsCode.CCAN_CITY_SOFT.value)
    uuid = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4, unique=True)

    # Relationship
    gender = db.relationship('GenderModel', foreign_keys=[gender_id], uselist=False)
    document_type = db.relationship('DocumentTypeModel', foreign_keys=[document_type_id], uselist=False)
    state = db.relationship('ParameterModel', foreign_keys=[state_id], uselist=False)
    vital_state = db.relationship('ParameterModel', foreign_keys=[vital_state_id], uselist=False)
    country = db.relationship('CountryModel', foreign_keys=[country_id], uselist=False)
    area = db.relationship('AreaModel', foreign_keys=[area_id], uselist=False)
    city = db.relationship('CityModel', foreign_keys=[city_id], uselist=False)
    nationality = db.relationship('CountryModel', foreign_keys=[nationality_id], uselist=False)
    civil_status = db.relationship('ParameterModel', foreign_keys=[civil_status_id], uselist=False)
    hospital_list = db.relationship('PatientHospitalModel')

    # Relación con diagnosis
    diagnosis_list = db.relationship("DiagnosisModel", back_populates="patient", lazy='dynamic')

    # Relación con treatment_plan
    treatment_plan_list = db.relationship("TreatmentPlanModel", back_populates="patient", lazy='dynamic')

    @hybrid_property
    def origins(self):
        patient_dao = PatientDao()
        origins = patient_dao.get_patient_origins(self.id)
        origins_format = None
        if origins:
            origins = list(map(lambda x: x.origin, origins))
            origins = set(map(lambda x: x if x is not None else OriginsCode.CCAN_CITY_SOFT.value, origins))
            origins_order = []
            # Set order
            if OriginsCode.SIGAP.value in origins:
                origins_order.append(OriginsCode.SIGAP.value)
            if OriginsCode.HIS.value in origins:
                origins_order.append(OriginsCode.HIS.value)
            if OriginsCode.SECCUMA.value in origins:
                origins_order.append(OriginsCode.SECCUMA.value)
            # if OriginsCode.CCAN_CITY_SOFT.value in origins:
            #     origins_order.append(OriginsCode.CCAN_CITY_SOFT.value)
            origins_format = " - ".join(origins_order)
            return origins_format
        return origins_format

    def __init__(self, id=None, firstname=None, lastname=None, document_number=None, state_id=None, birthdate=None,
                 address=None, gender_id=None, document_type_id=None, country_id=None, area_id=None, city_id=None,
                 nationality_id=None, phone=None, vital_state_id=None, registration_date=None, civil_status_id=None,
                 responsible_firstname=None, responsible_lastname=None, responsible_relationship=None,
                 responsible_phone=None, number_card=None, date_create=None, user_create=None, date_modify=None,
                 user_modify=None, origin=None, uuid=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.document_number = document_number
        self.state_id = state_id
        self.birthdate = birthdate
        self.address = address
        self.gender_id = gender_id
        self.document_type_id = document_type_id
        self.country_id = country_id
        self.area_id = area_id
        self.city_id = city_id
        self.nationality_id = nationality_id
        self.phone = phone
        self.vital_state_id = vital_state_id
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.registration_date = registration_date
        self.civil_status_id = civil_status_id
        self.responsible_firstname = responsible_firstname
        self.responsible_lastname = responsible_lastname
        self.responsible_relationship = responsible_relationship
        self.responsible_phone = responsible_phone
        self.number_card = number_card
        self.origin = origin
        self.uuid = uuid

    def json(self, jsondepth=0):
        cipher_key = current_app.config['ENCRYPTION_KEY']
        json = {
            'id': self.id,
            'firstname': db.session.query(decrypt_data(self.firstname, cipher_key)).scalar(),
            'lastname': db.session.query(decrypt_data(self.lastname, cipher_key)).scalar(),
            'document_number': db.session.query(decrypt_data(self.document_number, cipher_key)).scalar(),
            'state_id': self.state_id,
            'birthdate': self.birthdate.strftime("%d/%m/%Y") if self.birthdate else None,
            'address': self.address,
            'gender_id': self.gender_id,
            'phone': self.phone,
            'document_type_id': self.document_type_id,
            'country_id': self.country_id,
            'area_id': self.area_id,
            'city_id': self.city_id,
            'nationality_id': self.nationality_id,
            'vital_state_id': self.vital_state_id,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'registration_date': self.registration_date.strftime("%d/%m/%Y") if self.registration_date else None,
            'civil_status_id': self.civil_status_id,
            'responsible_firstname': self.responsible_firstname,
            'responsible_lastname': self.responsible_lastname,
            'responsible_relationship': self.responsible_relationship,
            'responsible_phone': self.responsible_phone,
            'number_card': self.number_card,
            'last_diagnosis': self.get_latest_diagnosis(jsondepth),
            'last_treatment_plan': self.get_latest_treatment_plan(jsondepth),
            'treatment_plan_progress': self.get_treatment_plan_progress(),
            'origins': self.get_origins(),
            'uuid': str(self.uuid),
        }

        if jsondepth > 0:
            if self.gender:
                json['gender'] = self.gender.json(jsondepth - 1)
            if self.document_type:
                json['document_type'] = self.document_type.json(jsondepth - 1)
            if self.state:
                json['state'] = self.state.json(jsondepth - 1)
                json['state_code'] = json.get('state', {}).get('code', None)
            if self.vital_state:
                json['vital_state'] = self.vital_state.json(jsondepth - 1)
            if self.country:
                json['country'] = self.country.json(jsondepth - 1)
            if self.area:
                json['area'] = self.area.json(jsondepth - 1)
            if self.city:
                json['city'] = self.city.json(jsondepth - 1)
            if self.nationality:
                json['nationality'] = self.nationality.json(jsondepth - 1)
            if self.civil_status:
                json['civil_status'] = self.civil_status.json(jsondepth - 1)
            json['hospital_list'] = [x.json(1) for x in self.hospital_list] if self.hospital_list else []
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def get_latest_diagnosis(self, jsondepth):
        last_diagnosis = None
        if self.diagnosis_list.count() != 0:
            last_diagnosis = max(self.diagnosis_list, key=lambda x: x.date_create)

        if last_diagnosis:
            return last_diagnosis.json(jsondepth)
        return None

    def get_latest_treatment_plan(self, jsondepth):
        last_treatment_plan = None
        if self.treatment_plan_list.count() != 0:
            list_has_state = list(filter(lambda x: x.state is not None, self.treatment_plan_list))
            list_in_progress = list(filter(lambda x: x.state.value == 'EN CURSO', list_has_state))
            if len(list_in_progress) > 0:
                last_treatment_plan = max(list_in_progress, key=lambda x: x.date_create)

        if last_treatment_plan:
            return last_treatment_plan.json(jsondepth)
        return None

    def get_treatment_plan_progress(self):
        plans = []
        tp_list = self.treatment_plan_list.all()
        if len(tp_list) > 0:
            list_has_state = list(filter(lambda x: x.state is not None, self.treatment_plan_list))
            list_in_progress = list(filter(lambda x: x.state.value == 'EN CURSO', list_has_state))
            if list_in_progress and len(list_in_progress):
                for treatment_plan_active in list_in_progress:
                    date_first_cycle = treatment_plan_active.date_first_cycle
                    periodicity = treatment_plan_active.periodicity
                    number_sessions = treatment_plan_active.number_sessions
                    plan = get_treatment_plan_dates(date_first_cycle=date_first_cycle, periodicity=periodicity,
                                                     number_sessions=number_sessions, db=db, treatment_plan=treatment_plan_active)
                    plans.append(plan)

                # Order
                try:
                    plans = sorted(plans, key=lambda x: x.get('treatment_plan_number', 0) if x else 0)
                except Exception as error:
                    logging.error(f"Ocurrió un error al ordenar la lista de planes. Detalle: {error}")
        return plans

    def encript_data(self):
        cipher_key = current_app.config['ENCRYPTION_KEY']
        self.firstname = get_encrypt_db(db, self.firstname, cipher_key)
        self.lastname = get_encrypt_db(db, self.lastname, cipher_key)
        self.document_number = get_encrypt_db(db, self.document_number, cipher_key)

    def save_to_db(self, encrypt=True):
        if encrypt:
            self.encript_data()

        super().save_to_db()

    def get_origins(self):
        # Importar los modelos dentro del método para evitar circular imports
        from models.dispatch_medications import DispatchMedicationsModel
        from models.medical_consultation import MedicalConsultationModel

        dispatch_medicaments_origin = DispatchMedicationsModel.query.filter_by(patient_id=self.id, origin='SICIAP').first()
        medical_consultation_origin = MedicalConsultationModel.query.filter_by(patient_id=self.id, origin ='HIS').first()

        origins = set()
        if self.origins:
            origins.add(self.origins)

        if dispatch_medicaments_origin:
            origins.add(dispatch_medicaments_origin.origin)
        if medical_consultation_origin:
            origins.add(medical_consultation_origin.origin)
        return list(origins) if origins else None
