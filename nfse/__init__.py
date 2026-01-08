import tempfile
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
import requests
import os
import gzip
import base64
from datetime import datetime

__version__ = "0.1.2"

def extract_pem_and_key_from_pfx(pfx_path, password):
    """
    Extrai o certificicado e senha e cria arquivos temporários .pem e .key
    """
    with open(pfx_path, 'rb') as f: 
        pfx_data = f.read()
    
    private_key, certificate, _ = load_key_and_certificates(pfx_data, password.encode())
    
    key_pem = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    cert_pem = certificate.public_bytes(Encoding.PEM)
    
    key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".key", mode='wb')
    cert_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem", mode='wb')
    
    key_file.write(key_pem)
    cert_file.write(cert_pem)
    
    key_file.close()
    cert_file.close()
    
    return cert_file.name, key_file.name


def descompactarZIP(conteudo: str) -> str:
    return gzip.decompress(base64.b64decode(conteudo)).decode("utf8")

def normalizar_cnpj(cnpj: str):
    return cnpj.replace(".", "").replace("-", "").replace("/", "")

def download_nfse(cnpj: str, nsu: int, output_path: str, cert_path: str, cert_password: str):
    """
    Baixa NFSe do Ambiente Nacional (ADN).
    
    Args:
        cnpj (str): CNPJ do contribuinte.
        nsu (int): Número Sequencial Único a partir do qual baixar.
        output_path (str): Diretório onde os arquivos XML serão salvos.
        cert_path (str): Caminho para o arquivo do certificado digital (.pfx).
        cert_password (str): Senha do certificado digital.
        
    Returns:
        str: Mensagem de status da operação.
    """
    cert = None
    key = None
    try:
        cert, key = extract_pem_and_key_from_pfx(cert_path, cert_password)
    except Exception as e:
        return f"Erro ao extrair certificado e chave, verifique o caminho do arquivo e senha. Erro: {e}"

    url = f"https://adn.nfse.gov.br/contribuintes/dfe/{nsu}"
    params = {
        "cnpjConsulta": normalizar_cnpj(cnpj),
        "lote": "true"
    }

    try:
        response = requests.get(url, params=params, cert=(cert, key))
        
        if response.status_code == 200:

            #Parse Requisicao
            data = response.json()
            lotes = data.get("LoteDFe", [])
            
            if not lotes:
                return "Nenhum documento encontrado"
            
            count = 0
            for lote in lotes:
                # nsu_doc = lote['NSU'] 
                chnfse = lote['ChaveAcesso']
                dthora = lote['DataHoraGeracao']
                
                pasta = datetime.fromisoformat(dthora).strftime("%Y.%m")
                dir_path = os.path.join(output_path, pasta)
                os.makedirs(dir_path, exist_ok=True)
                
                filepath = os.path.join(dir_path, f"{chnfse}.xml")
                conteudoXML = descompactarZIP(lote['ArquivoXml'])

                with open(filepath, 'w+', encoding='UTF-8') as f:
                    f.write(conteudoXML)
                count += 1

            return f"{count} documentos baixados com sucesso"
        
        elif response.status_code == 400:
            return f"Erro na requisição {response.text}"
        
        elif response.status_code == 404:
            return "NSU não encontrado"
        
        elif response.status_code == 500:
            return "Erro interno do servidor"
        
        elif response.status_code == 429:
            return "Muitas requisições, aguarde e tente novamente"
        
        else:
            return f"Erro na requisição {response.status_code}"
        

    except Exception as e:
        return f"Erro ao baixar NFSe: {e}"
        

    finally:
        if cert and os.path.exists(cert): 
            try: os.remove(cert)
            except: pass
        if key and os.path.exists(key): 
            try: os.remove(key)
            except: pass
