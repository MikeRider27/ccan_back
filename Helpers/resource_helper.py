from datetime import datetime

from flask_babel import _
from flask_jwt_extended import get_jwt
from flask_restful import Resource

from models.cie_o_morphology import CieOMorphologyModel
from models.cie_o_topography import CieOTopographyModel
from models.diagnosis import DiagnosisModel
from models.drug import DrugModel
from models.medicine import MedicineModel
from models.parameter import ParameterModel
from models.patient import PatientModel
from models.product import ProductModel
from models.specialty import SpecialtyModel
from models.treatment_scheme import TreatmentSchemeModel


class ResourceHelper(Resource):

    @staticmethod
    def trim_string(value):
        if not isinstance(value, str):
            raise ValueError(_("EXPECTED_STRING").format(value))
        return value.strip()

    @staticmethod
    def validate_text_15(code):
        if code:
            code = code.strip()
            if len(code) > 15:
                raise ValueError(_("ERROR_TEXT_TOO_LONG").format(length=15))
        return code


    @staticmethod
    def validate_text_255(value):
        if value:
            value = value.strip()
            if len(value) > 255:
                raise ValueError(_("ERROR_TEXT_TOO_LONG").format(length=255))

        return value


    @staticmethod
    def validate_drug_category(category_id):
        parameter = ParameterModel.find_by_id(category_id) if category_id else None
        if not parameter or parameter.domain != 'DRUG_CATEGORY':
            raise ValueError(_("INVALID_CATEGORY"))

        return category_id


    @staticmethod
    def validate_medicine(medicine_id):
        model = MedicineModel.find_by_id(medicine_id) if medicine_id else None
        if not model:
            raise ValueError(_("RECORD_NOT_FOUND"))

        return medicine_id


    @staticmethod
    def validate_drug_uuid(drug_uuid):
        drug = DrugModel.get_by_uuid(drug_uuid) if drug_uuid else None
        if not drug:
            raise ValueError(_("RECORD_NOT_FOUND"))

        return drug.id


    @staticmethod
    def validate_product_uuid(uuid):
        identity = get_jwt()
        hospital_id = identity.get('hospital_id', 0)
        product = ProductModel.get_by_uuid(uuid) if uuid else None
        if not product or product.hospital_id != hospital_id:
            raise ValueError(_("RECORD_NOT_FOUND"))

        return product.id


    @staticmethod
    def validate_concentration_unit(concentration_unit_id):
        parameter = ParameterModel.find_by_id(concentration_unit_id) if concentration_unit_id else None
        if not parameter or parameter.domain != 'PRODUCT_UNIT_CONCENTRATION':
            raise ValueError(_("INVALID_CONCENTRATION"))

        return concentration_unit_id


    @staticmethod
    def validate_quantity_unit(quantity_unit_id):
        parameter = ParameterModel.find_by_id(quantity_unit_id) if quantity_unit_id else None
        if not parameter or parameter.domain != 'PRODUCT_UNIT_QUANTITY':
            raise ValueError(_("INVALID_QUANTITY"))

        return quantity_unit_id


    @staticmethod
    def validate_dose_unit(dose_unit_id):
        parameter = ParameterModel.find_by_id(dose_unit_id) if dose_unit_id else None
        if not parameter or parameter.domain != 'PRODUCT_UNIT_DOSE':
            raise ValueError(_("INVALID_UNIT"))

        return dose_unit_id


    @staticmethod
    def validate_product_type(type_id):
        parameter = ParameterModel.find_by_id(type_id) if type_id else None
        if not parameter or parameter.domain != 'PRODUCT_TYPE':
            raise ValueError(_("INVALID_TYPE"))

        return type_id


    @staticmethod
    def validate_scheme_periodicity(type_id):
        parameter = ParameterModel.find_by_id(type_id) if type_id else None
        if not parameter or parameter.domain != 'SCHEME_PERIODICITY':
            raise ValueError(_("INVALID_TYPE"))

        return type_id


    @staticmethod
    def validate_scheme_category(catyegory_id):
        parameter = ParameterModel.find_by_id(catyegory_id) if catyegory_id else None
        if not parameter or parameter.domain != 'SCHEME_CATEGORY':
            raise ValueError(_("INVALID_TYPE"))

        return catyegory_id


    @staticmethod
    def validate_administration_route(route_id):
        parameter = ParameterModel.find_by_id(route_id) if route_id else None
        if not parameter or parameter.domain != 'PRODUCT_ADMINISTRATION_ROUTE':
            raise ValueError(_("INVALID_TYPE"))

        return route_id


    @staticmethod
    def validate_calculation_type(type_id):
        parameter = ParameterModel.find_by_id(type_id) if type_id else None
        if not parameter or parameter.domain != 'PRODUCT_CALCULATION_TYPE':
            raise ValueError(_("INVALID_TYPE"))

        return type_id


    @staticmethod
    def validate_frequency(type_id):
        parameter = ParameterModel.find_by_id(type_id) if type_id else None
        if not parameter or parameter.domain != 'PRODUCT_FREQUENCY':
            raise ValueError(_("INVALID_TYPE"))

        return type_id


    @staticmethod
    def validate_protocol(type_id):
        parameter = ParameterModel.find_by_id(type_id) if type_id else None
        if not parameter or parameter.domain != 'PROTOCOL_TYPE':
            raise ValueError(_("INVALID_TYPE"))

        return type_id


    @staticmethod
    def validate_specialty(type_id):
        specialty = SpecialtyModel.find_by_id(type_id) if type_id else None
        if not specialty:
            raise ValueError(_("RECORD_NOT_FOUND"))

        return type_id


    @staticmethod
    def validate_diagnosis(type_id):
        diagnosis = DiagnosisModel.find_by_id(type_id) if type_id else None
        if not diagnosis:
            raise ValueError(_("RECORD_NOT_FOUND"))

        return type_id


    @staticmethod
    def validate_topography(type_id):
        model = CieOTopographyModel.find_by_id(type_id) if type_id else None
        if not model:
            raise ValueError(_("RECORD_NOT_FOUND"))

        return type_id


    @staticmethod
    def validate_morphology(type_id):
        model = CieOMorphologyModel.find_by_id(type_id) if type_id else None
        if not model:
            raise ValueError(_("RECORD_NOT_FOUND"))

        return type_id


    @staticmethod
    def validate_cancer_stage(type_id):
        parameter = ParameterModel.find_by_id(type_id) if type_id else None
        if not parameter or parameter.domain != 'CANCER_STAGE':
            raise ValueError(_("INVALID_TYPE"))

        return type_id


    @staticmethod
    def validate_request_criteria(type_id):
        parameter = ParameterModel.find_by_id(type_id) if type_id else None
        if not parameter or parameter.domain != 'SCHEME_REQUEST_CRITERIA':
            raise ValueError(_("INVALID_TYPE"))

        return type_id


    @staticmethod
    def validate_date(date):
        if date:
            try:
                datetime.strptime(date, '%Y-%m-%d')
                return date

            except ValueError:
                raise ValueError(f"Invalid date format: {date}. Expected format: %Y-%m-%d")


    @staticmethod
    def validate_patient(patient_id):
        patient = PatientModel.find_by_id(patient_id) if patient_id else None
        if not patient :
            raise ValueError(_("RECORD_NOT_FOUND"))

        return patient.id


    @staticmethod
    def validate_treatment_scheme(uuid):
        identity = get_jwt()
        hospital_id = identity.get('hospital_id', 0)
        treatment_scheme = TreatmentSchemeModel.get_by_uuid(uuid) if uuid else None
        if not treatment_scheme or treatment_scheme.hospital_id != hospital_id:
            raise ValueError(_("RECORD_NOT_FOUND"))

        return treatment_scheme.id
