# g2-3soat-sa-auth-app


Este é um projeto Serverless que utiliza o Amazon Cognito User Pool para gerenciar usuários em uma aplicação serverless.

## Configuração

Antes de começar, é necessário configurar o ambiente:

1. Certifique-se de ter o [Serverless Framework](https://www.serverless.com/) instalado localmente.
2. Configure suas credenciais da AWS no seu ambiente local.
3. Certifique-se de ter um User Pool configurado no Amazon Cognito.


## Funções Lambda

### 1. `register_user`

Esta função registra um novo usuário no Amazon Cognito User Pool.

- **Endpoint:** `/register-user`
- **Método:** `POST`
- **Parâmetros:**
  - `email`: Email do usuário a ser registrado.
- **Retorno:**
  - Status code 200 se o usuário for registrado com sucesso.
  - Status code 400 se o email não for fornecido ou se o usuário já existir.
  - Status code 500 se ocorrer um erro inesperado.

### 2. `confirm_user`

Esta função confirma o registro de um usuário no Amazon Cognito User Pool usando o código de confirmação recebido.

- **Endpoint:** `/confirm-user`
- **Método:** `POST`
- **Parâmetros:**
  - `email`: Email do usuário.
  - `confirmationCode`: Código de confirmação recebido pelo usuário.
- **Retorno:**
  - Status code 200 se o usuário for confirmado com sucesso.
  - Status code 400 se o email ou o código de confirmação não forem fornecidos ou se o código de confirmação for inválido.
  - Status code 404 se o usuário não for encontrado.
  - Status code 500 se ocorrer um erro inesperado.

### 3. `authenticate_user`

Esta função autentica um usuário no Amazon Cognito User Pool.

- **Endpoint:** `/authenticate-user`
- **Método:** `POST`
- **Parâmetros:**
  - `email`: Email do usuário a ser autenticado.
- **Retorno:**
  - Status code 200 se o usuário for autenticado com sucesso, juntamente com um token de acesso.
  - Status code 400 se o email não for fornecido.
  - Status code 401 se o email estiver incorreto.
  - Status code 404 se o usuário não for encontrado.
  - Status code 500 se ocorrer um erro inesperado.

## Como usar

1. Clone este repositório para o seu ambiente local.
2. Configure suas credenciais da AWS no seu ambiente local.
3. Execute `serverless deploy` para implantar o projeto no AWS Lambda.
4. Use os endpoints fornecidos para registrar, confirmar e autenticar usuários no Amazon Cognito User Pool.
