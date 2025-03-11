from yml_main import YmlMain


class TreatmentPlanDao:
    yml_path = 'dao/yml/treatment_plan.yml'

    def get_number(self, patient_id):
        yml = YmlMain(yml_path=self.yml_path)
        params = {
            'patient_id': patient_id
        }
        row = yml.get_single_result(key='treatment_plan.next_number', params=params, as_dict=True)
        return row
