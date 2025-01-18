# cibersecurity-desafio-ransomware
Repositório para desafio final de entendimento de um ransomware utilizando Python


Esse desafio exigia o uso de códigos disponibilizados pela DIO para simular um ransowmware.  Foram disponibilizados códigos para encriptar e desencriptar um arquivo, passando o nome do arquivo dentro do código, em dois scripts distintos, um para cada ação.

Então, eu me baseei nesses códigos, mas preferi evoluir com as seguintes mudanças:
1) ser um script apenas;
2) ao invés de fazer a ação em um arquivo, fazer em todos os arquivos de um caminho.   E ainda indicar se seria recursivo ou não com os subdiretórios dentro do caminuo;
3) colocar as informações do caminho, da recursvidade e da chave simétrica de criptografia em um arquivo xml de configuração.

Com isso, gerei os arquivos desafioDioRansomware.py e config.xml, que estão nesse repositório.

Na imagem abaixo, podemos ver o passo a passo de utilização do script:
![Captura de tela 2025-01-18 204337](https://github.com/user-attachments/assets/4a52a7c7-4708-4b22-a00f-b5cc3d99b8c4)
