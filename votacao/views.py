import psycopg2, psycopg2.extras
from flask import g, session, request, redirect, url_for, render_template
from votacao import app

@app.before_request
def before_request():
   g.db = psycopg2.connect("dbname=votacao user=postgres password=sousa123 host=127.0.0.1")

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
        cur.execute("INSERT INTO eleitor (nome, cpf, senha) VALUES (%s, %s, %s)", (nome, cpf, senha))
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


@app.route('/home')
def home():
    return render_template('home.html')



            