import base64
import datetime

from flask_restful.reqparse import Namespace

from db import db, BaseModel
from models.medical_document import MedicalDocumentModel
from models.parameter import ParameterModel
from models.patient import PatientModel


class BreastFormModel(BaseModel):
    __tablename__ = 'breast_form'

    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(PatientModel.id))
    departament = db.Column(db.String)
    residential_address = db.Column(db.String)
    parity = db.Column(db.Boolean)
    pmhx = db.Column(db.String)
    presenting_complaint = db.Column(db.String)
    main_physical_clinical_findings = db.Column(db.String)
    performance_status_ecog_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    treatment_decision = db.Column(db.String)
    mammogram_date = db.Column(db.DateTime)
    mammogram_birads_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    mammogram_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    usg_breast_date = db.Column(db.DateTime)
    usg_breast_birads_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    usg_breast_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    fnac_date = db.Column(db.DateTime)
    fnac_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    fnac_summary = db.Column(db.String)
    trucut_date = db.Column(db.DateTime)
    trucut_histology_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    trucut_morphology_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    trucut_others = db.Column(db.String)
    trucut_grade = db.Column(db.String)
    trucut_hormone_receptor_status_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    trucut_her2_neu_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    other_biopsy_date = db.Column(db.DateTime)
    other_biopsy_histology_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    other_biopsy_morphology_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    other_biopsy_others = db.Column(db.String)
    other_biopsy_grade = db.Column(db.String)
    other_biopsy_hormone_receptor_status_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    other_biopsy_her2_neu_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    chest_xray_date = db.Column(db.DateTime)
    chest_xray_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    chest_xray_summary_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    chest_ct_date = db.Column(db.DateTime)
    chest_ct_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    chest_ct_summary_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    usg_liver_date = db.Column(db.DateTime)
    usg_liver_summary_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    blood_date = db.Column(db.DateTime)
    blood_fbc_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    blood_fbc = db.Column(db.String)
    blood_fbc_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    blood_lft_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    blood_urea_creatinine_report_id = db.Column(db.BigInteger, db.ForeignKey(MedicalDocumentModel.id))
    bone_scan_date = db.Column(db.DateTime)
    bone_scan_summary = db.Column(db.String)
    stage_breast_location_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    stage_breast_date = db.Column(db.DateTime)
    stage_breast_t_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    stage_breast_n_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    stage_breast_m_id = db.Column(db.BigInteger, db.ForeignKey(ParameterModel.id))
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_create = db.Column(db.String(30))
    date_modify = db.Column(db.DateTime)
    user_modify = db.Column(db.String(30))

    # Relationship
    patient = db.relationship('PatientModel', foreign_keys=[patient_id], uselist=False)
    performance_status_ecog = db.relationship('ParameterModel', foreign_keys=[performance_status_ecog_id], uselist=False)
    mammogram_birads = db.relationship('ParameterModel', foreign_keys=[mammogram_birads_id], uselist=False)
    mammogram_report = db.relationship('MedicalDocumentModel', foreign_keys=[mammogram_report_id], uselist=False)
    usg_breast_birads = db.relationship('ParameterModel', foreign_keys=[usg_breast_birads_id], uselist=False)
    usg_breast_report = db.relationship('MedicalDocumentModel', foreign_keys=[usg_breast_report_id], uselist=False)
    fnac_report = db.relationship('MedicalDocumentModel', foreign_keys=[fnac_report_id], uselist=False)
    trucut_histology_report = db.relationship('MedicalDocumentModel', foreign_keys=[trucut_histology_report_id], uselist=False)
    trucut_morphology = db.relationship('ParameterModel', foreign_keys=[trucut_morphology_id], uselist=False)
    trucut_her2_neu = db.relationship('ParameterModel', foreign_keys=[trucut_her2_neu_id], uselist=False)
    other_biopsy_histology_report = db.relationship('MedicalDocumentModel', foreign_keys=[other_biopsy_histology_report_id], uselist=False)
    other_biopsy_morphology = db.relationship('ParameterModel', foreign_keys=[other_biopsy_morphology_id], uselist=False)
    other_biopsy_hormone_receptor_status = db.relationship('ParameterModel', foreign_keys=[other_biopsy_hormone_receptor_status_id], uselist=False)
    other_biopsy_her2_neu = db.relationship('ParameterModel', foreign_keys=[other_biopsy_her2_neu_id], uselist=False)
    chest_xray_report = db.relationship('MedicalDocumentModel', foreign_keys=[chest_xray_report_id], uselist=False)
    chest_xray_summary = db.relationship('ParameterModel', foreign_keys=[chest_xray_summary_id], uselist=False)
    chest_ct_report = db.relationship('MedicalDocumentModel', foreign_keys=[chest_ct_report_id], uselist=False)
    chest_ct_summary = db.relationship('ParameterModel', foreign_keys=[chest_ct_summary_id], uselist=False)
    usg_liver_summary = db.relationship('ParameterModel', foreign_keys=[usg_liver_summary_id], uselist=False)
    _blood_fbc = db.relationship('ParameterModel', foreign_keys=[blood_fbc_id], uselist=False)
    blood_fbc_report = db.relationship('MedicalDocumentModel', foreign_keys=[blood_fbc_report_id], uselist=False)
    blood_lft_report = db.relationship('MedicalDocumentModel', foreign_keys=[blood_lft_report_id], uselist=False)
    blood_urea_creatinine_report = db.relationship('MedicalDocumentModel', foreign_keys=[blood_urea_creatinine_report_id], uselist=False)
    stage_breast_location = db.relationship('ParameterModel', foreign_keys=[stage_breast_location_id], uselist=False)
    stage_breast_t = db.relationship('ParameterModel', foreign_keys=[stage_breast_t_id], uselist=False)
    stage_breast_n = db.relationship('ParameterModel', foreign_keys=[stage_breast_n_id], uselist=False)
    stage_breast_m = db.relationship('ParameterModel', foreign_keys=[stage_breast_m_id], uselist=False)


    def __init__(self, id=None, patient_id=None, departament=None, residential_address=None, parity=None, pmhx=None,
                 presenting_complaint=None, main_physical_clinical_findings=None, performance_status_ecog_id=None,
                 treatment_decision=None, mammogram_date=None, mammogram_birads_id=None, mammogram_report_id=None,
                 usg_breast_date=None, usg_breast_birads_id=None, usg_breast_report_id=None, fnac_date=None,
                 fnac_report_id=None, fnac_summary=None, trucut_date=None, trucut_histology_report_id=None,
                 trucut_morphology_id=None, trucut_others=None, trucut_grade=None,
                 trucut_hormone_receptor_status_id=None, trucut_her2_neu_id=None, other_biopsy_date=None,
                 other_biopsy_histology_report_id=None, other_biopsy_morphology_id=None, other_biopsy_others=None,
                 other_biopsy_grade=None, other_biopsy_hormone_receptor_status_id=None, other_biopsy_her2_neu_id=None,
                 chest_xray_date=None, chest_xray_report_id=None, chest_xray_summary_id=None, chest_ct_date=None,
                 chest_ct_report_id=None, chest_ct_summary_id=None, usg_liver_date=None, usg_liver_summary_id=None,
                 blood_date=None, blood_fbc_id=None, blood_fbc=None, blood_fbc_report_id=None, blood_lft_report_id=None,
                 blood_urea_creatinine_report_id=None, bone_scan_date=None, bone_scan_summary=None, date_create=None,
                 user_create=None, date_modify=None, user_modify=None, stage_breast_location_id=None,
                 stage_breast_date=None, stage_breast_t_id=None, stage_breast_n_id=None, stage_breast_m_id=None):
        self.id = id
        self.patient_id = patient_id
        self.departament = departament
        self.residential_address = residential_address
        self.parity = parity
        self.pmhx = pmhx
        self.presenting_complaint = presenting_complaint
        self.main_physical_clinical_findings = main_physical_clinical_findings
        self.performance_status_ecog_id = performance_status_ecog_id
        self.treatment_decision = treatment_decision
        self.mammogram_date = mammogram_date
        self.mammogram_birads_id = mammogram_birads_id
        self.mammogram_report_id = mammogram_report_id
        self.usg_breast_date = usg_breast_date
        self.usg_breast_birads_id = usg_breast_birads_id
        self.usg_breast_report_id = usg_breast_report_id
        self.fnac_date = fnac_date
        self.fnac_report_id = fnac_report_id
        self.fnac_summary = fnac_summary
        self.trucut_date = trucut_date
        self.trucut_histology_report_id = trucut_histology_report_id
        self.trucut_morphology_id = trucut_morphology_id
        self.trucut_others = trucut_others
        self.trucut_grade = trucut_grade
        self.trucut_hormone_receptor_status_id = trucut_hormone_receptor_status_id
        self.trucut_her2_neu_id = trucut_her2_neu_id
        self.other_biopsy_date = other_biopsy_date
        self.other_biopsy_histology_report_id = other_biopsy_histology_report_id
        self.other_biopsy_morphology_id = other_biopsy_morphology_id
        self.other_biopsy_others = other_biopsy_others
        self.other_biopsy_grade = other_biopsy_grade
        self.other_biopsy_hormone_receptor_status_id = other_biopsy_hormone_receptor_status_id
        self.other_biopsy_her2_neu_id = other_biopsy_her2_neu_id
        self.chest_xray_date = chest_xray_date
        self.chest_xray_report_id = chest_xray_report_id
        self.chest_xray_summary_id = chest_xray_summary_id
        self.chest_ct_date = chest_ct_date
        self.chest_ct_report_id = chest_ct_report_id
        self.chest_ct_summary_id = chest_ct_summary_id
        self.usg_liver_date = usg_liver_date
        self.usg_liver_summary_id = usg_liver_summary_id
        self.blood_date = blood_date
        self.blood_fbc_id = blood_fbc_id
        self.blood_fbc = blood_fbc
        self.blood_fbc_report_id = blood_fbc_report_id
        self.blood_lft_report_id = blood_lft_report_id
        self.blood_urea_creatinine_report_id = blood_urea_creatinine_report_id
        self.bone_scan_date = bone_scan_date
        self.bone_scan_summary = bone_scan_summary
        self.date_create = date_create
        self.user_create = user_create
        self.date_modify = date_modify
        self.user_modify = user_modify
        self.stage_breast_location_id = stage_breast_location_id
        self.stage_breast_date = stage_breast_date
        self.stage_breast_t_id = stage_breast_t_id
        self.stage_breast_n_id = stage_breast_n_id
        self.stage_breast_m_id = stage_breast_m_id

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'patient_id': self.patient_id,
            'departament': self.departament,
            'residential_address': self.residential_address,
            'parity': self.parity,
            'pmhx': self.pmhx,
            'presenting_complaint': self.presenting_complaint,
            'main_physical_clinical_findings': self.main_physical_clinical_findings,
            'performance_status_ecog_id': self.performance_status_ecog_id,
            'treatment_decision': self.treatment_decision,
            'mammogram_date': self.mammogram_date.strftime("%d/%m/%Y") if self.mammogram_date else None,
            'mammogram_birads_id': self.mammogram_birads_id,
            'mammogram_report_id': self.mammogram_report_id,
            'usg_breast_date': self.usg_breast_date.strftime("%d/%m/%Y") if self.usg_breast_date else None,
            'usg_breast_birads_id': self.usg_breast_birads_id,
            'usg_breast_report_id': self.usg_breast_report_id,
            'fnac_date': self.fnac_date.strftime("%d/%m/%Y") if self.fnac_date else None,
            'fnac_report_id': self.fnac_report_id,
            'fnac_summary': self.fnac_summary,
            'trucut_date': self.trucut_date.strftime("%d/%m/%Y") if self.trucut_date else None,
            'trucut_histology_report_id': self.trucut_histology_report_id,
            'trucut_morphology_id': self.trucut_morphology_id,
            'trucut_others': self.trucut_others,
            'trucut_grade': self.trucut_grade,
            'trucut_hormone_receptor_status_id': self.trucut_hormone_receptor_status_id,
            'trucut_her2_neu_id': self.trucut_her2_neu_id,
            'other_biopsy_date': self.other_biopsy_date.strftime("%d/%m/%Y") if self.other_biopsy_date else None,
            'other_biopsy_histology_report_id': self.other_biopsy_histology_report_id,
            'other_biopsy_morphology_id': self.other_biopsy_morphology_id,
            'other_biopsy_others': self.other_biopsy_others,
            'other_biopsy_grade': self.other_biopsy_grade,
            'other_biopsy_hormone_receptor_status_id': self.other_biopsy_hormone_receptor_status_id,
            'other_biopsy_her2_neu_id': self.other_biopsy_her2_neu_id,
            'chest_xray_date': self.chest_xray_date.strftime("%d/%m/%Y") if self.chest_xray_date else None,
            'chest_xray_report_id': self.chest_xray_report_id,
            'chest_xray_summary_id': self.chest_xray_summary_id,
            'chest_ct_date': self.chest_ct_date.strftime("%d/%m/%Y") if self.chest_ct_date else None,
            'chest_ct_report_id': self.chest_ct_report_id,
            'chest_ct_summary_id': self.chest_ct_summary_id,
            'usg_liver_date': self.usg_liver_date.strftime("%d/%m/%Y") if self.usg_liver_date else None,
            'usg_liver_summary_id': self.usg_liver_summary_id,
            'blood_date': self.blood_date.strftime("%d/%m/%Y") if self.blood_date else None,
            'blood_fbc_id': self.blood_fbc_id,
            'blood_fbc': self.blood_fbc,
            'blood_fbc_report_id': self.blood_fbc_report_id,
            'blood_lft_report_id': self.blood_lft_report_id,
            'blood_urea_creatinine_report_id': self.blood_urea_creatinine_report_id,
            'bone_scan_date': self.bone_scan_date.strftime("%d/%m/%Y") if self.bone_scan_date else None,
            'bone_scan_summary': self.bone_scan_summary,
            'date_create': self.date_create,
            'user_create': self.user_create,
            'date_modify': self.date_modify,
            'user_modify': self.user_modify,
            'stage_breast_location_id': self.stage_breast_location_id,
            'stage_breast_date': self.stage_breast_date.strftime("%d/%m/%Y") if self.stage_breast_date else None,
            'stage_breast_t_id': self.stage_breast_t_id,
            'stage_breast_n_id': self.stage_breast_n_id,
            'stage_breast_m_id': self.stage_breast_m_id,
        }

        if jsondepth > 0:
            json['patient'] = self.patient.json(jsondepth - 1) if self.patient else None
            json['performance_status_ecog'] = self.performance_status_ecog.json(jsondepth - 1) if self.performance_status_ecog else None
            json['mammogram_birads'] = self.mammogram_birads.json(jsondepth - 1) if self.mammogram_birads else None
            json['mammogram_report'] = self.mammogram_report.json(jsondepth - 1) if self.mammogram_report else {}
            json['usg_breast_birads'] = self.usg_breast_birads.json(jsondepth - 1) if self.usg_breast_birads else None
            json['usg_breast_report'] = self.usg_breast_report.json(jsondepth - 1) if self.usg_breast_report else {}
            json['fnac_report'] = self.fnac_report.json(jsondepth - 1) if self.fnac_report else {}
            json['trucut_histology_report'] = self.trucut_histology_report.json(jsondepth - 1) if self.trucut_histology_report else {}
            json['trucut_morphology'] = self.trucut_morphology.json(jsondepth - 1) if self.trucut_morphology else None
            json['trucut_her2_neu'] = self.trucut_her2_neu.json(jsondepth - 1) if self.trucut_her2_neu else None
            json['other_biopsy_histology_report'] = self.other_biopsy_histology_report.json(jsondepth - 1) if self.other_biopsy_histology_report else {}
            json['other_biopsy_morphology'] = self.other_biopsy_morphology.json(jsondepth - 1) if self.other_biopsy_morphology else None
            json['other_biopsy_hormone_receptor_status'] = self.other_biopsy_hormone_receptor_status.json(jsondepth - 1) if self.other_biopsy_hormone_receptor_status else None
            json['other_biopsy_her2_neu'] = self.other_biopsy_her2_neu.json(jsondepth - 1) if self.other_biopsy_her2_neu else None
            json['chest_xray_report'] = self.chest_xray_report.json(jsondepth - 1) if self.chest_xray_report else {}
            json['chest_xray_summary'] = self.chest_xray_summary.json(jsondepth - 1) if self.chest_xray_summary else None
            json['chest_ct_report'] = self.chest_ct_report.json(jsondepth - 1) if self.chest_ct_report else {}
            json['chest_ct_summary'] = self.chest_ct_summary.json(jsondepth - 1) if self.chest_ct_summary else None
            json['usg_liver_summary'] = self.usg_liver_summary.json(jsondepth - 1) if self.usg_liver_summary else None
            json['_blood_fbc'] = self._blood_fbc.json(jsondepth - 1) if self._blood_fbc else None
            json['blood_fbc_report'] = self.blood_fbc_report.json(jsondepth - 1) if self.blood_fbc_report else {}
            json['blood_lft_report'] = self.blood_lft_report.json(jsondepth - 1) if self.blood_lft_report else {}
            json['blood_urea_creatinine_report'] = self.blood_urea_creatinine_report.json(jsondepth - 1) if self.blood_urea_creatinine_report else {}
            json['stage_breast_location'] = self.stage_breast_location.json(jsondepth - 1) if self.stage_breast_location else None
            json['stage_breast_t'] = self.stage_breast_t.json(jsondepth - 1) if self.stage_breast_t else None
            json['stage_breast_n'] = self.stage_breast_n.json(jsondepth - 1) if self.stage_breast_n else None
            json['stage_breast_m'] = self.stage_breast_m.json(jsondepth - 1) if self.stage_breast_m else None

        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

