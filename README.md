<h1 align="center">Comparação eficiência PostgreSQL</h1>

<p align="center">
  <p align="center">Comparação de SGBDs para um TCC</p>
  <a href="#-como-instalar">Como instalar</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-como-executar">Como executar</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
</p>

## 🤓 Como instalar
* Crie o **virtual environment** dentro do diretório do repositório<br>
`$ python3 -m venv nba_env`<br>

* Ativando o **virtual environment**<br>
`$ source nba_env/bin/activate` (MacOS e Linux) **ou** <br>
`$ nba_env\Scripts\activate` (Windows)<br>

* Instalando as dependências (repetir esses 2 passos a cada vez que um novo pacote for instalado)<br>
`$ /usr/local/opt/postgres/bin/createuser -s postgres` (***apenas se*** utiliza MacOS + HomeBrew)<br>
`$ pip install -r requirements.txt`

* Inicie o servidor do PostgreSQL<br>
`$ pg_ctl -D /usr/local/var/postgres start` (MacOS + HomeBrew)<br>
`$ sudo service postgresql start` (Linux) <br>
  
* Crie um banco de dados chamado **pokemon** no seu PostgreSQL Client favorito (eu uso o Postbird)<br>

* Inicie o processo de migração do banco de dados:<br>
`$ flask db init`
  
* Crie o script de migração do banco de dados:<br>
`$ flask db migrate`

* Atualize o banco de dados:<br>
`$ flask db upgrade`

* Rode o script que insere os dados no banco:<br>
`$ python insert.py`

## 💻 Como executar
* Rodar o back-end<br>
`$ flask run`

## 🎯 Consultas disponibilizadas por endpoints
*  `http://localhost:5000/api/<Nome Função>`
