import base64
import datetime

from flask_restful.reqparse import Namespace
from sqlalchemy.dialects.sqlite import JSON

from db import db, BaseModel
from models.medical_document import MedicalDocumentModel
from models.medical_document_type import MedicalDocumentTypeModel
from models.parameter import ParameterModel
from models.patient import PatientModel


class PatientInclusionCriteriaNeoadjuvantTrastuzumabModel(BaseModel):
    __tablename__ = 'patient_inclusion_criteria_neoadjuvant_trastuzumab'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    diagnosed_invasive_adenocarcinoma = db.Column(db.Boolean)
    neoadjuvant_trastuzumab_her2_positive = db.Column(db.Boolean)
    her2_positive_id = db.Column(JSON)
    determination_hormone_receptors = db.Column(db.Boolean)
    tumor_eq_ge_2cm = db.Column(db.Boolean)
    positive_axilla = db.Column(db.Boolean)
    marked_tumor_bed = db.Column(db.Boolean)
    blood_count_renal_hepatic_appropriate = db.Column(db.Boolean)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))
    tumor_size_diameter_determined_by = db.Column(db.String(30))
    positive_armpit_determined_by = db.Column(db.String(30))

    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)

    def __init__(self, id=None, patient_id=None, diagnosed_invasive_adenocarcinoma=None,
                 neoadjuvant_trastuzumab_her2_positive=None, her2_positive_id=None, determination_hormone_receptors=None,
                 tumor_eq_ge_2cm=None, positive_axilla=None, marked_tumor_bed=None, blood_count_renal_hepatic_appropriate=None,
                 date_create=None, user_create=None, date_modify=None, user_modify=None,
                 tumor_size_diameter_determined_by=None, positive_armpit_determined_by=None):
        self.id = id
        self.patient_id = patient_id
        self.diagnosed_invasive_adenocarcinoma = diagnosed_invasive_adenocarcinoma
        self.neoadjuvant_trastuzumab_her2_positive = neoadjuvant_trastuzumab_her2_positive
        self.her2_positive_id = her2_positive_id
        self.determination_hormone_receptors = determination_hormone_receptors
        self.tumor_eq_ge_2cm = tumor_eq_ge_2cm
        self.positive_axilla = positive_axilla
        self.marked_tumor_bed = marked_tumor_bed
        self.blood_count_renal_hepatic_appropriate = blood_count_renal_hepatic_appropriate
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.tumor_size_diameter_determined_by = tumor_size_diameter_determined_by
        self.positive_armpit_determined_by = positive_armpit_determined_by

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'diagnosed_invasive_adenocarcinoma': self.diagnosed_invasive_adenocarcinoma,
            'neoadjuvant_trastuzumab_her2_positive': self.neoadjuvant_trastuzumab_her2_positive,
            'her2_positive_id': self.her2_positive_id,
            'determination_hormone_receptors': self.determination_hormone_receptors,
            'tumor_eq_ge_2cm': self.tumor_eq_ge_2cm,
            'positive_axilla': self.positive_axilla,
            'marked_tumor_bed': self.marked_tumor_bed,
            'blood_count_renal_hepatic_appropriate': self.blood_count_renal_hepatic_appropriate,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
            'tumor_size_diameter_determined_by': self.tumor_size_diameter_determined_by,
            'positive_armpit_determined_by': self.positive_armpit_determined_by,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def patient_included(self):
        # Punto 1
        if not self.diagnosed_invasive_adenocarcinoma:
            return False
        # Punto 2
        if not self.neoadjuvant_trastuzumab_her2_positive:
            return False
        # Punto 3
        if not self.determination_hormone_receptors:
            return False

        punto4 = False
        if self.tumor_eq_ge_2cm:
            if self.tumor_size_diameter_determined_by == 'image':
                mammography_type = MedicalDocumentTypeModel.query.filter_by(description='MAMOGRAFÍA').first()
                mammography_doc = MedicalDocumentModel.query.filter_by(patient_id=self.patient_id, medical_document_type_id=mammography_type.id).all()
                if len(mammography_doc) > 0:
                    punto4 = True
            else:
                punto4 = True

        punto5 = False
        if self.positive_axilla:
            if self.positive_armpit_determined_by == 'ultrasound':
                mammography_type = MedicalDocumentTypeModel.query.filter_by(description='ECOGRAFÍA MAMARIA').first()
                mammography_doc = MedicalDocumentModel.query.filter_by(patient_id=self.patient_id, medical_document_type_id=mammography_type.id).all()
                if len(mammography_doc) > 0:
                    punto5 = True
            else:
                punto5 = True

        # Punto 4 y 5
        if not punto4 and not punto5:
            return False

        # Punto 6 (se deja sin efecto)
        # if not self.marked_tumor_bed:
        #     return False

        # Punto 7
        if not self.blood_count_renal_hepatic_appropriate:
            return False

        return True

    def get_documentos_faltantes(self):
        en_falta = []
        if self.tumor_eq_ge_2cm and self.tumor_size_diameter_determined_by == 'image':
            mammography_type = MedicalDocumentTypeModel.query.filter_by(description='MAMOGRAFÍA').first()
            mammography_doc = MedicalDocumentModel.query.filter_by(patient_id=self.patient_id,
                                                                   medical_document_type_id=mammography_type.id).all()
            if len(mammography_doc) == 0:
                en_falta.append('FALTA INCLUIR DOCUMENTO: MAMOGRAFÍA')


        if self.positive_axilla and self.positive_armpit_determined_by == 'ultrasound':
            mammography_type = MedicalDocumentTypeModel.query.filter_by(description='ECOGRAFÍA MAMARIA').first()
            mammography_doc = MedicalDocumentModel.query.filter_by(patient_id=self.patient_id,
                                                                   medical_document_type_id=mammography_type.id).all()
            if len(mammography_doc) == 0:
                en_falta.append('FALTA INCLUIR DOCUMENTO: ECOGRAFÍA MAMARIA')

        return en_falta
