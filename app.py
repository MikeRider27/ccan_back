from models.hospital import HospitalModel
from resources.deposit_lot import DepositLot, DepositLotList, DepositLotSearch, DepositLotQuantitySearch
from resources.drug import DrugResource, DrugListResource, DrugSearchResource
from resources.product import ProductResource, ProductListResource, ProductSearchResource
from resources.module import Module, ModuleList, ModuleSearch
from resources.module_role import ModuleRole, ModuleRoleList, ModuleRoleSearch
from resources.module_permission import ModulePermission, ModulePermissionList, ModulePermissionSearch
import datetime
import logging
import os
from datetime import timedelta
from logging.handlers import TimedRotatingFileHandler

from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request, redirect
from flask_babel import Babel, _
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt,
    verify_jwt_in_request
)
from flask_restful import Api

from db import db
from models.user import UserModel
from models.user_role import UserRoleModel
from resources.area import Area, AreaList, AreaSearch
from resources.breast_form import BreastForm, BreastFormList, BreastFormSearch
from resources.cervix_form import CervixForm, CervixFormList, CervixFormSearch, CervixBreastHeaderForm
from resources.chemotherapy import Chemotherapy, ChemotherapyList, ChemotherapySearch
from resources.chemotherapy_treatment_plan import ChemotherapyTreatmentPlan, ChemotherapyTreatmentPlanSearch, \
    ChemotherapyTreatmentPlanList
from resources.cie_10 import Cie_10, Cie_10List, Cie_10Search
from resources.cie_o_morphology import CieOMorphology, CieOMorphologyList, CieOMorphologySearch
from resources.cie_o_topography import CieOTopography, CieOTopographyList, CieOTopographySearch
from resources.cie_o_tumor_location import CieOTumorLocation, CieOTumorLocationList, CieOTumorLocationSearch
from resources.city import City, CityList, CitySearch
from resources.committee import Committee, CommitteeList, CommitteeSearch
from resources.configuration import Configuration, ConfigurationList, ConfigurationSearch
from resources.country import Country, CountryList, CountrySearch
from resources.deposit import Deposit, DepositList, DepositSearch
from resources.deposit_movement import DepositMovement, DepositMovementList, DepositMovementSearch
from resources.deposit_stock import DepositStock, DepositStockList, DepositStockSearch
from resources.destinatarios import Destinatarios, DestinatariosList, DestinatariosSearch
from resources.diagnosis import Diagnosis, DiagnosisSearch, DiagnosisList
from resources.diagnosis_ap import DiagnosisAp, DiagnosisApList, DiagnosisApSearch
from resources.dispatch_medications import DispatchMedications, DispatchMedicationsList, DispatchMedicationsSearch
from resources.doctor import Doctor, DoctorList, DoctorSearch
from resources.doctor_specialty import DoctorSpecialty, DoctorSpecialtyList, DoctorSpecialtySearch
from resources.document_type import DocumentType, DocumentTypeList, DocumentTypeSearch
from resources.entries import Entries, EntriesList, EntriesSearch
from resources.entries_deposit_stock import EntriesDepositStock, EntriesDepositStockList, EntriesDepositStockSearch
from resources.entries_lot import EntriesLot, EntriesLotList, EntriesLotSearch
from resources.evaluation import Evaluation, EvaluationList, EvaluationSearch, PatientEvaluationSearch, UsersEvaluator, \
    EvaluationComplete
from resources.evaluators import Evaluators, EvaluatorsList, EvaluatorsSearch
from resources.follow_up_treatment_plan import FollowUpTreatmentPlan, FollowUpTreatmentPlanSearch, \
    FollowUpTreatmentPlanList
from resources.gender import Gender, GenderList, GenderSearch
from resources.history import History, HistoryList, HistorySearch, NewHistoryList
from resources.hospital import Hospital, HospitalList, HospitalSearch
from resources.interoperabilidad import InteroperabilidadPatient, InteroperabilidadStock, \
    InteroperabilidadPatientConsultation
from resources.interoperabilidad_task import InteroperabilidadSyncInventorySiciapTask, \
    InteroperabilidadSyncPatientSigapTask, \
    InteroperabilidadSyncPatientDispatchMedicationSiciapTask, InteroperabilidadSyncPatientConsultationHisTask, \
    InteroperabilidadSyncTaskManager
from resources.lot import Lot, LotList, LotSearch
from resources.manufacturer import Manufacturer, ManufacturerList, ManufacturerSearch
from resources.medical_consultation import MedicalConsultation, MedicalConsultationList, MedicalConsultationSearch
from resources.medical_document import MedicalDocument, MedicalDocumentList, MedicalDocumentSearch, \
    MedicalDocumentInitialSearch
from resources.medical_document_type import MedicalDocumentType, MedicalDocumentTypeList, MedicalDocumentTypeSearch, \
    MedicalDocumentTypeInitialList, MedicalDocumentTypeRequirementsList
from resources.medical_team import MedicalTeam, MedicalTeamList, MedicalTeamSearch
from resources.medicine import Medicine, MedicineList, MedicineSearch
from resources.medicine_chemotherapy import MedicineChemotherapy, MedicineChemotherapyList, MedicineChemotherapySearch
from resources.medicine_medical_consultation import MedicineMedicalConsultation, MedicineMedicalConsultationList, \
    MedicineMedicalConsultationSearch
from resources.medicine_treatment_follow_up import MedicineTreatmentFollowUp, MedicineTreatmentFollowUpList, \
    MedicineTreatmentFollowUpSearch
from resources.medicine_treatment_plan import MedicineTreatmentPlan, MedicineTreatmentPlanList, \
    MedicineTreatmentPlanSearch
from resources.menopausal_state import MenopausalState, MenopausalStateList, MenopausalStateSearch
from resources.message import MessageList, MessageSearch, Message
from resources.notificaciones import NotificacionesList, Notificaciones
from resources.notificaciones import NotificacionesSearch
from resources.parameter import Parameter, ParameterList, ParameterSearch
from resources.patient import Patient, PatientList, PatientSearch, ServicePatient, PatientByDocument, PatientsAll, \
    PatientSearchNative, PatientImport
from resources.patient_exclusion_criteria import PatientExclusionCriteria, PatientExclusionCriteriaList, \
    PatientExclusionCriteriaSearch
from resources.patient_family_with_cancer import PatientFamilyWithCancer, PatientFamilyWithCancerList, \
    PatientFamilyWithCancerSearch
from resources.patient_hospital import PatientHospital, PatientHospitalList, PatientHospitalSearch
from resources.patient_inclusion_criteria import PatientInclusionCriteria, PatientInclusionCriteriaList, \
    PatientInclusionCriteriaSearch
from resources.patient_inclusion_criteria_adjuvant_trastuzumab import PatientInclusionCriteriaAdjuvantTrastuzumab, \
    PatientInclusionCriteriaAdjuvantTrastuzumabList, PatientInclusionCriteriaAdjuvantTrastuzumabSearch
from resources.patient_inclusion_criteria_neoadjuvant_trastuzumab import PatientInclusionCriteriaNeoadjuvantTrastuzumab, \
    PatientInclusionCriteriaNeoadjuvantTrastuzumabList, PatientInclusionCriteriaNeoadjuvantTrastuzumabSearch
from resources.periodicity import Periodicity, PeriodicityList, PeriodicitySearch
from resources.permission import Permission, PermissionList, PermissionSearch
from resources.personal_pathological_history import PersonalPathologicalHistory, PersonalPathologicalHistoryList, \
    PersonalPathologicalHistorySearch
from resources.puncture import Puncture, PunctureList, PunctureSearch
from resources.radiotherapy import Radiotherapy, RadiotherapyList, RadiotherapySearch
from resources.radiotherapy_treatment_plan import RadiotherapyTreatmentPlan, RadiotherapyTreatmentPlanSearch, \
    RadiotherapyTreatmentPlanList
from resources.report import PatientSummarize, PatientReport, PatientInclusionExclusionReport, PatientReportExcel, \
    Indicator1Report, DonationMedicationsReport, Indicator2Report
from resources.role import Role, RoleList, RoleSearch
from resources.role_permission import RolePermission, RolePermissionList, RolePermissionSearch
from resources.specialty import SpecialtySearch, SpecialtyList, Specialty
from resources.stock import Stock, StockList, StockSearch
from resources.superset import SupersetApi, Superset
from resources.supplier import Supplier, SupplierList, SupplierSearch
from resources.surgery import Surgery, SurgeryList, SurgerySearch
from resources.treatment_follow_up import TreatmentFollowUp, TreatmentFollowUpList, TreatmentFollowUpSearch
from resources.treatment_plan import TreatmentPlan, TreatmentPlanList, TreatmentPlanSearch, TreatmentPlanPlanification, \
    TreatmentPlanNumber
from resources.treatment_request import TreatmentRequest, TreatmentRequestList, TreatmentRequestSearch
from resources.treatment_scheme import TreatmentSchemeList, TreatmentScheme, TreatmentSchemeSearch
from resources.type_treatment import TypeTreatment, TypeTreatmentList, TypeTreatmentSearch
from resources.user import User, UserList, UserSearch, UserChangePass
from resources.user_role import UserRole, UserRoleList, UserRoleSearch
from utils import JSONEncoder, sha1_pass, JSONDecoder
from version import __version__

PREFIX = os.environ.get('PREFIX_PATH', '/api')
STATIC_FOLDER = os.environ.get('STATIC_FOLDER', 'static')
LOGS_FOLDER = os.environ.get('PREFIX_PATH', 'logs')

# Crear el directorio 'logs/' si no existe
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOGS_FOLDER)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path=f'{PREFIX}/{STATIC_FOLDER}')
babel = Babel(app)
CORS(app, supports_credentials=True)
api = Api(app, errors={
    'NoAuthorizationError': {
        "message": "Request does not contain an access token.",
        'error': 'authorization_required',
        'status': 401
    }
})

# TODO: only for local development... do not send to repository !
# app.debug = True

app.config['RESTFUL_JSON'] = {'cls': JSONEncoder}

# Set supported languages
app.config['LANGUAGES'] = ['en', 'es']
app.json_encoder = JSONEncoder
app.json_decoder = JSONDecoder

# Logging configuration
# Crear un folder de logs si no existe
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configurar el logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crear un handler para la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Crear un handler para los archivos de log rotativos
file_handler = TimedRotatingFileHandler('logs/app.log', when='D', interval=1, backupCount=30)
file_handler.setLevel(logging.INFO)
file_handler.suffix = "%Y-%m-%d"  # Nombre de los archivos con el día correspondiente

# Formato de log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Añadir handlers al logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

@app.errorhandler(404)
def handle_404_error(e):
    return jsonify({
        "description": "You seem lost...",
        'error': 'resource_not_found'
    }), 404


@app.errorhandler(400)
def handle_400_error(e):
    return jsonify({
        "description": "I don't understand this, please send it right.. appreciated!",
        'error': 'bad_request'
    }), 404


# TODO: Setear el local del navegador
def get_locale():
    return 'es'


babel.init_app(app, locale_selector=get_locale)


# Function to facilitate the app configuration from environment variables
def env_config(name, default):
    app.config[name] = os.environ.get(name, default=default)


# Database config
env_config('DB_USERNAME', 'postgres')
env_config('DB_PASSWORD', '123')
env_config('DB_HOST', '192.168.11.220')
env_config('DB_DATABASE', 'ccan_py')
env_config('DB_SCHEMA', 'public')
env_config('DB_PORT', '5432')
env_config('SQLALCHEMY_DATABASE_URI',
           f"postgresql://{app.config['DB_USERNAME']}:{app.config['DB_PASSWORD']}@{app.config['DB_HOST']}:{app.config['DB_PORT']}/{app.config['DB_DATABASE']}")

env_config('DB_INTEROPERABILIDAD', 'postgresql://readiness:Readiness.@localhost:5433/MSPSBS_REDINET')
app.config['SQLALCHEMY_BINDS'] = {
    # 'anotherdb':        'postgresql://postgres:postgres@localhost:5432/anotherdb'
    'interoperabilidad': app.config['DB_INTEROPERABILIDAD']
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = False

# Swagger config
app.config['SWAGGER'] = {
    'title': 'C/CAN City Soft',
    'version': '2.0.0',
    'description': 'Web Services API',
    'uiversion': 2,
    'tags': [{'name': 'jwt'}],
    'specs': [{
        'endpoint': 'apispec_1',
        'route': f'{PREFIX}/apispec_1.json',
        'rule_filter': lambda rule: True,  # all in
        'model_filter': lambda tag: True  # all in
    }],
    'specs_route': "/apidocs/",
    'static_url_path': '/static/swagger'
}
swagger = Swagger(app)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ERROR_MESSAGE_KEY'] = 'error'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

# Files configuration
env_config('UPLOAD_FOLDER', f'{STATIC_FOLDER}/uploaded_files')
env_config('MAX_CONTENT_LENGTH', 50 * 1000 * 1000)  # By default 50MB
env_config('MAX_PATH_LENGTH', 255)

# Servicio getCedula
env_config('BACKEND_MSPBS_URL', 'https://ws.mspbs.gov.py/api/getPersonas.php')
env_config('AUTH_MSPBS_USER', 'personas')
env_config('AUTH_MSPBS_PASS', '@g3137c0120')

# Encryption
# Random Encription Key
env_config('ENCRYPTION_KEY', 'q2_fbWIugwcQSwvXE5SVeRBAR0CgLQNGkJYEJsyU5zM=')

# Superset
env_config('SUPERSET_URL', 'https://dashboard.codelab.systems')
env_config('SUPERSET_USERNAME', 'readiness')
env_config('SUPERSET_PASSWORD', 'readiness')
env_config('SUPERSET_DASHBOARD_ID', 'bbb054f0-85ae-48d9-a179-0e6b625a7798')

# tokens blacklist (replace this with database table or a redis cluster in production)
blacklist = set()


@app.before_request
def before_request():
    try:
        verify_jwt_in_request()
        identity = get_jwt_identity()
        query = f"SELECT SET_CONFIG('myapp.current_username', '{identity}', false);"

    except Exception as e:
        query = "SELECT SET_CONFIG('myapp.current_username', 'NOT_LOGGED', false);"

    db.session.execute(query)


# Change this to get permissions from your permission store (database, redis, cache, file, etc.)
@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    p = UserRoleModel.query.join(UserModel).filter(UserModel.user == identity).all()
    result = {
        'roles': list(map(lambda x: {
            'hospital_id': x.hospital_id,
            # 'permission': list(map(lambda y: y.description, x.role.permissions))
            # 'permission': []
            'hospital': x.hospital.description,
            'rol': x.role.description
        }, p)),
        'admin': UserModel.find_by_user(identity).administrator,
        'hospital_id': None
    }
    return result


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    # TODO: Replace this with a centralized cache service (Redis, Mongo, a database, etc.)
    return jti in blacklist


######################
# Application routes #
######################

@app.route('/')
@app.route(f'{PREFIX}')
def welcome():
    return redirect("/apidocs", code=302)


@app.route(f'{PREFIX}/version')
def get_version():
    return jsonify({"version": __version__})


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route(f'{PREFIX}/login', methods=['POST'])
@swag_from('swagger/flask_jwt_extended/login.yaml')
def login():
    if not request.is_json:
        return jsonify({"error": _("BAD_REQUEST")}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"error": _("BAD_USERNAME_OR_PASSWORD")}), 400

    usuario_result = UserModel.query.filter_by(user=username, password=sha1_pass(password), state='A').all()

    if len(usuario_result) == 0:
        return jsonify({"error": _("BAD_USERNAME_OR_PASSWORD")}), 401

    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=username, expires_delta=expires)

    return jsonify(access_token=access_token), 200


@app.route(f'{PREFIX}/establishment_change', methods=['POST'])
@jwt_required()
@swag_from('swagger/flask_jwt_extended/establishment_change.yaml')
def establishment_change():
    user = UserModel.find_by_user(get_jwt_identity())
    if not user:
        return jsonify({"error": _("USER_NOT_FOUND")}), 400

    hospital_id = request.json.get('hospital_id')
    if hospital_id:
        hospital = HospitalModel.find_by_id(hospital_id)
        if not hospital:
            return jsonify({"error": _("HOSPITAL_NOT_FOUND")}), 404

        if not user.administrator:
            user_role = next(
                (role for role in user.role_list if role.hospital_id == hospital_id),
                None
            )
            if not user_role:
                return jsonify({"error": _("USER_NOT_ASSOCIATED_WITH_HOSPITAL")}), 403

    identity = user.user
    expires = datetime.timedelta(days=1)
    additional_claims = {"hospital_id": int(hospital_id)}
    access_token = create_access_token(identity=identity, expires_delta=expires, additional_claims=additional_claims)

    jti = get_jwt()['jti']
    blacklist.add(jti)

    return jsonify(access_token=access_token), 200


@app.route(f'{PREFIX}/logout', methods=['DELETE'])
@jwt_required()
@swag_from('swagger/flask_jwt_extended/logout.yaml')
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": _("SUCCESSFULLY_OUT")}), 200


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route(f'{PREFIX}/protected', methods=['GET'])
@jwt_required()
@swag_from('swagger/protected/example.yaml')
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route(f'{PREFIX}/permissions/<identity>', methods=['get'])
def permissions(identity):
    p = UserRoleModel.query.join(UserModel).filter(UserModel.user == identity).all()

    # Crear un diccionario para almacenar los permisos agrupados por hospital_id
    permissions_by_hospital = {}

    # Recorrer cada entrada relacionada con el usuario
    for entry in p:
        hospital_id = entry.hospital_id

        if hospital_id not in permissions_by_hospital:
            permissions_by_hospital[hospital_id] = set()

        # Agregar permisos directos del rol
        role_permissions = {perm.description for perm in entry.role.permissions}
        permissions_by_hospital[hospital_id].update(role_permissions)

        # Agregar permisos de los módulos relacionados con el rol
        for module_role in entry.role.module_list:
            module_permissions = {perm.description for perm in module_role.module.permissions}
            permissions_by_hospital[hospital_id].update(module_permissions)

    # Formatear el resultado como una lista de diccionarios
    result_permissions = [
        {
            'hospital_id': hospital_id,
            'permission': list(permissions)
        }
        for hospital_id, permissions in permissions_by_hospital.items()
    ]

    # Crear el resultado final
    result = {
        'permissions': result_permissions,
        'admin': UserModel.find_by_user(identity).administrator
    }
    return jsonify(result)


#############
# Inventory #
#############

api.add_resource(Lot, f'{PREFIX}/lot/<id>')
api.add_resource(LotList, f'{PREFIX}/lot')
api.add_resource(LotSearch, f'{PREFIX}/search/lot')

api.add_resource(Manufacturer, f'{PREFIX}/manufacturer/<id>')
api.add_resource(ManufacturerList, f'{PREFIX}/manufacturer')
api.add_resource(ManufacturerSearch, f'{PREFIX}/search/manufacturer')

api.add_resource(Supplier, f'{PREFIX}/supplier/<id>')
api.add_resource(SupplierList, f'{PREFIX}/supplier')
api.add_resource(SupplierSearch, f'{PREFIX}/search/supplier')

api.add_resource(Deposit, f'{PREFIX}/deposit/<id>')
api.add_resource(DepositList, f'{PREFIX}/deposit')
api.add_resource(DepositSearch, f'{PREFIX}/search/deposit')

api.add_resource(Entries, f'{PREFIX}/entries/<id>')
api.add_resource(EntriesList, f'{PREFIX}/entries')
api.add_resource(EntriesSearch, f'{PREFIX}/search/entries')

api.add_resource(DepositStock, f'{PREFIX}/deposit_stock/<id>')
api.add_resource(DepositStockList, f'{PREFIX}/deposit_stock')
api.add_resource(DepositStockSearch, f'{PREFIX}/search/deposit_stock')

api.add_resource(Stock, f'{PREFIX}/stock/<id>')
api.add_resource(StockList, f'{PREFIX}/stock')
api.add_resource(StockSearch, f'{PREFIX}/search/stock')

api.add_resource(DepositMovement, f'{PREFIX}/deposit_movement/<id>')
api.add_resource(DepositMovementList, f'{PREFIX}/deposit_movement')
api.add_resource(DepositMovementSearch, f'{PREFIX}/search/deposit_movement')

api.add_resource(DispatchMedications, f'{PREFIX}/dispatch_medications/<id>')
api.add_resource(DispatchMedicationsList, f'{PREFIX}/dispatch_medications')
api.add_resource(DispatchMedicationsSearch, f'{PREFIX}/search/dispatch_medications')

api.add_resource(History, f'{PREFIX}/history/<id>')
api.add_resource(HistoryList, f'{PREFIX}/history')
api.add_resource(HistorySearch, f'{PREFIX}/search/history')
api.add_resource(NewHistoryList, f'{PREFIX}/history_list/<stock_id>')

##########################
# Patient Administration #
##########################

api.add_resource(MedicalTeam, f'{PREFIX}/medical_team/<id>')
api.add_resource(MedicalTeamList, f'{PREFIX}/medical_team')
api.add_resource(MedicalTeamSearch, f'{PREFIX}/search/medical_team')

api.add_resource(MedicineTreatmentPlan, f'{PREFIX}/medicine_treatment_plan/<id>')
api.add_resource(MedicineTreatmentPlanList, f'{PREFIX}/medicine_treatment_plan')
api.add_resource(MedicineTreatmentPlanSearch, f'{PREFIX}/search/medicine_treatment_plan')

api.add_resource(TreatmentPlan, f'{PREFIX}/treatment_plan/<id>')
api.add_resource(TreatmentPlanList, f'{PREFIX}/treatment_plan')
api.add_resource(TreatmentPlanSearch, f'{PREFIX}/search/treatment_plan')
api.add_resource(TreatmentPlanPlanification, f'{PREFIX}/planification/treatment_plan')
api.add_resource(TreatmentPlanNumber, f'{PREFIX}/number/treatment_plan/<patient_id>')

api.add_resource(UserRole, f'{PREFIX}/user_role/<id>')
api.add_resource(UserRoleList, f'{PREFIX}/user_role')
api.add_resource(UserRoleSearch, f'{PREFIX}/search/user_role')

api.add_resource(Patient, f'{PREFIX}/patient/<id>')
api.add_resource(PatientList, f'{PREFIX}/patient')
# api.add_resource(PatientSearch, f'{PREFIX}/search/patient')
api.add_resource(PatientSearchNative, f'{PREFIX}/search/patient')
api.add_resource(ServicePatient, f'{PREFIX}/service/getpatient/<ciPatient>')
api.add_resource(PatientByDocument, f'{PREFIX}/get/patient_by_document/<document>')
api.add_resource(PatientImport, f'{PREFIX}/import/patient')

api.add_resource(Permission, f'{PREFIX}/permission/<id>')
api.add_resource(PermissionList, f'{PREFIX}/permission')
api.add_resource(PermissionSearch, f'{PREFIX}/search/permission')

api.add_resource(User, f'{PREFIX}/user/<id>')
api.add_resource(UserList, f'{PREFIX}/user')
api.add_resource(UserSearch, f'{PREFIX}/search/user')
api.add_resource(UserChangePass, f'{PREFIX}/change_password/<username>')

api.add_resource(Radiotherapy, f'{PREFIX}/radiotherapy/<id>')
api.add_resource(RadiotherapyList, f'{PREFIX}/radiotherapy')
api.add_resource(RadiotherapySearch, f'{PREFIX}/search/radiotherapy')

api.add_resource(Chemotherapy, f'{PREFIX}/chemotherapy/<id>')
api.add_resource(ChemotherapyList, f'{PREFIX}/chemotherapy')
api.add_resource(ChemotherapySearch, f'{PREFIX}/search/chemotherapy')

api.add_resource(DocumentType, f'{PREFIX}/document_type/<id>')
api.add_resource(DocumentTypeList, f'{PREFIX}/document_type')
api.add_resource(DocumentTypeSearch, f'{PREFIX}/search/document_type')

api.add_resource(MedicalDocument, f'{PREFIX}/medical_document/<id>')
api.add_resource(MedicalDocumentList, f'{PREFIX}/medical_document')
api.add_resource(MedicalDocumentSearch, f'{PREFIX}/search/medical_document')
api.add_resource(MedicalDocumentInitialSearch, f'{PREFIX}/search/medical_document_initial')

api.add_resource(MedicalDocumentType, f'{PREFIX}/medical_document_type/<id>')
api.add_resource(MedicalDocumentTypeList, f'{PREFIX}/medical_document_type')
api.add_resource(MedicalDocumentTypeSearch, f'{PREFIX}/search/medical_document_type')
api.add_resource(MedicalDocumentTypeInitialList, f'{PREFIX}/medical_document_type_initial')
api.add_resource(MedicalDocumentTypeRequirementsList, f'{PREFIX}/requirements/medical_document_type/<patient_id>')

api.add_resource(Gender, f'{PREFIX}/gender/<id>')
api.add_resource(GenderList, f'{PREFIX}/gender')
api.add_resource(GenderSearch, f'{PREFIX}/search/gender')

api.add_resource(Country, f'{PREFIX}/country/<id>')
api.add_resource(CountryList, f'{PREFIX}/country')
api.add_resource(CountrySearch, f'{PREFIX}/search/country')

api.add_resource(Area, f'{PREFIX}/area/<id>')
api.add_resource(AreaList, f'{PREFIX}/area')
api.add_resource(AreaSearch, f'{PREFIX}/search/area')

api.add_resource(City, f'{PREFIX}/city/<id>')
api.add_resource(CityList, f'{PREFIX}/city')
api.add_resource(CitySearch, f'{PREFIX}/search/city')

api.add_resource(DiagnosisAp, f'{PREFIX}/diagnosis_ap/<id>')
api.add_resource(DiagnosisApList, f'{PREFIX}/diagnosis_ap')
api.add_resource(DiagnosisApSearch, f'{PREFIX}/search/diagnosis_ap')

api.add_resource(Surgery, f'{PREFIX}/surgery/<id>')
api.add_resource(SurgeryList, f'{PREFIX}/surgery')
api.add_resource(SurgerySearch, f'{PREFIX}/search/surgery')

api.add_resource(Role, f'{PREFIX}/role/<id>')
api.add_resource(RoleList, f'{PREFIX}/role')
api.add_resource(RoleSearch, f'{PREFIX}/search/role')

api.add_resource(Hospital, f'{PREFIX}/hospital/<id>')
api.add_resource(HospitalList, f'{PREFIX}/hospital')
api.add_resource(HospitalSearch, f'{PREFIX}/search/hospital')

api.add_resource(Puncture, f'{PREFIX}/puncture/<id>')
api.add_resource(PunctureList, f'{PREFIX}/puncture')
api.add_resource(PunctureSearch, f'{PREFIX}/search/puncture')

api.add_resource(Periodicity, f'{PREFIX}/periodicity/<id>')
api.add_resource(PeriodicityList, f'{PREFIX}/periodicity')
api.add_resource(PeriodicitySearch, f'{PREFIX}/search/periodicity')

api.add_resource(TypeTreatment, f'{PREFIX}/type_treatment/<id>')
api.add_resource(TypeTreatmentList, f'{PREFIX}/type_treatment')
api.add_resource(TypeTreatmentSearch, f'{PREFIX}/search/type_treatment')

api.add_resource(RolePermission, f'{PREFIX}/role_permission/<id>')
api.add_resource(RolePermissionList, f'{PREFIX}/role_permission')
api.add_resource(RolePermissionSearch, f'{PREFIX}/search/role_permission')

api.add_resource(Cie_10, f'{PREFIX}/cie_10/<id>')
api.add_resource(Cie_10List, f'{PREFIX}/cie_10')
api.add_resource(Cie_10Search, f'{PREFIX}/search/cie_10')

api.add_resource(CieOMorphology, f'{PREFIX}/cie_o_morphology/<id>')
api.add_resource(CieOMorphologyList, f'{PREFIX}/cie_o_morphology')
api.add_resource(CieOMorphologySearch, f'{PREFIX}/search/cie_o_morphology')

api.add_resource(CieOTumorLocation, f'{PREFIX}/cie_o_tumor_location/<id>')
api.add_resource(CieOTumorLocationList, f'{PREFIX}/cie_o_tumor_location')
api.add_resource(CieOTumorLocationSearch, f'{PREFIX}/search/cie_o_tumor_location')

api.add_resource(CieOTopography, f'{PREFIX}/cie_o_topography/<id>')
api.add_resource(CieOTopographyList, f'{PREFIX}/cie_o_topography')
api.add_resource(CieOTopographySearch, f'{PREFIX}/search/cie_o_topography')

api.add_resource(MenopausalState, f'{PREFIX}/menopausal_state/<id>')
api.add_resource(MenopausalStateList, f'{PREFIX}/menopausal_state')
api.add_resource(MenopausalStateSearch, f'{PREFIX}/search/menopausal_state')

api.add_resource(Medicine, f'{PREFIX}/medicine/<id>')
api.add_resource(MedicineList, f'{PREFIX}/medicine')
api.add_resource(MedicineSearch, f'{PREFIX}/search/medicine')

api.add_resource(Doctor, f'{PREFIX}/doctor/<id>')
api.add_resource(DoctorList, f'{PREFIX}/doctor')
api.add_resource(DoctorSearch, f'{PREFIX}/search/doctor')

api.add_resource(Parameter, f'{PREFIX}/parameter/<id>')
api.add_resource(ParameterList, f'{PREFIX}/parameter')
api.add_resource(ParameterSearch, f'{PREFIX}/search/parameter')

api.add_resource(PatientInclusionCriteriaAdjuvantTrastuzumab,
                 f'{PREFIX}/patient_inclusion_criteria_adjuvant_trastuzumab/<id>')
api.add_resource(PatientInclusionCriteriaAdjuvantTrastuzumabList,
                 f'{PREFIX}/patient_inclusion_criteria_adjuvant_trastuzumab')
api.add_resource(PatientInclusionCriteriaAdjuvantTrastuzumabSearch,
                 f'{PREFIX}/search/patient_inclusion_criteria_adjuvant_trastuzumab')

api.add_resource(PatientInclusionCriteriaNeoadjuvantTrastuzumab,
                 f'{PREFIX}/patient_inclusion_criteria_neoadjuvant_trastuzumab/<id>')
api.add_resource(PatientInclusionCriteriaNeoadjuvantTrastuzumabList,
                 f'{PREFIX}/patient_inclusion_criteria_neoadjuvant_trastuzumab')
api.add_resource(PatientInclusionCriteriaNeoadjuvantTrastuzumabSearch,
                 f'{PREFIX}/search/patient_inclusion_criteria_neoadjuvant_trastuzumab')

api.add_resource(PatientExclusionCriteria, f'{PREFIX}/patient_exclusion_criteria/<id>')
api.add_resource(PatientExclusionCriteriaList, f'{PREFIX}/patient_exclusion_criteria')
api.add_resource(PatientExclusionCriteriaSearch, f'{PREFIX}/search/patient_exclusion_criteria')

api.add_resource(Committee, f'{PREFIX}/committee/<id>')
api.add_resource(CommitteeList, f'{PREFIX}/committee')
api.add_resource(CommitteeSearch, f'{PREFIX}/search/committee')

api.add_resource(PatientInclusionCriteria, f'{PREFIX}/patient_inclusion_criteria/<id>')
api.add_resource(PatientInclusionCriteriaList, f'{PREFIX}/patient_inclusion_criteria')
api.add_resource(PatientInclusionCriteriaSearch, f'{PREFIX}/search/patient_inclusion_criteria')

api.add_resource(TreatmentFollowUp, f'{PREFIX}/treatment_follow_up/<id>')
api.add_resource(TreatmentFollowUpList, f'{PREFIX}/treatment_follow_up')
api.add_resource(TreatmentFollowUpSearch, f'{PREFIX}/search/treatment_follow_up')

api.add_resource(Specialty, f'{PREFIX}/specialty/<id>')
api.add_resource(SpecialtyList, f'{PREFIX}/specialty')
api.add_resource(SpecialtySearch, f'{PREFIX}/search/specialty')

api.add_resource(DoctorSpecialty, f'{PREFIX}/doctor_specialty/<id>')
api.add_resource(DoctorSpecialtyList, f'{PREFIX}/doctor_specialty')
api.add_resource(DoctorSpecialtySearch, f'{PREFIX}/search/doctor_specialty')

api.add_resource(MedicalConsultation, f'{PREFIX}/medical_consultation/<id>')
api.add_resource(MedicalConsultationList, f'{PREFIX}/medical_consultation')
api.add_resource(MedicalConsultationSearch, f'{PREFIX}/search/medical_consultation')

api.add_resource(PersonalPathologicalHistory, f'{PREFIX}/personal_pathological_history/<id>')
api.add_resource(PersonalPathologicalHistoryList, f'{PREFIX}/personal_pathological_history')
api.add_resource(PersonalPathologicalHistorySearch, f'{PREFIX}/search/personal_pathological_history')

api.add_resource(PatientFamilyWithCancer, f'{PREFIX}/patient_family_with_cancer/<id>')
api.add_resource(PatientFamilyWithCancerList, f'{PREFIX}/patient_family_with_cancer')
api.add_resource(PatientFamilyWithCancerSearch, f'{PREFIX}/search/patient_family_with_cancer')

api.add_resource(Evaluation, f'{PREFIX}/evaluation/<id>')
api.add_resource(EvaluationList, f'{PREFIX}/evaluation')
api.add_resource(EvaluationSearch, f'{PREFIX}/search/evaluation')
api.add_resource(PatientEvaluationSearch, f'{PREFIX}/search/patient_evaluation')
api.add_resource(UsersEvaluator, f'{PREFIX}/evaluation/user_evaluators')
api.add_resource(EvaluationComplete, f'{PREFIX}/evaluation/complete_revision/<patient_id>')

api.add_resource(Evaluators, f'{PREFIX}/evaluators/<id>')
api.add_resource(EvaluatorsList, f'{PREFIX}/evaluators')
api.add_resource(EvaluatorsSearch, f'{PREFIX}/search/evaluators')

api.add_resource(MedicineTreatmentFollowUp, '/medicine_treatment_follow_up/<id>')
api.add_resource(MedicineTreatmentFollowUpList, '/medicine_treatment_follow_up')
api.add_resource(MedicineTreatmentFollowUpSearch, '/search/medicine_treatment_follow_up')

# SERVICIOS DE INTEROPERABILIDAD
api.add_resource(InteroperabilidadPatient, f'{PREFIX}/interoperabilidad/patient/<patient_id>')
api.add_resource(InteroperabilidadStock, f'{PREFIX}/interoperabilidad/stock/<stock_id>')
api.add_resource(InteroperabilidadPatientConsultation, f'{PREFIX}/interoperabilidad/patient_consultation/<patient_id>')

api.add_resource(InteroperabilidadSyncTaskManager, f'{PREFIX}/interoperabilidad/tasks/task_manager')
api.add_resource(InteroperabilidadSyncPatientSigapTask, f'{PREFIX}/interoperabilidad/tasks/patient')
api.add_resource(InteroperabilidadSyncPatientConsultationHisTask, f'{PREFIX}/interoperabilidad/tasks/patient_consultation')
api.add_resource(InteroperabilidadSyncPatientDispatchMedicationSiciapTask, f'{PREFIX}/interoperabilidad/tasks/patient_dispatch_medications')
api.add_resource(InteroperabilidadSyncInventorySiciapTask, f'{PREFIX}/interoperabilidad/tasks/stock')

api.add_resource(Configuration, f'{PREFIX}/configuration/<id>')
api.add_resource(ConfigurationList, f'{PREFIX}/configuration')
api.add_resource(ConfigurationSearch, f'{PREFIX}/search/configuration')

api.add_resource(Diagnosis, f'{PREFIX}/diagnosis/<id>')
api.add_resource(DiagnosisList, f'{PREFIX}/diagnosis')
api.add_resource(DiagnosisSearch, f'{PREFIX}/search/diagnosis')

api.add_resource(MedicineMedicalConsultation, f'{PREFIX}/medicine_medical_consultation/<id>')
api.add_resource(MedicineMedicalConsultationList, f'{PREFIX}/medicine_medical_consultation')
api.add_resource(MedicineMedicalConsultationSearch, f'{PREFIX}/search/medicine_medical_consultation')

api.add_resource(EntriesLot, f'{PREFIX}/entries_lot/<id>')
api.add_resource(EntriesLotList, f'{PREFIX}/entries_lot')
api.add_resource(EntriesLotSearch, f'{PREFIX}/search/entries_lot')

api.add_resource(EntriesDepositStock, f'{PREFIX}/entries_deposit_stock/<id>')
api.add_resource(EntriesDepositStockList, f'{PREFIX}/entries_deposit_stock')
api.add_resource(EntriesDepositStockSearch, f'{PREFIX}/search/entries_deposit_stock')

api.add_resource(FollowUpTreatmentPlan, f'{PREFIX}/follow_up_treatment_plan/<id>')
api.add_resource(FollowUpTreatmentPlanList, f'{PREFIX}/follow_up_treatment_plan')
api.add_resource(FollowUpTreatmentPlanSearch, f'{PREFIX}/search/follow_up_treatment_plan')

api.add_resource(ChemotherapyTreatmentPlan, f'{PREFIX}/chemotherapy_treatment_plan/<id>')
api.add_resource(ChemotherapyTreatmentPlanList, f'{PREFIX}/chemotherapy_treatment_plan')
api.add_resource(ChemotherapyTreatmentPlanSearch, f'{PREFIX}/search/chemotherapy_treatment_plan')

api.add_resource(RadiotherapyTreatmentPlan, f'{PREFIX}/radiotherapy_treatment_plan/<id>')
api.add_resource(RadiotherapyTreatmentPlanList, f'{PREFIX}/radiotherapy_treatment_plan')
api.add_resource(RadiotherapyTreatmentPlanSearch, f'{PREFIX}/search/radiotherapy_treatment_plan')

api.add_resource(PatientHospital, f'{PREFIX}/patient_hospital/<id>')
api.add_resource(PatientHospitalList, f'{PREFIX}/patient_hospital')
api.add_resource(PatientHospitalSearch, f'{PREFIX}/search/patient_hospital')

api.add_resource(MedicineChemotherapy, f'{PREFIX}/medicine_chemotherapy/<id>')
api.add_resource(MedicineChemotherapyList, f'{PREFIX}/medicine_chemotherapy')
api.add_resource(MedicineChemotherapySearch, f'{PREFIX}/search/medicine_chemotherapy')

api.add_resource(Message, f'{PREFIX}/message/<id>')
api.add_resource(MessageList, f'{PREFIX}/message')
api.add_resource(MessageSearch, f'{PREFIX}/search/message')

api.add_resource(Destinatarios, f'{PREFIX}/inbox/<id>')
api.add_resource(DestinatariosList, f'{PREFIX}/inbox')
api.add_resource(DestinatariosSearch, f'{PREFIX}/search/inbox')

api.add_resource(Notificaciones, f'{PREFIX}/notificaciones/<id>')
api.add_resource(NotificacionesList, f'{PREFIX}/notificaciones')
api.add_resource(NotificacionesSearch, f'{PREFIX}/search/notificaciones')

# Reports
api.add_resource(PatientSummarize, f'{PREFIX}/summarize/patient/<patient_id>')
api.add_resource(PatientReport, f'{PREFIX}/report/patient/<patient_id>')
api.add_resource(PatientReportExcel, f'{PREFIX}/report_excel/patient/<patient_id>')
api.add_resource(PatientInclusionExclusionReport, f'{PREFIX}/report/patient_incl_excl/<patient_id>')

api.add_resource(Indicator1Report, f'{PREFIX}/report/indicator_1')
api.add_resource(Indicator2Report, f'{PREFIX}/report/indicator_2')
api.add_resource(DonationMedicationsReport, f'{PREFIX}/report/donation_medications')

# Superset
api.add_resource(Superset, f'{PREFIX}/superset/superset_data')
api.add_resource(SupersetApi, f'{PREFIX}/superset/fetch_guest_token')

# CSVDownload
api.add_resource(PatientsAll, f'{PREFIX}/patient_download_csv')

api.add_resource(CervixForm, f'{PREFIX}/cervix_form/<id>')
api.add_resource(CervixFormList, f'{PREFIX}/cervix_form')
api.add_resource(CervixFormSearch, f'{PREFIX}/search/cervix_form')

api.add_resource(BreastForm, f'{PREFIX}/breast_form/<id>')
api.add_resource(BreastFormList, f'{PREFIX}/breast_form')
api.add_resource(BreastFormSearch, f'{PREFIX}/search/breast_form')

api.add_resource(CervixBreastHeaderForm, f'{PREFIX}/cervix_breast_header_form/<patient_id>')

api.add_resource(ModulePermission, f'{PREFIX}/module_permission/<id>')
api.add_resource(ModulePermissionList, f'{PREFIX}/module_permission')
api.add_resource(ModulePermissionSearch, f'{PREFIX}/search/module_permission')

api.add_resource(ModuleRole, f'{PREFIX}/module_role/<id>')
api.add_resource(ModuleRoleList, f'{PREFIX}/module_role')
api.add_resource(ModuleRoleSearch, f'{PREFIX}/search/module_role')

api.add_resource(Module, f'{PREFIX}/module/<id>')
api.add_resource(ModuleList, f'{PREFIX}/module')
api.add_resource(ModuleSearch, f'{PREFIX}/search/module')

api.add_resource(DepositLot, f'{PREFIX}/deposit_lot/<id>')
api.add_resource(DepositLotList, f'{PREFIX}/deposit_lot')
api.add_resource(DepositLotSearch, f'{PREFIX}/search/deposit_lot')
api.add_resource(DepositLotQuantitySearch, f'{PREFIX}/search/deposit_lot_quantity')

api.add_resource(TreatmentScheme, f'{PREFIX}/treatment_scheme/<uuid>')
api.add_resource(TreatmentSchemeList, f'{PREFIX}/treatment_scheme')
api.add_resource(TreatmentSchemeSearch, f'{PREFIX}/search/treatment_scheme')

api.add_resource(TreatmentRequest, f'{PREFIX}/treatment_request/<uuid>')
api.add_resource(TreatmentRequestList, f'{PREFIX}/treatment_request')
api.add_resource(TreatmentRequestSearch, f'{PREFIX}/search/treatment_request')

api.add_resource(DrugResource, f'{PREFIX}/drug/<uuid>')
api.add_resource(DrugListResource, f'{PREFIX}/drug')
api.add_resource(DrugSearchResource, f'{PREFIX}/search/drug')

api.add_resource(ProductResource, f'{PREFIX}/product/<uuid>')
api.add_resource(ProductListResource, f'{PREFIX}/product')
api.add_resource(ProductSearchResource, f'{PREFIX}/search/product')



# Method for scheduled tasks daemon
# def start_scheduled_tasks_daemon():
#     with app.app_context():
#         logging.info("Scheduled Task Daemon Started")
#         while True:
#             run_time = get_run_time_from_db()
#             now_time = datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M'), '%H:%M').time()
#             if run_time == now_time:
#                 # Execute All Tasks
#                 task_manager()
#                 time.sleep(60)  # Se espera almenos 60 segundos antes de la siguiente comprobacion
#
#             time.sleep(60)


# Init thread daemon for scheduled tasks only in production mode
# def init_thread_scheduled_tasks():
#     start_scheduled_tasks_thread = Thread(target=start_scheduled_tasks_daemon)
#     start_scheduled_tasks_thread.start()


# init_thread_scheduled_tasks()


if __name__ == '__main__':
    db.init_app(app)
    app.run(host=os.environ.get("FLASK_HOST", default="localhost"), port=os.environ.get("FLASK_PORT", default=5000))

# these lines are required for debugging with pycharm (although you can delete them if you want)
else:
    db.init_app(app)
