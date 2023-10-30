from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from flask import jsonify, request
from flask_jwt_extended import JWTManager

from resources.start import Start

import os
from dotenv import load_dotenv


from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

load_dotenv()


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv(
    "JWT_SECRET_KEY")  # Chave de autenticação JWT
CORS(app)


api = Api(app)

jwt = JWTManager(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='API CONTROLE FINANCEIRO',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/documentacao/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)


@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return {'message': 'Você foi desconectado.'}, 401  # unauthorized


api.add_resource(Start, "/")
docs.register(Start)

# Main Function
if __name__ == '__main__':
    print("API PYTHON INICIADA")
    app.run(host='0.0.0.0', port=5001, debug=True)