import os
from utils import carregar_info, guardar_info
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.utils import secure_filename
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

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
    # Keep using your info.json for the bio/contacts for now
    # Move JSON logic to a separate util file if possible
    from utils import carregar_info
    info = carregar_info()
    trabalhos = Project.query.order_by(Project.id.desc()).all()
    return render_template('index.html', info=info, trabalhos=trabalhos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == os.getenv('ADMIN_USER') and \
           request.form['password'] == os.getenv('ADMIN_PASSWORD'):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', erro="Invalid Credentials!")
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

        # 3. Guardar tudo no info.json
        if guardar_info(info):
            return redirect(url_for('admin'))
            
    return render_template('editar_info.html', info=info)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Automatically creates the .db file if it doesn't exist
    app.run(debug=True, port=5001)
