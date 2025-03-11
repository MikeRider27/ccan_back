import sys

from flask import current_app, request

from yml_main import YmlMain


class PatientDao:
    yml_path = 'dao/yml/patient.yml'

    def get_patient_paginated(self, filters: dict = None):
        yml = YmlMain(yml_path=self.yml_path)

        # Parametros
        cipher_key = current_app.config['ENCRYPTION_KEY']
        params = {
            'cipher_key': cipher_key
        }

        # Filters
        if not filters:
            filters = {}

        query_filter = ''
        if filters:
            filter_list = []
            strict_filter = []
            for clave, valor in filters.items():
                # Ignorar si la clave del filtro no tiene valor
                if not valor:
                    continue

                # OR or AND filters
                if clave == 'registration_date':
                    filter_list.append(f"TO_CHAR(patient.{clave}, 'DD/MM/YYYY') ilike '%{valor}%'")
                if clave == 'state':
                    filter_list.append(f"{clave}.value ilike '%{valor}%'")
                if clave == 'document_type':
                    filter_list.append(f"{clave}.description ilike '%{valor}%'")
                if clave == 'document_number':
                    filter_list.append(f"decrypt_data(patient.{clave}, '{cipher_key}') ilike '%{valor}%'")
                if clave == 'firstname':
                    filter_list.append(f"decrypt_data(patient.{clave}, '{cipher_key}') ilike '%{valor}%'")
                if clave == 'lastname':
                    filter_list.append(f"decrypt_data(patient.{clave}, '{cipher_key}') ilike '%{valor}%'")
                if clave == 'gender':
                    filter_list.append(f"{clave}.description ilike '%{valor}%'")
                if clave == 'origins':
                    filter_list.append(
                        f"(LOWER(patient.origin) ILIKE LOWER('%{valor}%') "
                        f"OR LOWER(dispatch_medications.origin) ILIKE LOWER('%{valor}%') "
                        f"OR LOWER(medical_consultation.origin) ILIKE LOWER('%{valor}%'))"
                    )
                    # filter_list.append(f"patient.origin ilike '%{valor}%'")

                # Only AND filters
                if clave == 'hospital_id':
                    strict_filter.append(f"patient_hospital.{clave} = {valor}")

            # No strict filter resolution
            general_filter = request.args.get('general_filter', None, str) == 'true'

            if general_filter:
                no_strict_query_filter = '\nOR '.join(filter_list)
            else:
                no_strict_query_filter = '\nAND '.join(filter_list)

            # Strict filter resolution
            strict_query_filter = ''
            if len(strict_filter) > 0:
                strict_query_filter = '\nAND '.join(strict_filter)

            if no_strict_query_filter and strict_query_filter:
                query_filter = f"{no_strict_query_filter} AND {strict_query_filter}"
            else:
                query_filter = no_strict_query_filter if no_strict_query_filter else strict_query_filter

        # Conversion de claves de ordenamiento
        sort_conv = {
            'registration_date': 'patient.registration_date'
        }

        results = yml.get_list(query_key='patient.query', params=params, query_filter=query_filter, sort_conv=sort_conv)
        # New origins
        if 'items' in results:
            for patient in results['items']:
                patient['origin'] = self.get_origins(patient['id'], patient['origins'])

        return results

    def get_origins(self, patient_id, patient_origin):
        from models.dispatch_medications import DispatchMedicationsModel
        from models.medical_consultation import MedicalConsultationModel

        dispatch_medicaments_origin = DispatchMedicationsModel.query.filter_by(patient_id=patient_id, origin='SICIAP').first()
        medical_consultation_origin = MedicalConsultationModel.query.filter_by(patient_id=patient_id, origin ='HIS').first()

        origins = set()
        if patient_origin:
            origins.add(patient_origin)

        if dispatch_medicaments_origin:
            origins.add(dispatch_medicaments_origin.origin)
        if medical_consultation_origin:
            origins.add(medical_consultation_origin.origin)
        return list(origins) if origins else None

    def patient_sumarize(self, patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        cipher_key = current_app.config['ENCRYPTION_KEY']
        params = {
            'patient_id': patient_id,
            'cipher_key': cipher_key
        }
        row = yml.get_single_result(key='patient.summarize', params=params, as_dict=True)
        return row

    def get_patient_origins(self, patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        rows = yml.get_result(key='patient.origin', params=params)
        return rows

    def get_patients_document(self):
        yml = YmlMain(yml_path=self.yml_path)
        cipher_key = current_app.config['ENCRYPTION_KEY']
        params = {
            'cipher_key': cipher_key
        }
        rows = yml.get_result(key='patient.patients_document', params=params, as_dict=True)
        return rows


    def get_patients_all(self):
        yml = YmlMain(yml_path=self.yml_path)
        cipher_key = current_app.config['ENCRYPTION_KEY']
        params = {
            'cipher_key': cipher_key
        }
        rows = yml.get_result(key='patient.patients_all', params=params, as_dict=True)
        return rows
