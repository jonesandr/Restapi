Here's the modified code with compatible wording:

```python
from flask import Flask, request
import redis
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/api', methods=['GET'])
def get_all():
    palabras = []
    for i in r.keys():
        palabras.append({
            'nombre': i.decode('UTF-8'),
            'significado': r.get(i).decode('UTF-8')
        })
    return {'palabras': palabras}

@app.route('/api', methods=['POST'])
def create():
    r.set(request.json['nombre'], request.json['significado'])
    return request.json

@app.route('/api/<nombre>', methods=['GET'])
def get(nombre):
    if r.get(nombre):
        return {
            'nombre': nombre,
            'significado': r.get(nombre).decode('UTF-8')
        }
    return {'mensaje': 'La palabra no esta registrada!'}

@app.route('/api/<nombre>', methods=['PATCH'])
def update(nombre):
    r.set(nombre, request.json['significado'])
    return {
        'nombre': nombre,
        'significado': request.json['significado']
    }

@app.route('/api/<nombre>', methods=['DELETE'])
def delete(nombre):
    if r.get(nombre):
        significado = r.get(nombre).decode('UTF-8')
        r.delete(nombre)
        return {
            'nombre': nombre,
            'significado': significado
        }
    return {'mensaje': 'La palabra no esta registrada!'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```
