from sanic import Sanic
from sanic_cors import CORS, cross_origin

app = Sanic()
CORS(app)
app.static('/', '.')
app.config['CORS_AUTOMATIC_OPTIONS'] = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
