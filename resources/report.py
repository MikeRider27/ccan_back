from io import BytesIO

import numpy as np
import pandas as pd
from flask import current_app, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_babel import _

from dao.patient_dao import PatientDao
from dao.report_dao import ReportDao
from reports.jasperutils import JasperUtils
from security import check
from utils import get_report_from_pandas


class PatientSummarize(Resource):
    @jwt_required()
    @check('patient_summarize')
    # @swag_from('../swagger/patient/get_patient.yaml')
    def get(self, patient_id):
        patient_dao = PatientDao()
        data = patient_dao.patient_sumarize(patient_id=patient_id)

        return data, 200


class PatientReport(Resource):

    @jwt_required()
    @check('patient_summarize')
    # @swag_from('../swagger/patient/get_patient.yaml')
    def get(self, patient_id):
        try:
            reports_params = request.args.to_dict()
            data = {
                'patient_id': patient_id,
                'cipher_key': current_app.config['ENCRYPTION_KEY'],
                'user_report': get_jwt_identity(),
                'personal_pathological_history_report': reports_params.get('personal_pathological_history_report',
                                                                           False) == 'true',
                'medical_consultation_report': reports_params.get('medical_consultation_report', False) == 'true',
                'diagnosis_report': reports_params.get('diagnosis_report', False) == 'true',
                'diagnosis_ap_report': reports_params.get('diagnosis_ap_report', False) == 'true',
                'treatment_plan_report': reports_params.get('treatment_plan_report', False) == 'true',
                'follow_up_treatment_report': reports_params.get('follow_up_treatment_report', False) == 'true',
                'chemotherapy_report': reports_params.get('chemotherapy_report', False) == 'true',
                'radiotherapy_report': reports_params.get('radiotherapy_report', False) == 'true',
                'surgery_report': reports_params.get('surgery_report', False) == 'true',
                'committee_report': reports_params.get('committee_report', False) == 'true'
            }

            jasperutils = JasperUtils()
            jasperutils.init_app()
            return jasperutils.print_pdf('patient/summarize', parameters=data, subreports=True)
        except Exception as e:
            return {'error': f'{e}'}, 500


class PatientReportExcel(Resource):

    @jwt_required()
    @check('patient_summarize')
    # @swag_from('../swagger/patient/get_patient.yaml')
    def get(self, patient_id):
        try:
            reports_params = request.args.to_dict()
            sheets = []
            report_dao = ReportDao()


            #  Siempre incluir los datos personales
            results = report_dao.patient_personal_data(patient_id=patient_id)
            personal_data = {
                'name': 'Datos Personales',
                'data': results
            }
            sheets.append(personal_data)


            # Verificar si diagnosis_report es True
            if reports_params.get('diagnosis_report', False) == 'true':
                diagnosis_results = report_dao.patient_diagnosis(patient_id=patient_id)
                diagnosis_sheet = {
                    'name': 'Diagnóstico',
                    'data': diagnosis_results
                }
                sheets.append(diagnosis_sheet)


            # Verificar si personal_pathological_history_report es True
            if reports_params.get('personal_pathological_history_report', False) == 'true':
                pathological_history_results = (report_dao.patient_pathological_history
                                                         (patient_id=patient_id))
                pathological_history_sheet = {
                    'name': 'Antecedentes Patológicos',
                    'data': pathological_history_results
                }
                sheets.append(pathological_history_sheet)


            # Verificar si medical_consultation_report es True
            if reports_params.get('medical_consultation_report', False) == 'true':
                medical_consultation_results = report_dao.patient_medical_consultation(patient_id=patient_id)
                medical_consultation_sheet = {
                    'name': 'Consulta Médica',
                    'data': medical_consultation_results
                }
                sheets.append(medical_consultation_sheet)


            # Verificar si diagnosis_ap_report es True
            if reports_params.get('diagnosis_ap_report', False) == 'true':
                diagnosis_ap_results = report_dao.patient_diagnosis_ap(patient_id=patient_id)
                diagnosis_ap_sheet = {
                    'name': 'Anatomía Patológica',
                    'data': diagnosis_ap_results
                }
                sheets.append(diagnosis_ap_sheet)


            # Verificar si treatment_plan_report es True
            if reports_params.get('treatment_plan_report', False) == 'true':
                treatment_plan_results = report_dao.patient_treatment_plan(patient_id=patient_id)
                treatment_plan_sheet = {
                    'name': 'Plan de Tratamiento',
                    'data': treatment_plan_results
                }
                sheets.append(treatment_plan_sheet)


            # Verificar si follow_up_treatment_report es True
            if reports_params.get('follow_up_treatment_report', False) == 'true':
                follow_up_results = report_dao.patient_follow_up(patient_id=patient_id)
                follow_up_sheet = {
                    'name': 'Seguimiento',
                    'data': follow_up_results
                }
                sheets.append(follow_up_sheet)


            # Verificar si chemotherapy_report es True
            if reports_params.get('chemotherapy_report', False) == 'true':
                chemotherapy_results = report_dao.patient_chemotherapy(patient_id=patient_id)
                chemotherapy_sheet = {
                    'name': 'Quimioterapia',
                    'data': chemotherapy_results
                }
                sheets.append(chemotherapy_sheet)


            # Verificar si radiotherapy_report es True
            if reports_params.get('radiotherapy_report', False) == 'true':
                radiotherapy_results = report_dao.patient_radiotherapy(patient_id=patient_id)
                radiotherapy_sheet = {
                    'name': 'Redioterapia',
                    'data': radiotherapy_results
                }
                sheets.append(radiotherapy_sheet)


            # Verificar si surgery_report es True
            if reports_params.get('surgery_report', False) == 'true':
                surgery_results = report_dao.patient_surgery(patient_id=patient_id)
                surgery_sheet = {
                    'name': 'Cirugía',
                    'data': surgery_results
                }
                sheets.append(surgery_sheet)


            # Verificar si committee_report es True
            if reports_params.get('committee_report', False) == 'true':
                medical_consultation_results = report_dao.patient_committee(patient_id=patient_id)
                medical_consultation_sheet = {
                    'name': 'Comité Multidisciplinario',
                    'data': medical_consultation_results
                }
                sheets.append(medical_consultation_sheet)


            excel = get_report_from_pandas(sheets)

            return excel

        except Exception as e:
            return {'error': f'{e}'}, 500


class PatientInclusionExclusionReport(Resource):
    @jwt_required()
    @check('patient_incl_excl_report')
    # @swag_from('../swagger/patient/get_patient.yaml')
    def get(self, patient_id):
        data = {
            'patient_id': patient_id,
            'cipher_key': current_app.config['ENCRYPTION_KEY']
        }

        try:
            jasperutils = JasperUtils()
            jasperutils.init_app()
            return jasperutils.print_pdf('patient/inc_exc', parameters=data)
        except Exception as e:
            return {'error': f'{e}'}, 500


class Indicator1Report(Resource):
    @jwt_required()
    @check('report_indicator_1_get')
    # @swag_from('../swagger/report/get_report_indicator_1.yaml')
    def get(self):
        sheets = []
        report_dao = ReportDao()

        # report_indicator_1
        results = report_dao.indicator_1()
        sheet = {
            'name': 'Informe Consolidado',
            'data': results
        }
        sheets.append(sheet)

        excel = get_report_from_pandas(sheets)

        return excel


class Indicator2Report(Resource):
    @jwt_required()
    @check('report_indicator_2_get')
    # @swag_from('../swagger/report/get_report_indicator_2.yaml')
    def get(self):
        sheets = []
        report_dao = ReportDao()

        # report_medications_used
        results = report_dao.indicator_2_medications_used()
        sheet = {
            'name': 'Medicina utilizadas',
            'data': results
        }
        sheets.append(sheet)

        excel = get_report_from_pandas(sheets)

        return excel


class DonationMedicationsReport(Resource):
    @jwt_required()
    @check('report_donation_medications_get')
    # @swag_from('../swagger/report/get_report_donation_medications.yaml')
    def get(self):
        report_dao = ReportDao()

        # report_medications_used
        results = report_dao.donation_medications()
        if len(results) == 0:
            return {'message': _("REPORT_DATA_NOT_FOUND")}, 404

        df = pd.DataFrame(results)

        # Añadir un índice para diferenciar las filas con el mismo ID paciente
        df['row_num'] = df.groupby('ID paciente').cumcount() + 1

        # Pivotar los datos
        pivoted = df.pivot_table(index='ID paciente', columns='row_num',
                                 values=['Código Medicamento', 'Nombre Medicamento',
                                         'Fecha de Inicio Medicamento',
                                         'Fecha de Fin Medicamento', 'Cantidad', 'Mg'],
                                 aggfunc='first').reset_index()

        # Asignar nombres de columnas para manipulacion
        pivoted.columns = [f'{col[0]} {col[1]}' if col[1] else col[0] for col in pivoted.columns]

        # Ajustar nombres de columnas y ordenarlas
        num_cols = len(df['row_num'].unique())
        new_columns = ['ID paciente']
        for num in range(1, num_cols + 1):
            new_columns += [
                f'Código Medicamento {num}',
                f'Nombre Medicamento {num}',
                f'Fecha de Inicio Medicamento {num}',
                f'Fecha de Fin Medicamento {num}',
                f'Cantidad {num}',
                f'Mg {num}'
            ]

        # Reorganizar las columnas en el DataFrame
        pivoted = pivoted[new_columns]

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            pivoted.to_excel(writer, index=False, sheet_name='Donación de Medicamentos')

            pivoted.replace([np.nan, np.inf, -np.inf], '', inplace=True)

            # Acceder al libro y a las hojas para aplicar estilos
            workbook = writer.book
            worksheet1 = writer.sheets['Donación de Medicamentos']

            # Definir estilos
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#e0e0e0',
                'border': 1
            })

            cell_format = workbook.add_format({
                'border': 1
            })

            # Aplicar estilos a las cabeceras
            worksheet1.write_row(0, 0, pivoted.columns, header_format)

            # Aplicar estilos a las celdas
            for row_num in range(1, len(pivoted) + 1):
                worksheet1.write_row(row_num, 0, pivoted.iloc[row_num - 1], cell_format)

        # Configura el puntero al principio del archivo
        output.seek(0)

        # Envía el archivo Excel al usuario
        return send_file(output, attachment_filename="reporte.xlsx", as_attachment=True)

