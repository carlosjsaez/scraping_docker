from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_restful import Api, Resource
from flasgger import Swagger, LazyString, LazyJSONEncoder
import json

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': 3306,
        'database': 'urparts_scraper'
    }

api = Flask(__name__)

api.config['MYSQL_HOST'] = config['host']
api.config['MYSQL_USER'] = config['user']
api.config['MYSQL_PASSWORD'] = config['password']
api.config['MYSQL_DB'] = config['database']
api.config['MYSQL_PORT'] = config['port']


rest = Api(api)

swagger_config = {
    "version": '1.0',
    "title": "Data Scrapping",
    "description": "Proyecto API REST",
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

class consulta(Resource):
        # @api.route('/', methods = ['GET'])
        def get(self, params = 'test'):
                """
                post endpoint
                ---
                tags:
                  - Flast Restful APIs
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
                    description: Error The quuery inputs are not strings
                  200:
                    description: Database query output
                    schema:
                      id: stats
                      properties:
                        sum:
                          type: integer
                          description: The sum of number
                        product:
                          type: integer
                          description: The sum of number
                        division:
                          type: integer
                          description: The sum of number
                """
                print(params)
                try:
                    params_raw = ['manufacturer', 'category', 'model', 'part', 'part_category']
                    params = []
                    params_val = []
                    for x in params_raw:
                        new_val = request.args.get(x)
                        if new_val:
                            params_val.append(new_val)
                            params.append(x)
                    if len(params) > 0:
                        query = f'WHERE ' + ' AND '.join([f'{param} = "{param_val}"' for param_val, param in zip(params_val, params)])
                    else:
                        query = ''
                    cur = mysql.connection.cursor()
                    cur.execute(f'SELECT * from urparts_scraper.parts {query}')
                    results = cur.fetchall()
                    res = jsonify({'status': 'Query succesful', 'json_data': json.dumps(results)})
                    return res

                except Exception as e:
                    print(e)

rest.add_resource(consulta, '/get')

if __name__ == '__main__':
  api.run(debug=True, host='0.0.0.0')