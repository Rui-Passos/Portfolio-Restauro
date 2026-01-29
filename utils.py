import json
import os

# Define o caminho para o ficheiro de informações (biografia, contactos)
INFO_FILE = 'info.json'

def carregar_info():
    default_info = {
        "nome": "Inês",
        "titulo": "Conservadora-Restauradora",
        "sobre_mim": "Biografia a ser editada...",
        "especialidades": "Pintura, Talha, Mobiliário",
        "formacao": "Licenciatura em Conservação e Restauro",
        "email": "exemplo@email.com",
        "linkedin": "https://linkedin.com/",
        "instagram": "https://instagram.com/"
    }
    
    try:
        if os.path.exists(INFO_FILE):
            with open(INFO_FILE, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                # Garante que chaves novas existem no dicionário (Merge)
                for k, v in default_info.items():
                    dados.setdefault(k, v)
                return dados
        return default_info
    except (json.JSONDecodeError, IOError) as e:
        print(f"Erro ao ler {INFO_FILE}: {e}")
        return default_info

def guardar_info(dados):
    """
    Guarda as informações atualizadas no ficheiro JSON.
    """
    try:
        with open(INFO_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Erro ao guardar {INFO_FILE}: {e}")
        return False