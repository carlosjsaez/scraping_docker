from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_restful import Api, Resource
from flasgger import Swagger, LazyString, LazyJSONEncoder

# Config files

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': 3306,
        'database': 'urparts_scraper'
    }

# Api definition

api = Flask(__name__)

api.config['MYSQL_HOST'] = config['host']
api.config['MYSQL_USER'] = config['user']
api.config['MYSQL_PASSWORD'] = config['password']
api.config['MYSQL_DB'] = config['database']
api.config['MYSQL_PORT'] = config['port']

rest = Api(api)

# Swagger Documentation

swagger_config = {
    "version": '1.0',
    "title": "MySQL query API",
    "description": "API REST",
    "termsOfService": "",
    "headers": [],
    "specs": [{
        "endpoint": "api",
        "route": "/api.json"
    }],
    "specs_route": "/",
    "static_url_path": "/flasgger_static",
    "swagger_ui": True
}
api.json_encoder = LazyJSONEncoder
lazy_template = dict(
    host=LazyString(lambda: request.host)
)
swagger = Swagger(api, config=swagger_config, template=lazy_template)

mysql = MySQL(api)

class Consulta(Resource):

        def get(self):
                """
                post endpoint
                ---
                tags:
                  - Flask Restful APIs
                parameters:
                  - name: manufacturer
                    in: query
                    type: string
                    required: false
                    description: name of the product's manufacturer
                  - name: category
                    in: query
                    type: string
                    required: false
                    description: category of the product
                  - name: model
                    in: query
                    type: string
                    required: false
                    description: model of the product
                  - name: part
                    in: query
                    type: string
                    required: false
                    description: part of the product
                  - name: part_category
                    in: query
                    type: string
                    required: false
                    description: category's part of the product
                responses:
                  500:
                    description: Error The query inputs are not strings
                  200:
                    description: Database query output
                    schema:
                      properties:
                        manufacturer:
                            type: string
                            description: name of the product's manufacturer
                        category:
                            type: string
                            description: category of the product
                        model:
                            type: string
                            description: model of the product
                        part:
                            type: string
                            description: part of the product
                        part_category:
                            type: string
                            description: category's part of the product
                """
                try:

                    # Iteration over the allowed parameters to gather them
                    params_raw = ['manufacturer', 'category', 'model', 'part', 'part_category']
                    params = []
                    params_val = []
                    for x in params_raw:
                        new_val = request.args.get(x)
                        if new_val:
                            params_val.append(new_val)
                            params.append(x)

                    # As long as we have at least one input parameter, we must include filters in our query
                    if len(params) > 0:
                        query = f'WHERE ' + ' AND '.join([f'{param} = "{param_val}"' for param_val, param in zip(params_val, params)])
                    else:
                        query = ''
                    cur = mysql.connection.cursor()
                    cur.execute(f'SELECT * from urparts_scraper.parts {query}')

                    # Extraction of data and headers to create the output json
                    results = cur.fetchall()
                    row_headers = [x[0] for x in cur.description]

                    # Output json creation
                    json_data = []
                    for result in results:
                        json_data.append(dict(zip(row_headers, result)))

                    return jsonify(json_data)

                except Exception as e:
                    print(e)

# Resources for the REST API
rest.add_resource(Consulta, '/get')

if __name__ == '__main__':
  api.run(debug=True, host='0.0.0.0')