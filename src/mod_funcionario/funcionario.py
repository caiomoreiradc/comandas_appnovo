from flask import Blueprint, render_template, request, redirect, url_for
import requests
from funcoes import Funcoes
from settings import HEADERS_API, ENDPOINT_FUNCIONARIO
from mod_login.login import validaSessao
bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

''' rotas dos formulários '''
@bp_funcionario.route('/', methods=['GET', 'POST'])
@validaSessao
def formListaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        return render_template('formListaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/form-funcionario/', methods=['GET'])
def formFuncionario():
    return render_template('formFuncionario.html')
@validaSessao
def formFuncionario():
  return render_template('formFuncionario.html')

@bp_funcionario.route('/insert', methods=['POST'])
@validaSessao
def insert():
    try:
        # dados enviados via FORM
        id_funcionario = 1
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.cifraSenha(request.form['senha'])
        # monta o JSON para envio a API
        payload = {'id_funcionario': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=HEADERS_API, json=payload)
        
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])