import psycopg2, psycopg2.extras
from flask import g, session, request, redirect, url_for, render_template
from votacao import app

@app.before_request
def before_request():
   g.db = psycopg2.connect("dbname=votacao user=postgres password=xuxu21")

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == 'GET'):
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    else:
        nome = request.form['nome']
        cpf = request.form['cpf']
        senha = request.form['password']
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO eleitor (nome, cpf, senha) VALUES ('%s', '%s', '%s')" %(nome, cpf, senha))
        g.db.commit()
        return redirect(url_for('login'))

    #cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("SELECT * FROM genero;")
    #data = cur.fetchall()
    #cur.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        cpf = request.form['cpf']
        senha = request.form['password']
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM eleitor;")
        data = cur.fetchall()
        for x in data:
            if x['cpf'] == cpf and x['senha'] == senha:
                session['name'] = x['nome']
                return redirect(url_for('home'))
            else:
                pass
        return redirect(url_for('login'))

@app.route('/home')
def home():
    if request.method == 'POST':
        return render_template('criarvotacao.html')
    return render_template('home.html')


@app.route('/criarvotacao', methods=['GET', 'POST'])
def criarvotacao():
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM candidato')
    candidatos = cur.fetchall()
    if (request.method == 'POST'):
        nome = request.form['nome']
        descricao = request.form['descricao']
        candidato_um = request.form['candidato']
        candidato_dois = request.form['candidatos']
        periodo = request.form['periodo']
        query = "INSERT INTO eleicao (nome, descricao, candidato1, candidato2, periodo) VALUES ('{}', '{}', {}, {}, '{}')".format(nome, descricao, candidato_um, candidato_dois, periodo)
        cur.execute(query)
        cur.execute("SELECT * FROM eleicao WHERE candidato1 = {} and candidato2 = {}".format(candidato_um, candidato_dois))
        eleicao = cur.fetchone()
        g.db.commit()
        return redirect(url_for('sucesso', id_votacao = eleicao[0]))
    return render_template('criarvotacao.html', candidatos = candidatos)

@app.route('/cadastrocandidato', methods=['GET', 'POST'])
def cadastrocandidato():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        nome1 = request.form['nome1']
        descricao1 = request.form['descricao1']
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO candidato (nome, descricao) VALUES ('%s', '%s')" %(nome, descricao)) 
        cur.execute("INSERT INTO candidato (nome, descricao) VALUES ('%s', '%s')" %(nome1, descricao1)) 
        g.db.commit()
        return redirect(url_for('criarvotacao'))
    return render_template('cadastrocandidato.html')

@app.route('/sucesso/<int:id_votacao>')
def sucesso(id_votacao):
    return render_template('sucesso.html', id_votacao = id_votacao)

@app.route('/testar/<int:id_votacao>')
def testar(id_votacao):
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM eleicao WHERE id = '{}'".format(id_votacao))
    eleicao = cur.fetchone()
    cur.execute("SELECT * FROM candidato WHERE id = '{}'".format(eleicao[3]))
    candidato_um = cur.fetchone()
    cur.execute("SELECT * FROM candidato WHERE id = '{}'".format(eleicao[4]))
    candidato_dois = cur.fetchone()
    if request.method == 'POST':
        pass    
    return render_template('votacao.html', candidato1 = candidato_um, candidato2 = candidato_dois)
