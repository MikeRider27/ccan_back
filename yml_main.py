import os
import sys

import yaml
from flask import current_app, request
from sqlalchemy import text

from db import db


class YmlMain:
    yml_path = ''
    data = []

    def __init__(self, yml_path):
        self.yml_path = os.path.join(current_app.root_path, yml_path)
        self.load_data()

    def load_data(self):
        stream = open(self.yml_path, 'r', encoding='utf8')
        self.data = yaml.load(stream, Loader=yaml.FullLoader)

    def get_key_data(self, key):
        ret = None
        first = True
        for k in key.split('.'):
            if first:
                ret = self.data[key.split('.')[0]]
                first = False
            else:
                ret = ret[k]
        return ret

    def get_result(self, key, params=None, as_dict=False, datasource=None):
        if params is None:
            params = {}

        query = self.get_key_data(key)
        if 'show_pagination' in params and params['show_pagination']:
            query = str(query) + ' OFFSET :offset LIMIT :limit'

        native_sql = text(query)

        if datasource:
            with db.get_engine(bind=datasource).connect() as connection:
                results = connection.execute(native_sql, params)
        else:
            results = db.engine.execute(native_sql, params)

        results = results.fetchall()

        if as_dict:
            results = [r._asdict() for r in results]

        return results

    def get_single_result(self, key, params=None, as_dict=False, datasource=None):
        if params is None:
            params = {}

        query = self.get_key_data(key)

        native_sql = text(query)

        if datasource:
            with db.get_engine(bind=datasource).connect() as connection:
                results = connection.execute(native_sql, params)
        else:
            results = db.engine.execute(native_sql, params)

        result = results.fetchone()

        if as_dict:
            return result._asdict()

        return result

    def get_list(self, query_key: str, params: dict = None, query_filter: str = '', sort_conv: dict = None):

        # Ajuste de parametros
        if params is None:
            params = {}

        if sort_conv is None:
            sort_conv = {}

        query_parts = self.get_key_data(query_key)

        # Ensamblar la consulta SELECT principal
        query = f"{query_parts['select_clause']}{query_parts['from_clause']}{query_parts['joins_clause']}"

        # Filters
        if query_filter:
            query += f"WHERE {query_filter}\n"

        # SubQuery para total
        subquery_for_total = query

        # Sort
        sort_by = request.args.get('sortBy', None, str)
        descending = request.args.get('descending', 'false', str) == 'true'
        if sort_by:
            sort_by = sort_conv.get(sort_by) if sort_conv.get(sort_by, None) else sort_by
            query += f"ORDER BY {sort_by} {'DESC' if descending else 'ASC'}\n"

        # Pagination, por defecto se pagina
        pagination = request.args.get('pagination', 'true', str) == 'true'
        if pagination:
            # Si la paginación está habilitada, agregamos LIMIT y OFFSET
            query += f"{query_parts['pagination_clause']}"

            # Se obtiene parametros de paginacion
            per_page = request.args.get('rowsPerPage', None, int)
            per_page = sys.maxsize if per_page == 0 else per_page
            page = request.args.get('page', 1, int)

            # Se calcula el offset basado en la página actual y el número de resultados por página
            offset = (page - 1) * per_page

            # Se ajusta parametros de paginacion para query
            params['per_page'] = per_page
            params['offset'] = offset

            # Ejecutamos la consulta con paginación
            native_sql = text(query)
            results = db.engine.execute(native_sql, params)
            results = results.fetchall()
            results = [r._asdict() for r in results]

            response = {
                'page': page,
                'pages': 10,
                'per_page': per_page,
                'items': results
            }

            # Total
            # Ensamblar la consulta Total
            query = f"SELECT COUNT(*) AS total FROM ({subquery_for_total}) t"
            native_sql = text(query)
            results = db.engine.execute(native_sql, params)
            results = results.fetchone()
            results = results._asdict()
            response['total'] = results.get('total', 0)
        else:
            # Ejecutamos la consulta son paginación
            native_sql = text(query)
            results = db.engine.execute(native_sql, params)
            results = results.fetchall()
            response = [r._asdict() for r in results]

        return response
