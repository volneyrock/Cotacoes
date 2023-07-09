# Cotações

Este projeto é uma página e também API de cotações de moedas que permite ao usuário obter cotações de moedas filtradas por símbolo de moeda, data de início e data de término.

## Executando o projeto

O projeto usa Docker e Docker Compose para facilitar a configuração e a execução. Para executar o projeto, siga as etapas abaixo:

1. Certifique-se de que o Docker e o Docker Compose estejam instalados em sua máquina. Caso não estejam, você pode baixá-los [aqui](https://docs.docker.com/get-docker/) e [aqui](https://docs.docker.com/compose/install/), respectivamente.

2. Clone este repositório na sua máquina:

    ```bash
    git clone https://github.com/volneyrock/desafioBrMed
    ```

3. Navegue para a pasta do projeto:

    ```bash
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```

4. Construa e execute o projeto com Docker Compose:

    ```bash
    docker-compose up --build
    ```

Agora o projeto deve estar rodando em `localhost:80`.

## Documentação da API

A documentação da API está disponível em `localhost:80/swagger/` ou se preferir `localhost:80/redoc/`  quando o projeto está sendo executado. A documentação usa o Swagger e inclui detalhes de todos os endpoints disponíveis, bem como os parâmetros que podem ser usados.

<!-- ## Versão online
Fiz deploy da aplicação em uma instencia EC2 da AWS, para acessar a aplicação online basta acessar os links abaixo:

Página web: [http://34.207.78.174/](http://54.227.89.163/)

Documentação da API estilo swagger: [http://34.207.78.174/swagger](http://54.227.89.163/swagger)

Documentação da API estilo redoc: [http://34.207.78.174/redoc](http://54.227.89.163/redoc) -->

## Testes
Voce pode rodar os testes usando o comando:
``` docker compose run --rm test ```
