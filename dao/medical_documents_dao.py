from yml_main import YmlMain


class MedicalDocumentsDao:
    yml_path = 'dao/yml/medical_documents.yml'

    def get_requirements_files_data(self, patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        results = yml.get_result(key='medical_documents.requirements_list', params=params, as_dict=True)
        return results
