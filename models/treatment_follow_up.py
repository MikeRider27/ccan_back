import datetime

from db import db, BaseModel
from models.doctor import DoctorModel
from models.hospital import HospitalModel
from models.patient import PatientModel
from models.treatment_plan import TreatmentPlanModel


class TreatmentFollowUpModel(BaseModel):
    __tablename__ = 'treatment_follow_up'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    hospital_id = db.Column(db.BigInteger, db.ForeignKey(HospitalModel.id))
    follow_up_date = db.Column(db.Date)
    last_cancer_control_date = db.Column(db.Date)
    type_treatment = db.Column(db.String(30))
    breast = db.Column(db.String(30))
    armpit = db.Column(db.Boolean)
    suspension_treatment = db.Column(db.Boolean)
    suspension_treatment_reason = db.Column(db.String)
    suspension_treatment_custom_reason = db.Column(db.String(30))
    congestive_heart_failure = db.Column(db.Boolean)
    fevi_follow_up_date = db.Column(db.Date)
    fevi_value = db.Column(db.Integer)
    fevi_trastuzumab_dose = db.Column(db.Integer)
    other_severe_adverse_events = db.Column(db.Boolean)
    other_severe_adverse_events_detail = db.Column(db.String)
    other_complementary_studies = db.Column(db.String)
    dose_adjustment = db.Column(db.Boolean)
    dose_adjustment_reason = db.Column(db.String(100))
    comentaries = db.Column(db.String)
    doctor_id = db.Column(db.BigInteger, db.ForeignKey(DoctorModel.id))
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30), nullable=False)
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    hospital = db.relationship('HospitalModel', foreign_keys=[hospital_id], uselist=False)
    doctor = db.relationship('DoctorModel', foreign_keys=[doctor_id], uselist=False)
    medicine_list = db.relationship('MedicineTreatmentFollowUpModel', cascade="all, delete-orphan")
    treatment_plan_list = db.relationship('TreatmentPlanModel', secondary='follow_up_treatment_plan')

    def __init__(self, id, patient_id, hospital_id, follow_up_date, last_cancer_control_date, type_treatment, breast, armpit,
                 suspension_treatment, suspension_treatment_reason, suspension_treatment_custom_reason,
                 congestive_heart_failure, fevi_follow_up_date, fevi_value, fevi_trastuzumab_dose,
                 other_severe_adverse_events, other_severe_adverse_events_detail, other_complementary_studies,
                 dose_adjustment, dose_adjustment_reason, comentaries,
                 doctor_id, date_create=None, user_create=None, date_modify=None, user_modify=None):
        self.id = id
        self.patient_id = patient_id
        self.hospital_id = hospital_id
        self.follow_up_date = follow_up_date
        self.last_cancer_control_date = last_cancer_control_date
        self.type_treatment = type_treatment
        self.breast = breast
        self.armpit = armpit
        self.suspension_treatment = suspension_treatment
        self.suspension_treatment_reason = suspension_treatment_reason
        self.suspension_treatment_custom_reason = suspension_treatment_custom_reason
        self.congestive_heart_failure = congestive_heart_failure
        self.fevi_follow_up_date = fevi_follow_up_date
        self.fevi_value = fevi_value
        self.fevi_trastuzumab_dose = fevi_trastuzumab_dose
        self.other_severe_adverse_events = other_severe_adverse_events
        self.other_severe_adverse_events_detail = other_severe_adverse_events_detail
        self.other_complementary_studies = other_complementary_studies
        self.dose_adjustment = dose_adjustment
        self.dose_adjustment_reason = dose_adjustment_reason
        self.comentaries = comentaries
        self.doctor_id = doctor_id
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'hospital_id': self.hospital_id,
            'follow_up_date': self.follow_up_date.strftime("%d/%m/%Y") if self.follow_up_date else None,
            'last_cancer_control_date': self.last_cancer_control_date.strftime("%d/%m/%Y") if self.last_cancer_control_date else None,
            'type_treatment': self.type_treatment,
            'breast': self.breast,
            'armpit': self.armpit,
            'suspension_treatment': self.suspension_treatment,
            'suspension_treatment_reason': self.suspension_treatment_reason,
            'suspension_treatment_custom_reason': self.suspension_treatment_custom_reason,
            'congestive_heart_failure': self.congestive_heart_failure,
            'fevi_follow_up_date': self.fevi_follow_up_date.strftime("%d/%m/%Y") if self.fevi_follow_up_date else None,
            'fevi_value': self.fevi_value,
            'fevi_trastuzumab_dose': self.fevi_trastuzumab_dose,
            'other_severe_adverse_events': self.other_severe_adverse_events,
            'other_severe_adverse_events_detail': self.other_severe_adverse_events_detail,
            'other_complementary_studies': self.other_complementary_studies,
            'dose_adjustment': self.dose_adjustment,
            'dose_adjustment_reason': self.dose_adjustment_reason,
            'comentaries': self.comentaries,
            'doctor_id': self.doctor_id,
            'date_create': self.date_create.strftime("%d/%m/%Y %H:%M:%S") if self.date_create else None,
            'user_create': self.user_create,
            'date_modify': self.date_modify.strftime("%d/%m/%Y %H:%M:%S") if self.date_modify else None,
            'user_modify': self.user_modify,
        }

        if jsondepth > 0:
            if self.patient:
                json['patient'] = self.patient.json(jsondepth - 1)
            if self.hospital:
                json['hospital'] = self.hospital.json(jsondepth - 1)
            if self.doctor:
                json['doctor'] = self.doctor.json(jsondepth - 1)
            json['medicine_list'] = []
            if self.medicine_list:
                for medicine in self.medicine_list:
                    json['medicine_list'].append(medicine.json(jsondepth - 1))
            json['treatment_plan_list'] = [
                {'treatment_plan': x.json(1), 'treatment_plan_id': x.id, 'chemotherapy_id': self.id} for x in
                self.treatment_plan_list] if self.treatment_plan_list else []
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

