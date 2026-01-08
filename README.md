# NFSe Nacional

Biblioteca Python para baixar Notas Fiscais de Serviço Eletrônicas (NFSe) do Ambiente de Dados Nacional (ADN).

## Instalação

Você pode instalar a biblioteca via PyPI:

```bash
pip install dfe-nfse
```

## Uso

Para utilizar a biblioteca, você precisa de um certificado digital A1 (.pfx) e sua respectiva senha.

```python
from nfse import download_nfse

cnpj = "00000000000000"
nsu = 100 
output_path = "./notas" 
cert_path = "/caminho/para/seu/certificado.pfx"
cert_password = "sua_senha_aqui"

resultado = download_nfse(
    cnpj=cnpj, 
    nsu=nsu, 
    output_path=output_path, 
    cert_path=cert_path, 
    cert_password=cert_password
)

print(resultado)
```

## Requisitos

- Python 3.6+
- requests
- cryptography

## Estrutura

Os arquivos XML baixados serão organizados em pastas por ano e mês (ex: `2024.01`) dentro do diretório de saída especificado.

## Licença

MIT
