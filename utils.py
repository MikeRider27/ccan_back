import logging
import os
import pathlib
import sys
import time
import datetime
import decimal
import hashlib

import pandas as pd
import numpy as np
from io import BytesIO

from dateutil.relativedelta import relativedelta
from flask import request, current_app, send_file
from flask.json import JSONEncoder, JSONDecoder
# Define custom JSONEncoder for the ISO Datetime format
from flask_restful.reqparse import Namespace
from json.decoder import WHITESPACE

from sqlalchemy import or_, and_, func, text, desc
from sqlalchemy.engine import Row


class JSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            elif isinstance(obj, decimal.Decimal):
                return float(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class JSONDecoder(JSONDecoder):
    unicode_replacements = {
        '\u2018': "'", '\u2019': "'"
    }

    def __init__(self, *args, **kwargs):
        self.orig_obj_hook = kwargs.pop("object_hook", None)
        super(JSONDecoder, self).__init__(*args, object_hook=self.custom_obj_hook, strict=False, **kwargs)

    def decode(self, s, _w=WHITESPACE.match):
        for rk in self.unicode_replacements.keys():
            s = s.replace(rk, self.unicode_replacements.get(rk))
        # if max(s) > u'\u00FF':
        #     print(f'Unicode out of range in {s.index(max(s))}. Deleting that character and continuing')
        return super().decode(s, _w)

    def custom_obj_hook(self, dct):
        # Calling custom decode function:4
        if self.orig_obj_hook:  # Do we have another hook to call?
            return self.orig_obj_hook(dct)  # Yes: then do it
        return dct  # No: just return the decoded dict


# return a long representations of the current time in milliseconds
def current_time_milliseconds():
    return int(round(time.time() * 1000))


# Generate a 'unique' md5 hash adding the current time in milliseconds
# to a string
def unique_md5(string: str):
    m = hashlib.md5()
    m.update(f'{current_time_milliseconds()}{string}'.encode())
    return m.hexdigest()


# Utility function to only execute and assigment to an object if the value from a reqparse.Namespace dict is not None
def _assign_if_something(obj: object, newdata: Namespace, key: str, with_none=False):
    value = newdata.get(key)

    if with_none:
        obj.__setattr__(key, value)
    else:
        # Assign value only if not None
        if value is not None:
            obj.__setattr__(key, value)


# Apply filter restrictions
def restrict(query, filters, name, condition):
    f = filters.get(name)
    if f:
        query = query.filter(condition(f))
    return query


def restrict_collector(filter_list, filters, name, condition):
    f = filters.get(name)
    if f:
        filter_list.append(condition(f))
    return filter_list


def apply_filters(query, filter_list):
    multiple = request.args.get('multiple', False, bool)
    if multiple:
        return query.filter(or_(*filter_list))
    return query.filter(and_(*filter_list))


# Encrypt password
def sha1_pass(text: str):
    m = hashlib.sha1()
    m.update(text.encode('utf-8'))
    d = m.digest()
    t = ''
    for aux in d:
        c: int = aux & 0xff
        hs = '{:02x}'.format(c)
        t += hs
    return t


def paginated_results(query, sort=True, is_patient=False, depth=1):
    # Sorting (simple columns on model)
    key = current_app.config['ENCRYPTION_KEY']

    if sort:
        sort_by = request.args.get('sortBy', None, str)
        if sort_by:
            descending = request.args.get('descending', 'false', str)
            # Verificar encriptacion de Paciente
            if is_patient and (sort_by == 'firstname' or sort_by == 'lastname' or sort_by == 'documents_number'):
                sort = '%s %s' % (f"decrypt_data({sort_by}, '{key}')", 'desc' if descending == 'true' else 'asc')
            else:
                sort = '%s %s' % (sort_by, 'desc' if descending == 'true' else 'asc')
            query = query.order_by(text(sort))

    # Pagination
    pagination = request.args.get('pagination', 'true', str)
    jsondepth = request.args.get('jsondepth', depth, int)
    if pagination == 'true':
        per_page = request.args.get('rowsPerPage', None, int)
        per_page = sys.maxsize if per_page == 0 else per_page  # Cero is evaluated to None, Max items take 1000 items
        paginated = query.paginate(page=request.args.get('page', 1, int), per_page=per_page)
        # Se reduce al primer elemento de una tupla en caso de agregar columnas en distincts
        items = paginated.items
        if len(items) > 0:
            row = items[0]
            if isinstance(row, Row):
                items = list(map(lambda x: x[0], items))
        return {
            'page': paginated.page,
            'pages': paginated.pages,
            'per_page': paginated.per_page,
            'total': query.count(),
            'items': [x.json(jsondepth) if jsondepth else x.json() for x in items]
        }
    else:
        items = query.all()
        # Se reduce al primer elemento de una tupla en caso de agregar columnas en distincts
        if len(items) > 0:
            row = items[0]
            if isinstance(row, Row):
                items = list(map(lambda x: x[0], items))
        return [x.json(jsondepth) if jsondepth else x.json() for x in items]


def get_filename_hash(filename):
    date = datetime.datetime.now()
    filename_split = filename.split('.')
    filename_hash = "{}_{}".format(''.join(filename_split[:-1]), date.strftime("%Y%m%d_%H%M%S_%f"))
    if len(filename_split) > 1:
        filename_hash += "." + filename_split[-1]
    return filename_hash


def get_file_directory(module, date_path=True):
    if not date_path:
        path_string = str(os.path.join(current_app.config['UPLOAD_FOLDER'], module))
        return create_or_get_path(path_string)

    date = datetime.datetime.now()
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    path_string = str(os.path.join(current_app.config['UPLOAD_FOLDER'], module, year, month, day))
    return create_or_get_path(path_string)


def check_length_path(path):
    if len(path) > current_app.config['MAX_PATH_LENGTH']:
        diference = len(path) - current_app.config['MAX_PATH_LENGTH']
        filename_split = path.split('_')
        filename_split[-4] = filename_split[-4][:-diference]
        path = '_'.join(filename_split)
    return path


def create_or_get_path(path_string):
    path = pathlib.Path(path_string)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    return str(path)


def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


def decrypt_data(value, secret_key):
    return func.decrypt_data(value, secret_key)


def get_encrypt_db(db=None, data=None, key=None):
    native_sql = f"SELECT encrypt_data('{data}', '{key}') as encrypt"
    result = db.engine.execute(native_sql)
    result_row = result.fetchone()
    return result_row[0]


def sorting_relationship_type(request, query, column):
    descending = request.args.get('descending', 'false', str)
    if descending == 'true':
        query = query.order_by(desc(column))
    else:
        query = query.order_by(column)
    return query


def sorting_relationship_type_by_two_columns(request, query, column, column2):
    descending = request.args.get('descending', 'false', str)
    if descending == 'true':
        query = query.order_by(desc(column), desc(column2))
    else:
        query = query.order_by(column, column2)
    return query


def check_business_day(date):
    if date.weekday() == 5:
        date += datetime.timedelta(days=2)
    if date.weekday() == 6:
        date += datetime.timedelta(days=1)

    return date


def get_treatment_plan_dates(date_first_cycle, periodicity, number_sessions, db=None, treatment_plan=None):
    date_cycle = date_first_cycle
    dates = [date_cycle.strftime("%d/%m/%Y") if date_cycle else None]

    for _ in range(number_sessions - 1):
        if periodicity.code == 'DAILY':
            date_cycle += relativedelta(days=1)
        if periodicity.code == 'WEEKLY':
            date_cycle += relativedelta(days=7)
        if periodicity.code == 'BIWEEKLY':
            date_cycle += relativedelta(days=15)
        if periodicity.code == '21_DAYS':
            date_cycle += relativedelta(days=21)
        if periodicity.code == 'MONTHLY':
            date_cycle += relativedelta(months=1)
        if periodicity.code == 'QUARTERLY':
            date_cycle += relativedelta(months=3)
        if periodicity.code == 'BIANNUAL':
            date_cycle += relativedelta(months=6)
        if periodicity.code == 'ANNUAL':
            date_cycle += relativedelta(years=1)

        date_cycle = check_business_day(date_cycle)
        dates.append(date_cycle.strftime("%d/%m/%Y") if date_cycle else None)

    plan = {
        'date_last_cycle': dates[-1],
        'dates': dates
    }

    if db and treatment_plan:
        treatment_plan_id = treatment_plan.id
        native_sql = None
        if treatment_plan.type_treatment.code == 'CHEMOTHERAPY':
            native_sql = text("""SELECT ch.id, ch.date, ctp.num_session, session.value AS session_state
                                    FROM chemotherapy ch
                                             JOIN parameter session ON ch.session_state_id = session.id
                                             JOIN chemotherapy_treatment_plan ctp ON ch.id = ctp.chemotherapy_id
                                    WHERE ctp.treatment_plan_id = :treatment_plan_id
                                    ORDER BY ch.date_create ASC""")

        if treatment_plan.type_treatment.code == 'RADIOTHERAPY':
            native_sql = text("""SELECT rad.id, rad.date, rtp.num_session, session.value AS session_state
                                    FROM radiotherapy rad
                                             JOIN parameter session ON rad.session_state_id = session.id
                                             JOIN radiotherapy_treatment_plan rtp ON rad.id = rtp.radiotherapy_id
                                    WHERE rtp.treatment_plan_id = :treatment_plan_id
                                    ORDER BY rad.date_create ASC""")

        if native_sql != None:
            result = db.engine.execute(native_sql, {'treatment_plan_id': treatment_plan_id})
            results = result.fetchall()
            sessions = []
            count = 0
            realized = 0
            for date in dates:
                result = None
                if count < len(results):
                    result = results[count]
                data = {
                    'plan_date': date,
                    'plan_nro': count + 1
                }
                if result:
                    data['session_date'] = result[1].strftime("%d/%m/%Y") if date_cycle else None
                    data['session_nro'] = result[2]
                    data['session_state'] = result[3]
                    realized += 1

                sessions.append(data)
                count += 1

            try:
                plan['sessions'] = sessions
                plan['realized'] = f"{realized}/{len(dates)}"
                plan['next_session_number'] = realized+1 if realized+1 <= len(dates) else 'Finalized'
                plan['next_session_date'] = dates[realized] if realized+1 <= len(dates) else 'Finalized'
                plan['type_treatment'] = treatment_plan.type_treatment.description
                plan['treatment_plan_number'] = treatment_plan.number
            except Exception as error:
                logging.error(f"An error occurred while obtaining treatment plan dates. Details: {error}. Treatment plan: {treatment_plan.json()}")

    return plan


def log_interoperability(operacion, origen, data):
    try:
        # Variables
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        message = f"""
        -------------------------------------------------------------------------
        Fecha y Hora: {current_datetime}
        Operacion: {operacion}
        Origen: {origen}
        Registrar en CCAN el siguiente payload
        Datos: {data}
        -------------------------------------------------------------------------
        """
        logging.info(message)
    except Exception as err:
        logging.error(f"An error occurred while generating Interoperability log. Detail: {err.__cause__}")


def log_duration_execution(task_name, duration_seg):
    # Convertir la duración a horas, minutos y segundos
    hours = duration_seg // 3600
    minutes = (duration_seg % 3600) // 60
    seconds = duration_seg % 60

    logging.info(
        f"Execution duration of process {task_name}: {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds")


def validate_json_parser(parser, json_data):
    # Crear un diccionario de argumentos validados
    validated_data = {}
    for arg in parser.args:
        name = arg.name
        if name in json_data:
            value = json_data[name]
            if arg.type is not None:
                try:
                    if callable(arg.type) and value == '':
                        value = None
                    if value:
                        value = arg.type(value)
                except ValueError:
                    raise ValueError(f"Invalid value for {name}: {value}")
            validated_data[name] = value
        elif arg.required:
            raise ValueError(f"Missing required argument: {name}")
    return validated_data


def get_report_from_pandas(report_data_list):
    if not report_data_list:
        return None

    # Guarda el DataFrame en un archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for report_data in report_data_list:
            data = report_data.get('data')
            name = report_data.get('name')
            if data:
                # Convertir `rowResults` a un DataFrame de Pandas
                df = pd.DataFrame(data)
                df.to_excel(writer, index=False, sheet_name=name)

                df.replace([np.nan, np.inf, -np.inf], '', inplace=True)

                # Acceder al libro y a las hojas para aplicar estilos
                workbook = writer.book
                worksheet1 = writer.sheets[name]

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
                worksheet1.write_row(0, 0, df.columns, header_format)

                # Aplicar estilos a las celdas
                for row_num in range(1, len(df)+1):
                    worksheet1.write_row(row_num, 0, df.iloc[row_num - 1], cell_format)

    # Configura el puntero al principio del archivo
    output.seek(0)

    # Envía el archivo Excel al usuario
    return send_file(output, attachment_filename="reporte.xlsx", as_attachment=True)


def parse_date(date_string):
    if not date_string:
        return None

    try:
        # Intentar convertir solo con el formato de fecha
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except Exception as error:
        try:
            # Si falla, intentar convertir con formato de fecha y hora
            date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        except Exception as error:
            date = None

    return date
