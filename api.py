import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource


app = Flask(__name__)
api = Api(app, version='1.0', title='Your API', description='API Description')


ns = api.namespace('your_namespace', description='Your API operations')
@ns.route('/your_endpoint')
class YourResource(Resource):
    @ns.doc('your_get_endpoint')
    def get(self):
        """Your GET operation description here."""
        return {'message': 'GET operation response'}
    
connect = os.getenv('CONNECTION')
app.config['SQLALCHEMY_DATABASE_URI'] = connect
db = SQLAlchemy(app)

"ID", "nome", "idade", "nota do primeiro semestre", "nota do segundo semestre", "nome do professor", "número da sala"
class Alunos(db.Model):
    __tablename__ = 'alunos'

    ID = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    idade = db.Column(db.Integer)
    nota1 = db.Column(db.Float(precision=2))
    nota2 = db.Column(db.Float(precision=2))
    nome_professor = db.Column(db.String(255))
    numero_sala = db.Column(db.Integer)


@app.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Alunos.query.all()
    aluno_list = []
    for aluno in alunos:
        aluno_data = {
            'ID': aluno.ID,
            'nome': aluno.nome,
            'idade': aluno.idade,
            'nota do primeiro semestre': float(aluno.nota1),
            'nota do segundo semestre': float(aluno.nota2),
            'nome do professor': aluno.nome_professor,
            'número da sala': aluno.numero_sala
        }
        aluno_list.append(aluno_data)
    return jsonify({'alunos': aluno_list}), 200


@app.route('/alunos/<int:aluno_id>', methods=['GET'])
def get_aluno(aluno_id):
    try:
        aluno = Alunos.query.get(aluno_id)
    
        aluno_data = {
            'ID': aluno.ID,
            'nome': aluno.nome,
            'idade': aluno.idade,
            'nota do primeiro semestre': float(aluno.nota1),
            'nota do segundo semestre': float(aluno.nota2),
            'nome do professor': aluno.nome_professor,
            'número da sala': aluno.numero_sala
        }
        return jsonify(aluno_data), 200
    except:
        return jsonify({'error':'Aluno not found'}), 404
    

@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    try:
        nome = data['nome']
        idade = data['idade']
        nota1 = data['nota do primeiro semestre']
        nota2 = data['nota do segundo semestre']
        nome_professor = data['nome do professor']
        numero_sala = data['número da sala']
        new_aluno = Alunos(nome=nome, idade=idade, nota1=nota1, nota2=nota2, nome_professor=nome_professor, numero_sala=numero_sala)
        db.session.add(new_aluno)
        db.session.commit()
        return jsonify(new_aluno), 201
    except:
        return jsonify({'error': 'Bad Request'}), 400


@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.get_json()
    try:
        nome = data['nome']
        idade = data['idade']
        nota1 = data['nota do primeiro semestre']
        nota2 = data['nota do segundo semestre']
        nome_professor = data['nome do professor']
        numero_sala = data['número da sala']
        aluno = Alunos.query.get(aluno_id)
        if aluno:
            aluno.nome = nome
            aluno.idade = idade
            aluno.nota1 = nota1
            aluno.nota2 = nota2
            aluno.nome_professor = nome_professor
            aluno.numero_sala = numero_sala
            db.session.commit()
            return jsonify(aluno), 200
        else:
            return jsonify({'error': 'Aluno not found'}), 404
    except:
        return jsonify({'error': 'Bad Request'}), 400


@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    aluno = Alunos.query.get(aluno_id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Aluno not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)