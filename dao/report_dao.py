from flask import current_app

from yml_main import YmlMain


class ReportDao:
    yml_path = 'dao/yml/report.yml'

    def indicator_1(self):
        yml = YmlMain(yml_path=self.yml_path)
        cipher_key = current_app.config['ENCRYPTION_KEY']
        params = {
            'cipher_key': cipher_key
        }
        rows = yml.get_result(key='report.indicador_1', params=params)
        return rows

    def indicator_2_medications_used(self):
        yml = YmlMain(yml_path=self.yml_path)
        params = {}
        rows = yml.get_result(key='report.indicador_2.report_medications_used', params=params)
        return rows

    def donation_medications(self):
        yml = YmlMain(yml_path=self.yml_path)
        params = {}
        rows = yml.get_result(key='report.donation_medications', params=params)
        return rows

    def patient_personal_data(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        cipher_key = current_app.config['ENCRYPTION_KEY']
        params = {
            'patient_id': patient_id,
            'cipher_key': cipher_key
        }
        rows = yml.get_result(key='report.patient.personal_data', params=params)
        return rows

    def patient_diagnosis(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.diagnosis', params=params)
        return rows

    def patient_pathological_history(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.pathological_history', params=params)
        return rows

    def patient_medical_consultation(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.medical_consultation', params=params)
        return rows

    def patient_diagnosis_ap(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.diagnosis_ap', params=params)
        return rows

    def patient_treatment_plan(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.treatment_plan', params=params)
        return rows

    def patient_follow_up(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.follow_up', params=params)
        return rows

    def patient_chemotherapy(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.chemotherapy', params=params)
        return rows

    def patient_radiotherapy(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.radiotherapy', params=params)
        return rows

    def patient_surgery(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.surgery', params=params)
        return rows

    def patient_committee(self,patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='report.patient.committee', params=params)
        return rows