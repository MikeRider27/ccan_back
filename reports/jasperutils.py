import os

from flask import make_response, current_app
from pyreportjasper import JasperPy


class JasperUtils:

    reports_path = os.path.dirname(os.path.abspath(__file__))

    jasper = JasperPy()

    app = None
    con = None

    def init_app(self):
        self.app = current_app
        self.con = {
            'driver': 'postgres',
            'username': current_app.config['DB_USERNAME'],
            'password': current_app.config['DB_PASSWORD'],
            'host': current_app.config['DB_HOST'],
            'database': current_app.config['DB_DATABASE'],
            'schema': current_app.config['DB_SCHEMA'],
            'port': current_app.config['DB_PORT']
        }

    def print_pdf(self, name='summarize', parameters: dict = None, subreports: bool = False):
        if not parameters:
            parameters = {}

        jasper_file = self.reports_path + f'/jasperstudio/c_can_city_soft/{name}.jrxml'
        output_dir = self.reports_path + f'/tmp'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        pdf_file = f'{output_dir}/{name[name.rfind("/")+1:]}.pdf'
        resource = self.reports_path + f'/jasperstudio/c_can_city_soft'

        # Subreports
        if subreports:
            subreports_path = self.reports_path + f'/jasperstudio/c_can_city_soft/subreports'
            parameters['subreports_path'] = f"{subreports_path}/"

            # Listar archivos en la carpeta
            subreports_dir = os.listdir(subreports_path)

            # Imprimir los nombres de los archivos
            for subreport_file in subreports_dir:
                if subreport_file.endswith('.jrxml'):
                    subreport_path = os.path.join(subreports_path, subreport_file)
                    print(subreport_path)
                    self.jasper.compile(subreport_path)

            self.jasper.compile(jasper_file)
            jasper_file = self.reports_path + f'/jasperstudio/c_can_city_soft/{name}.jasper'

        try:
            for key in parameters.keys():
                parameters[key] = str(parameters[key])
            self.jasper.process(jasper_file, output_dir, parameters=parameters, db_connection=self.con,
                                format_list=["pdf"], resource=resource)
            with self.app.open_resource(pdf_file) as f:
                content = f.read()
            response = make_response(content)
            response.headers['Content-Type'] = 'application/pdf; charset=utf-8'
            response.headers['Content-Disposition'] = f'filename={name}.pdf'
            return response
        except Exception as e:
            print(e)
            return make_response(f'{{ error: "{e}" }}', 500)

    def print_excel(self, name='summarize', parameters: dict = None, subreports: bool = False):

        if not parameters:
            parameters = {}

        jasper_file = self.reports_path + f'/jasperstudio/c_can_city_soft/{name}.jrxml'
        output_dir = self.reports_path + f'/tmp'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        excel_file = f'{output_dir}/{name[name.rfind("/") + 1:]}.xlsx'
        resource = self.reports_path + f'/jasperstudio/c_can_city_soft'

        # Subreports
        if subreports:
            subreports_path = self.reports_path + f'/jasperstudio/c_can_city_soft/subreports'
            parameters['subreports_path'] = f"{subreports_path}/"

            # Listar archivos en la carpeta
            subreports_dir = os.listdir(subreports_path)

            # Imprimir los nombres de los archivos
            for subreport_file in subreports_dir:
                if subreport_file.endswith('.jrxml'):
                    subreport_path = os.path.join(subreports_path, subreport_file)
                    print(subreport_path)
                    self.jasper.compile(subreport_path)

            self.jasper.compile(jasper_file)
            jasper_file = self.reports_path + f'/jasperstudio/c_can_city_soft/{name}.jasper'

        try:
            for key in parameters.keys():
                parameters[key] = str(parameters[key])
            self.jasper.process(jasper_file, output_dir, parameters=parameters, db_connection=self.con,
                                format_list=["xlsx"], resource=resource)

            with self.app.open_resource(excel_file) as f:
                content = f.read()

            response = make_response(content)
            response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response.headers['Content-Disposition'] = f'attachment; filename={name}.xlsx'
            return response
        except Exception as e:
            print(e)
            return make_response(f'{{ error: "{e}" }}', 500)

    def compile_report(self, name):
        jrxml_file = self.reports_path + f'/jasperstudio/lipar/{name}.jrxml'
        try:
            self.jasper.compile(jrxml_file)
            return "{'ok': 'realizado'}"
        except Exception as e:
            print(e)
            return make_response(f'{{ error: "{e}" }}', 500)


jasperutils = JasperUtils()
