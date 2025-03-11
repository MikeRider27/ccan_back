import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.medical_document import MedicalDocumentModel
from models.parameter import ParameterModel
from models.patient import PatientModel


class CervixFormModel(BaseModel):
    __tablename__ = 'cervix_form'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    departament = db.Column(db.String)
    parity = db.Column(db.Boolean)
    residential_address = db.Column(db.String)
    pmhx = db.Column(db.String)
    presenting_complaint = db.Column(db.String)
    main_physical_clinical_findings = db.Column(db.String)
    performance_status_ecog_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    treatment_decision = db.Column(db.String)
    colposcopy_date = db.Column(db.DateTime)
    colposcopy_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    cervical_biopsy_date = db.Column(db.DateTime)
    cervical_biopsy_histology = db.Column(db.String)
    cervical_biopsy_morphology = db.Column(db.String)
    cervical_biopsy_grade = db.Column(db.String)
    usg_pelvis_abdomen_date = db.Column(db.DateTime)
    usg_pelvis_abdomen_site_of_mass_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    usg_pelvis_abdomen_size_of_mass = db.Column(db.String)
    usg_pelvis_abdomen_extensions_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    chest_xray_date = db.Column(db.DateTime)
    chest_xray_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    chest_xray_summary_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    pelvic_mri_date = db.Column(db.DateTime)
    pelvic_mri_site_of_mass_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    pelvic_mri_size_of_mass = db.Column(db.String)
    pelvic_mri_extensions_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    blood_date = db.Column(db.DateTime)
    blood_fbc_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    blood_fbc = db.Column(db.String)
    blood_lft_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    blood_urea_creatinine_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    stage_figo_date = db.Column(db.DateTime)
    stage_figo_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    stage_figo_i_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    stage_figo_ia_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    stage_figo_ib_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    stage_figo_ii_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    stage_figo_iii_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    stage_figo_iv_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30))
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    performance_status_ecog = db.relationship('ParameterModel', foreign_keys=[performance_status_ecog_id], uselist=False)
    colposcopy_report = db.relationship('MedicalDocumentModel', foreign_keys=[colposcopy_report_id], uselist=False)
    usg_pelvis_abdomen_site_of_mass = db.relationship('ParameterModel', foreign_keys=[usg_pelvis_abdomen_site_of_mass_id], uselist=False)
    usg_pelvis_abdomen_extensions = db.relationship('ParameterModel', foreign_keys=[usg_pelvis_abdomen_extensions_id], uselist=False)
    chest_xray_report = db.relationship('MedicalDocumentModel', foreign_keys=[chest_xray_report_id], uselist=False)
    chest_xray_summary = db.relationship('ParameterModel', foreign_keys=[chest_xray_summary_id], uselist=False)
    pelvic_mri_site_of_mass = db.relationship('ParameterModel', foreign_keys=[pelvic_mri_site_of_mass_id], uselist=False)
    pelvic_mri_extensions = db.relationship('ParameterModel', foreign_keys=[pelvic_mri_extensions_id], uselist=False)
    _blood_fbc = db.relationship('ParameterModel', foreign_keys=[blood_fbc_id], uselist=False)
    blood_lft_report = db.relationship('MedicalDocumentModel', foreign_keys=[blood_lft_report_id], uselist=False)
    blood_urea_creatinine_report = db.relationship('MedicalDocumentModel', foreign_keys=[blood_urea_creatinine_report_id], uselist=False)
    stage_figo = db.relationship('ParameterModel', foreign_keys=[stage_figo_id], uselist=False)
    stage_figo_i = db.relationship('ParameterModel', foreign_keys=[stage_figo_i_id], uselist=False)
    stage_figo_ia = db.relationship('ParameterModel', foreign_keys=[stage_figo_ia_id], uselist=False)
    stage_figo_ib = db.relationship('ParameterModel', foreign_keys=[stage_figo_ib_id], uselist=False)
    stage_figo_ii = db.relationship('ParameterModel', foreign_keys=[stage_figo_ii_id], uselist=False)
    stage_figo_iii = db.relationship('ParameterModel', foreign_keys=[stage_figo_iii_id], uselist=False)
    stage_figo_iv = db.relationship('ParameterModel', foreign_keys=[stage_figo_iv_id], uselist=False)


    def __init__(self, id=None, patient_id=None, departament=None, parity=None, residential_address=None, pmhx=None,
                 presenting_complaint=None, main_physical_clinical_findings=None, performance_status_ecog_id=None,
                 treatment_decision=None, colposcopy_date=None, colposcopy_report_id=None, cervical_biopsy_date=None,
                 cervical_biopsy_histology=None, cervical_biopsy_morphology=None, cervical_biopsy_grade=None,
                 usg_pelvis_abdomen_date=None, usg_pelvis_abdomen_site_of_mass_id=None,
                 usg_pelvis_abdomen_size_of_mass=None, usg_pelvis_abdomen_extensions_id=None, chest_xray_date=None,
                 chest_xray_report_id=None, chest_xray_summary_id=None, pelvic_mri_date=None,
                 pelvic_mri_site_of_mass_id=None, pelvic_mri_size_of_mass=None, pelvic_mri_extensions_id=None,
                 blood_date=None, blood_fbc_id=None, blood_fbc=None, blood_lft_report_id=None,
                 blood_urea_creatinine_report_id=None, stage_figo_date=None, stage_figo_id=None, date_create=None,
                 user_create=None, date_modify=None, user_modify=None, stage_figo_i_id=None, stage_figo_ia_id=None,
                 stage_figo_ib_id=None, stage_figo_ii_id=None, stage_figo_iii_id=None, stage_figo_iv_id=None):
        self.id = id
        self.patient_id = patient_id
        self.departament = departament
        self.parity = parity
        self.residential_address = residential_address
        self.pmhx = pmhx
        self.presenting_complaint = presenting_complaint
        self.main_physical_clinical_findings = main_physical_clinical_findings
        self.performance_status_ecog_id = performance_status_ecog_id
        self.treatment_decision = treatment_decision
        self.colposcopy_date = colposcopy_date
        self.colposcopy_report_id = colposcopy_report_id
        self.cervical_biopsy_date = cervical_biopsy_date
        self.cervical_biopsy_histology = cervical_biopsy_histology
        self.cervical_biopsy_morphology = cervical_biopsy_morphology
        self.cervical_biopsy_grade = cervical_biopsy_grade
        self.usg_pelvis_abdomen_date = usg_pelvis_abdomen_date
        self.usg_pelvis_abdomen_site_of_mass_id = usg_pelvis_abdomen_site_of_mass_id
        self.usg_pelvis_abdomen_size_of_mass = usg_pelvis_abdomen_size_of_mass
        self.usg_pelvis_abdomen_extensions_id = usg_pelvis_abdomen_extensions_id
        self.chest_xray_date = chest_xray_date
        self.chest_xray_report_id = chest_xray_report_id
        self.chest_xray_summary_id = chest_xray_summary_id
        self.pelvic_mri_date = pelvic_mri_date
        self.pelvic_mri_site_of_mass_id = pelvic_mri_site_of_mass_id
        self.pelvic_mri_size_of_mass = pelvic_mri_size_of_mass
        self.pelvic_mri_extensions_id = pelvic_mri_extensions_id
        self.blood_date = blood_date
        self.blood_fbc_id = blood_fbc_id
        self.blood_fbc = blood_fbc
        self.blood_lft_report_id = blood_lft_report_id
        self.blood_urea_creatinine_report_id = blood_urea_creatinine_report_id
        self.stage_figo_date = stage_figo_date
        self.stage_figo_id = stage_figo_id
        self.stage_figo_i_id = stage_figo_i_id
        self.stage_figo_ia_id = stage_figo_ia_id
        self.stage_figo_ib_id = stage_figo_ib_id
        self.stage_figo_ii_id = stage_figo_ii_id
        self.stage_figo_iii_id = stage_figo_iii_id
        self.stage_figo_iv_id = stage_figo_iv_id
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'departament': self.departament,
            'parity': self.parity,
            'residential_address': self.residential_address,
            'pmhx': self.pmhx,
            'presenting_complaint': self.presenting_complaint,
            'main_physical_clinical_findings': self.main_physical_clinical_findings,
            'performance_status_ecog_id': self.performance_status_ecog_id,
            'treatment_decision': self.treatment_decision,
            'colposcopy_date': self.colposcopy_date.strftime("%d/%m/%Y") if self.colposcopy_date else None,
            'colposcopy_report_id': self.colposcopy_report_id,
            'cervical_biopsy_date': self.cervical_biopsy_date.strftime("%d/%m/%Y") if self.cervical_biopsy_date else None,
            'cervical_biopsy_histology': self.cervical_biopsy_histology,
            'cervical_biopsy_morphology': self.cervical_biopsy_morphology,
            'cervical_biopsy_grade': self.cervical_biopsy_grade,
            'usg_pelvis_abdomen_date': self.usg_pelvis_abdomen_date.strftime("%d/%m/%Y") if self.usg_pelvis_abdomen_date else None,
            'usg_pelvis_abdomen_site_of_mass_id': self.usg_pelvis_abdomen_site_of_mass_id,
            'usg_pelvis_abdomen_size_of_mass': self.usg_pelvis_abdomen_size_of_mass,
            'usg_pelvis_abdomen_extensions_id': self.usg_pelvis_abdomen_extensions_id,
            'chest_xray_date': self.chest_xray_date.strftime("%d/%m/%Y") if self.chest_xray_date else None,
            'chest_xray_report_id': self.chest_xray_report_id,
            'chest_xray_summary_id': self.chest_xray_summary_id,
            'pelvic_mri_date': self.pelvic_mri_date.strftime("%d/%m/%Y") if self.pelvic_mri_date else None,
            'pelvic_mri_site_of_mass_id': self.pelvic_mri_site_of_mass_id,
            'pelvic_mri_size_of_mass': self.pelvic_mri_size_of_mass,
            'pelvic_mri_extensions_id': self.pelvic_mri_extensions_id,
            'blood_date': self.blood_date.strftime("%d/%m/%Y") if self.blood_date else None,
            'blood_fbc_id': self.blood_fbc_id,
            'blood_fbc': self.blood_fbc,
            'blood_lft_report_id': self.blood_lft_report_id,
            'blood_urea_creatinine_report_id': self.blood_urea_creatinine_report_id,
            'stage_figo_date': self.stage_figo_date.strftime("%d/%m/%Y") if self.stage_figo_date else None,
            'stage_figo_id': self.stage_figo_id,
            'stage_figo_i_id': self.stage_figo_i_id,
            'stage_figo_ia_id': self.stage_figo_ia_id,
            'stage_figo_ib_id': self.stage_figo_ib_id,
            'stage_figo_ii_id': self.stage_figo_ii_id,
            'stage_figo_iii_id': self.stage_figo_iii_id,
            'stage_figo_iv_id': self.stage_figo_iv_id,
            'date_create': self.date_create,
            'user_create': self.user_create,
            'date_modify': self.date_modify,
            'user_modify': self.user_modify,
        }

        if jsondepth > 0:
            json['patient'] = self.patient.json(jsondepth - 1) if self.patient else None
            json['performance_status_ecog'] = self.performance_status_ecog.json(jsondepth - 1) if self.performance_status_ecog else None
            json['colposcopy_report'] = self.colposcopy_report.json(jsondepth - 1) if self.colposcopy_report else {}
            json['usg_pelvis_abdomen_site_of_mass'] = self.usg_pelvis_abdomen_site_of_mass.json(jsondepth - 1) if self.usg_pelvis_abdomen_site_of_mass else None
            json['usg_pelvis_abdomen_extensions'] = self.usg_pelvis_abdomen_extensions.json(jsondepth - 1) if self.usg_pelvis_abdomen_extensions else None
            json['chest_xray_report'] = self.chest_xray_report.json(jsondepth - 1) if self.chest_xray_report else {}
            json['chest_xray_summary'] = self.chest_xray_summary.json(jsondepth - 1) if self.chest_xray_summary else None
            json['pelvic_mri_site_of_mass'] = self.pelvic_mri_site_of_mass.json(jsondepth - 1) if self.pelvic_mri_site_of_mass else None
            json['pelvic_mri_extensions'] = self.pelvic_mri_extensions.json(jsondepth - 1) if self.pelvic_mri_extensions else None
            json['_blood_fbc'] = self._blood_fbc.json(jsondepth - 1) if self._blood_fbc else None
            json['blood_lft_report'] = self.blood_lft_report.json(jsondepth - 1) if self.blood_lft_report else {}
            json['blood_urea_creatinine_report'] = self.blood_urea_creatinine_report.json(jsondepth - 1) if self.blood_urea_creatinine_report else {}
            json['stage_figo'] = self.stage_figo.json(jsondepth - 1) if self.stage_figo else None
            json['stage_figo_i'] = self.stage_figo_i.json(jsondepth - 1) if self.stage_figo_i else None
            json['stage_figo_ia'] = self.stage_figo_ia.json(jsondepth - 1) if self.stage_figo_ia else None
            json['stage_figo_ib'] = self.stage_figo_ib.json(jsondepth - 1) if self.stage_figo_ib else None
            json['stage_figo_ii'] = self.stage_figo_ii.json(jsondepth - 1) if self.stage_figo_ii else None
            json['stage_figo_iii'] = self.stage_figo_iii.json(jsondepth - 1) if self.stage_figo_iii else None
            json['stage_figo_iv'] = self.stage_figo_iv.json(jsondepth - 1) if self.stage_figo_iv else None

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

