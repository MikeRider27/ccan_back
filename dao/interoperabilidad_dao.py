from yml_main import YmlMain


class InteroperabilidadDao:
    yml_path = 'dao/yml/interoperabilidad.yml'

    def patient_data(self, patient_document):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_document': patient_document
        }
        result = yml.get_result(key='interoperabilidad.patient.biopsia', params=params, as_dict=True,
                                datasource='interoperabilidad')
        return result

    def hospital_map(self):
        yml = YmlMain(yml_path=self.yml_path)
        return yml.get_key_data(key='map_interoerabilidad_ccan.hospital')

    def get_medicine_history_siciap_header(self, codigo_medicamento):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'codigo_medicamento': codigo_medicamento
        }
        results = yml.get_result(key='interoperabilidad.inventario.siciap_mov_origen_lote', params=params, as_dict=True,
                                 datasource='interoperabilidad')
        return results

    def get_medicine_history_siciap(self, codigo_medicamento):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'codigo_medicamento': codigo_medicamento
        }
        results = yml.get_result(key='interoperabilidad.inventario.siciap_mov', params=params, as_dict=True,
                                 datasource='interoperabilidad')
        return results

    def get_medicine_history_ccan_header(self, codigo_medicamento):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'codigo_medicamento': codigo_medicamento
        }
        results = yml.get_result(key='interoperabilidad.inventario.ccan_mov_origen_lote', params=params, as_dict=True)
        return results

    def get_medicine_history_ccan(self, codigo_medicamento):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'codigo_medicamento': codigo_medicamento
        }
        results = yml.get_result(key='interoperabilidad.inventario.ccan_mov', params=params, as_dict=True)
        return results

    def get_patients_sigap(self):
        yml = YmlMain(yml_path=self.yml_path)
        results = yml.get_result(key='interoperabilidad.patient.sigap', as_dict=True, datasource='interoperabilidad')
        return results

    def get_patient_consultation_his(self, patient_document, patient_registration_date):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_document': patient_document,
            'patient_registration_date': patient_registration_date
        }
        results = yml.get_result(key='interoperabilidad.consultation.his', params=params, as_dict=True,
                                 datasource='interoperabilidad')
        return results

    def get_patient_dispatch_medications(self, medicine_code, patient_document, patient_registration_date):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'medicine_code': medicine_code,
            'patient_document': patient_document,
            'patient_registration_date': patient_registration_date
        }
        results = yml.get_result(key='interoperabilidad.inventario.dispatch_medication', params=params, as_dict=True,
                                 datasource='interoperabilidad')
        return results

    def get_patient_dispatch_medications_history(self, patient_document, patient_registration_date):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_document': patient_document,
            'patient_registration_date': patient_registration_date
        }
        results = yml.get_result(key='interoperabilidad.inventario.dispatch_medication_history', params=params,
                                 as_dict=True, datasource='interoperabilidad')
        return results
