# Trabalho Lesões Vasculares
Este código é referente ao backend do trabalho de doutorado "Sistema inteligente baseado na Lógica Fuzzy para avaliação e tratamento de pessoas com úlceras vasculares crônicas" de Luiz Eduardo Wonsttret e ao TCC "SISTEMA DE APOIO A DECISÃO CLÍNICA PARA O DIAGNÓSTICO DE ÚLCERAS VASCULARES" de Felipe Del Corona Losso.

# Execução
Para inicializar o banco de dados local é preciso rodar o seguinte comando:
```
docker compose up -d
```
Para a execução do sistema é necessário configuras as seguintes variáveis da ambiente:
```
export DB_PORT=<Porta Banco de Dados>
export DB_DATABASE=<Nome Banco de Dados>
export DB_URL=<URL Banco de Dados>
export DB_USER=<Usuário Banco de Dados>
export DB_PASSWORD=<Senha Banco de Dados>
export SECRET=<Senha API>
```

Onde as variáveis que iniciam com db são referentes ao banco de dados e a variável secret é a senha para acessar as URLs expostas.


Antes da inicialização é necessário estar utilizando Python versão 3.9 e rodar o comando:

```
pip install -r requirements.txt
```

Finalmente para execução do sistema basta rodar o seguinte comando:

```
python3.9 app.py
```