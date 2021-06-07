import pymysql
from app import app
from config import mysql, auth
from flask import jsonify, Response
from flask import flash, request
from contextlib import closing
import requests

a = open("/home/ubuntu/lb.txt", "r")
lb_endpoint = f'http://{str(a.read()).strip}'
a.close()

basic_auth = auth

#Criando as Rotas API para a Tabela Cliente_compra_curso
@app.route('/compras/produtos', methods = ['POST'])
@basic_auth.required
def add_comprar_produtos():
	try:
		_json = request.get_json(force = True)
		_id = _json['id']
		_data = _json['data']
		_idCliente = _json['idCliente']
		_idCurso = _json['idCurso']
		if _id and _data and _idCliente and _idCurso and request.method == 'POST':
			sqlQuery = "INSERT INTO vendas.vendas(id, data, idCliente, idCurso) VALUES(%s, %s, %s, %s)"
			bindData = (_id, _data, _idCliente, _idCurso)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)

			# Verificação se o Id do cliente confere com o db_clientes
			cliente = requests.get(f'http://lb_endpoint/clientes/{_idCliente}', headers = {"Authorization":"Basic YWxlOjI1NjgzMzk0QEd1"})
			curso = requests.get(f'http://lb_endpoint/produtos/{_idCurso}', headers = {"Authorization":"Basic YWxlOjI1NjgzMzk0QEd1"})

			if cliente.status_code == 404:
				return ('Cliente não encontrado'), 400
			elif curso.status_code == 404:
				return ('Curso não encontrado'), 400 

			status = curso.json()['ativo']
			if status == 'N':
				return ('Produto indisponível, compra não cadastrada!'), 404
			elif status  == 'S':
				cursor.execute(sqlQuery, bindData)
				conn.commit()
				response = jsonify('Compra adicionado com sucesso!')
				response.status_code = 200
				return response
		else:
			return not_found()
	except Exception as error:
		return error, 500
	finally:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.close()
		conn.close()

@app.route('/compras/produtos/<int:idCliente>', methods =['GET'])
@basic_auth.required
def compras_pesquisar_id(idCliente):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT id, data, idCliente, idCurso FROM vendas.vendas WHERE idCliente = %s", idCliente)
		
		userRows = cursor.fetchall()
		if not userRows:
			return Response('Compra não encontrado', status = 404)
		
		curso = [] #lista de json dos vários cursos comprados por um cliente
		cliente = requests.get(f'http://lb_endpoint/clientes/{idCliente}', headers = {"Authorization":"Basic YWxlOjI1NjgzMzk0QEd1"})
		for i in userRows:

			c = requests.get(f'http://lb_endpoint/produtos/{i["idCurso"]}', headers = {"Authorization":"Basic YWxlOjI1NjgzMzk0QEd1"})
			
			i['data'] = f"{i['data']}"
			curso.append(c.json())
			
			response = jsonify(userRows, cliente.json(), curso)
			response.status_code = 200
			return response

	except Exception as e:
		return jsonify({"Error":f"{e}"}), 500
	finally:
		cursor.close() 
		conn.close()

@app.route('/compras/produtos', methods = ['GET'])
@basic_auth.required
def compras_produtos():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute('SELECT id, DATE_FORMAT(data,"%Y-%m-%d") as data, idCliente, idCurso FROM vendas.vendas')
		userRows = cursor.fetchall()
		response = jsonify(userRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/compras/produtos/<int:id>', methods=['PUT'])
@basic_auth.required
def update_compras_produtos(id):
	try:
		_json = request.get_json(force = True)
		_id = _json['id']
		_data = _json['data']
		_idCliente = _json['idCliente']
		_idCurso = _json['idCurso']
		if  _data and _idCliente and _idCurso and _id and request.method == 'PUT':
			sqlQuery = "SELECT * FROM vendas.vendas WHERE id=%s"
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, id)
			select = cursor.fetchone()
			if not select:
				return Response('Compra não cadastrada', status=400)
			sqlQuery = "UPDATE vendas.vendas SET data=%s, idCliente=%s, idCurso=%s, id=%s WHERE id=%s"
			bindData = (_data, _idCliente, _idCurso, _id, id)
            # Verificação se o Id do cliente confere com o db_clientes
			cliente = requests.get(f'http://lb_endpoint/clientes/{_idCliente}', headers = {"Authorization":"Basic YWxlOjI1NjgzMzk0QEd1"})
			curso = requests.get(f'http://lb_endpoint/produtos/{_idCurso}', headers = {"Authorization":"Basic YWxlOjI1NjgzMzk0QEd1"})

			if cliente.status_code == 404:
				return ('Cliente não encontrado'), 400
			elif curso.status_code == 404:
				return ('Curso não encontrado'), 400
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			response = jsonify('Dados alterados com sucesso!')
			response.status_code = 200
			return response
		else:
			return not_found()

	except Exception as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

@app.route('/compras/produtos/<int:id>', methods=['DELETE'])
@basic_auth.required
def delete_cursos(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM vendas.vendas WHERE id = %s", id)
		conn.commit()
		response = jsonify('Employee deleted successfully!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
@basic_auth.required
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True, host= "0.0.0.0", port=80)