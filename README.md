# google-places-project
Webservice​ que faz uma busca de locais pelo nome do local na Google Places API e armazena os resultados.


**Instalar Depedências**

`$ cd google-places-project`

`$ pip3 install -r requirements`


**Versão do Python**

O Webservice só roda com a versão 3.3 ou acima do Python.


**Rodar Webservice**

`$ cd google-places-project`

`$ python3 run.py` 

Argumentos:
    --host=`<host>` (Default localhost)
    --port=`<port>` (Default 8000)


**Rodar Testes**

`$ PYTHONPATH=<my_dir>/google-places-project python3 tests/<test>.py`

**Api**

GET `http://<host>:<port>/places/`

Query String

- name: Nome do Local, é obrigatório;

Retorno

Array de objetos com pares: address, name, place_id, latitude e longitude.

Status Code

- 200 - OK;
- 400 - Caso name não seja passado;


POST `http://<host>:<port>/places/`

Corpo do Pedido (JSON)

- address - String com o endereço completo; 
- name - String com o Nome do Local;
- place_id - String com o Google Place ID;
- latitude - Número de acordo com a latitude do Local;
- longitude - Número de acordo com a longitude do Local;

Retorno

Objeto com os pares do corpo + ID.

Status Code

- 201 - OK;
- 400 - Caso o corpo do request esteja inválido;

DELETE `http://<host>:<port>/places/<ID>`

Status Code

- 204 - OK;
- 404 - Caso não exista o ID cadastrado;
