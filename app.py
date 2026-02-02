import os
from utils import carregar_info, guardar_info
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.utils import secure_filename
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer


# Define categorias de projetos
CATEGORIAS = ["Pintura", "Escultura", "Mobiliário", "Fotografia", "Papel", "Outros"]

# --- 1. CONFIGURATION & ENV SETUP ---
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'portfolio.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload Settings
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * \
    1024 * 1024  # Limit upload size to 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

db = SQLAlchemy(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'inessambado@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Restauro2026!' # Password de app gerada no Gmail

# mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)


# --- 2. MODELS ---

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)
    video_url = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), default='General')

    def __repr__(self):
        return f'<Project {self.title}>'

# --- 3. HELPERS ---


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 4. ROUTES ---


@app.route('/')
def home():
    from utils import carregar_info
    info = carregar_info()
    trabalhos = Project.query.order_by(Project.id.desc()).all()
    return render_template('index.html', info=info, trabalhos=trabalhos, categorias=CATEGORIAS)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from utils import carregar_info
        info = carregar_info()
        
        # Compara removendo espaços e ignorando maiúsculas no nome
        user_enviado = request.form.get('username', '').strip().lower()
        pass_enviada = request.form.get('password', '').strip()
        
        user_correto = info.get('nome', '').strip().lower()
        pass_correta = info.get('password', '').strip()
        
        if user_enviado == user_correto and pass_enviada == pass_correta:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        
        # Mensagem padrão de erro para o utilizador
        return render_template('login.html', erro="Utilizador ou Password incorretos!")
        
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    trabalhos = Project.query.order_by(Project.id.desc()).all()

    if request.method == 'POST':
        file = request.files.get('imagem')
        titulo = request.form.get('titulo')

        if file and allowed_file(file.filename) and titulo:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            novo_projeto = Project(
                title=titulo,
                description=request.form.get('descricao'),
                image_filename=filename,
                video_url=request.form.get('video_url'),
                # Aqui ele pega o valor selecionado no dropdown
                category=request.form.get('categoria', 'Outros') 
            )

            db.session.add(novo_projeto)
            db.session.commit()
            return redirect(url_for('admin'))

    # ADICIONAMOS 'categorias=CATEGORIAS' no final desta linha:
    return render_template('admin.html', trabalhos=trabalhos, categorias=CATEGORIAS)


@app.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    projeto = Project.query.get_or_404(id)

    # Securely delete the file
    try:
        caminho_img = os.path.join(
            app.config['UPLOAD_FOLDER'], projeto.image_filename)
        if os.path.exists(caminho_img):
            os.remove(caminho_img)
    except Exception as e:
        print(f"Error deleting file: {e}")

    db.session.delete(projeto)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/projeto/<int:id>')
def projeto_detalhe(id):
    projeto = Project.query.get_or_404(id)
    return render_template('projecto.html', projeto=projeto)

@app.route('/editar_info', methods=['GET', 'POST'])
@login_required
def editar_info():
    info = carregar_info()
    if request.method == 'POST':
        # 1. Atualizar campos de texto
        campos = ['nome', 'titulo', 'sobre_mim', 'especialidades', 'formacao', 'email', 'linkedin', 'instagram']
        for campo in campos:
            info[campo] = request.form.get(campo)
        
        # 2. Lógica para o PDF do Currículo
        if 'cv_file' in request.files:
            file = request.files['cv_file']
            if file and file.filename != '':
                if file.filename.lower().endswith('.pdf'):
                    # Usamos um nome fixo para o CV para evitar acumular ficheiros velhos
                    filename = "curriculo_ines_sambado.pdf"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    info['cv_path'] = filename # Guarda o nome no info.json
                else:
                    # Opcional: podias passar uma mensagem de erro aqui se não for PDF
                    "O ficheiro do CV deve ser um PDF."
                    pass 

        # 2.1 Atualizar password se fornecida
        nova_pass = request.form.get('nova_password')
        if nova_pass and nova_pass.strip() != "":
            info['password'] = nova_pass.strip()

        # 3. Guardar tudo no info.json
        if guardar_info(info):
            return redirect(url_for('admin'))
        else:
            return "Erro crítico: Não foi possível escrever no ficheiro info.json. Verifique as permissões no servidor."
            
    return render_template('editar_info.html', info=info)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form.get('email')
        info = carregar_info()
        
        if email == info.get('email'):
            token = s.dumps(email, salt='password-reset-salt')
            link = url_for('reset_token', token=token, _external=True)
            
            msg = Message('Recuperação de Password - Portfólio',
                          sender='o-teu-email@gmail.com',
                          recipients=[email])
            msg.body = f'Para redefinir a sua password, clique no link: {link}'
            mail.send(msg)
            return "Verifique o seu email para o link de recuperação."
            
    return render_template('reset_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    try:
        # O token expira em 1800 segundos (30 minutos)
        email = s.loads(token, salt='password-reset-salt', max_age=1800)
    except:
        return 'O link de recuperação expirou ou é inválido.'

    if request.method == 'POST':
        nova_pass = request.form.get('password')
        # Aqui deves guardar a nova password no teu ficheiro de config ou BD
        # Se usares hash, lembra-te de encriptar!
        return redirect(url_for('login'))

    return render_template('reset_token.html')

# ROTA SECRETA PARA EMERGÊNCIA
# Só tu saberás que este link existe
@app.route('/force-reset-admin-99') 
def force_reset():
    from utils import carregar_info, guardar_info
    info = carregar_info()
    
    # Lê do .env. Se não encontrar, usa uma genérica (ou vice-versa)
    nova_pass = os.getenv('EMERGENCY_RESET_PASSWORD', 'Restauro2026!!') 
    info['password'] = nova_pass
    
    if guardar_info(info):
        return f"✅ Password resetada com sucesso para o valor definido no sistema."
    return "❌ Erro ao guardar."


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Automatically creates the .db file if it doesn't exist
    app.run(debug=True, port=5001)
