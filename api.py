from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_pg_user:your_pg_password@your_pg_host/your_database_name'

db = SQLAlchemy(app)

# Task model
class Alunos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)

# Route to get all tasks (GET request)
@app.route('/alunos', methods=['GET'])
def get_tasks():
    alunos = Alunos.query.all()
    aluno_list = [{'id': aluno.id, 'title': aluno.title} for aluno in alunos]
    return jsonify({'alunos': aluno_list})

# Route to create a new task (POST request)
@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    if 'title' in data:
        title = data['title']
        new_aluno = Alunos(title=title)
        db.session.add(new_aluno)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'})
    else:
        return jsonify({'error': 'Title is required'}), 400

# Route to update an existing task (PUT request)
@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.get_json()
    if 'title' in data:
        title = data['title']
        aluno = Alunos.query.get(aluno_id)
        if aluno:
            aluno.title = title
            db.session.commit()
            return jsonify({'message': 'Task updated successfully'})
        else:
            return jsonify({'error': 'Task not found'}), 404
    else:
        return jsonify({'error': 'Title is required'}), 400

# Route to delete a task (DELETE request)
@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    aluno = Alunos.query.get(aluno_id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)