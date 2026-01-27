import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

# 1. Carregar variáveis de ambiente primeiro
load_dotenv()

# 2. Criar a APP 
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# 3. Configuração da Base de Dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'portfolio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. Ligar a DB à APP
db = SQLAlchemy(app) 

# 5. Definir o Modelo
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)
    video_url = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=True)

# --- CONFIGURAÇÕES RESTANTES (Remove a segunda linha app = Flask(__name__)) ---
ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Configurações de Upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- FUNÇÕES DE SUPORTE (BACKEND ROBUSTO) ---

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def carregar_dados():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_dados(dados):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_info():
    default_info = {
        "sobre_mim": "Biografia a ser editada...",
        "email": "ines@exemplo.com",
        "linkedin": "https://linkedin.com/"
    }
    try:
        if os.path.exists('info.json'):
            with open('info.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
                # Garante que chaves novas existem no dicionário
                for k, v in default_info.items():
                    dados.setdefault(k, v)
                return dados
        return default_info
    except Exception:
        return default_info

# --- MIDDLEWARE ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROTAS ---

@app.route('/')
def home():
    info = carregar_info() 
    # Em vez de carregar_dados(), usamos a Query do SQLAlchemy:
    trabalhos = Project.query.all() 
    return render_template('index.html', info=info, trabalhos=trabalhos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', erro="Credenciais inválidas!")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    # Carrega todos os projetos da base de dados (ordenados pelo ID mais recente)
    trabalhos = Project.query.order_by(Project.id.desc()).all()
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        video_url = request.form.get('video_url') # Novo campo
        categoria = request.form.get('categoria', 'Geral')
        file = request.files.get('imagem')

        if titulo and descricao and file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Cria o novo objeto Project para a base de dados
            novo_projeto = Project(
                title=titulo,
                description=descricao,
                image_filename=filename,
                video_url=video_url,
                category=categoria
            )
            
            db.session.add(novo_projeto)
            db.session.commit() # Grava na base de dados
            return redirect(url_for('admin'))
            
    return render_template('admin.html', trabalhos=trabalhos)


@app.route('/editar_info', methods=['GET', 'POST'])
@login_required
def editar_info():
    info = carregar_info()
    if request.method == 'POST':
        info['sobre_mim'] = request.form.get('sobre_mim')
        info['email'] = request.form.get('email')
        info['linkedin'] = request.form.get('linkedin')
        
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=4, ensure_ascii=False)
        return redirect(url_for('admin'))
    return render_template('editar_info.html', info=info)


@app.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    # Procura o projeto na base de dados ou dá erro 404 se não existir
    projeto = Project.query.get_or_404(id)
    
    # 1. Apagar o ficheiro da imagem da pasta uploads
    caminho_img = os.path.join(app.config['UPLOAD_FOLDER'], projeto.image_filename)
    if os.path.exists(caminho_img):
        os.remove(caminho_img)
    
    # 2. Apagar o registo da base de dados
    db.session.delete(projeto)
    db.session.commit()
    
    return redirect(url_for('admin'))

@app.route('/projeto/<int:id>')
def projeto_detalhe(id):
    projeto = Project.query.get_or_404(id)
    # Mudança de 'projeto.html' para 'projecto.html'
    return render_template('projecto.html', projeto=projeto)


if __name__ == '__main__':
    app.run(debug=True)