# KnowLow2 - Bot de Discord para RPG de Mesa

## Visão Geral

O KnowLow2 é um bot de Discord projetado para aprimorar a experiência de jogadores e mestres de RPG de mesa, especialmente para o sistema de D&D 5ª Edição. Ele oferece funcionalidades como rolagem de dados e busca de informações sobre regras e informações do jogo.

## Funcionalidades

* **Rolagem de Dados:** Role dados virtuais com o comando `!NdM`, onde N é o número de dados e M é o número de faces (ex: `!d20`, `!2d6`).

* **Busca de Informações:** Faça perguntas sobre regras, mecânicas e informações de D&D 5ª Edição usando o comando `!pergunta <sua pergunta>`. O bot utiliza o Google para buscar informações relevantes.

* **Mensagens de Boas-Vindas:** Envia uma mensagem de boas-vindas automática para novos membros do servidor.

## Como Usar

1.  **Crie um bot no Discord Developer Portal:**

    *  Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
    *  Clique em "Create New Application".
    *  Dê um nome ao seu bot e clique em "Create".
    *  No menu à esquerda, clique em "Bot".
    *  Clique em "Add Bot" e confirme a criação do bot.
    *  Copie o "Token" do seu bot e guarde-o em segurança.
    *  Em "Privileged Gateway Intents", habilite "SERVER MEMBERS Intent" e "MESSAGE CONTENT INTENT".

2.  **Configure o token:** Certifique-se de ter o token do seu bot configurado como uma variável de ambiente (`DISCORD_TOKEN`).

3.  **Convide o bot para o seu servidor:**
    * No menu à esquerda do Portal do Desenvolvedor, clique em "OAuth2" e depois em "URL Generator".
    * Em "Scopes", selecione "bot".
    * Em "Bot Permissions", selecione as permissões que o bot precisa (por exemplo, "Send Messages", "Read Message History").
    * Copie o URL gerado e abra-o no seu navegador.
    * Selecione o servidor para onde você quer adicionar o bot e clique em "Authorize".

4.  **Use os comandos:** Utilize os comandos no chat do Discord para rolar dados e buscar informações.

## Tecnologias Utilizadas

* [Discord.py](https://discordpy.readthedocs.io/en/stable/): Biblioteca Python para interagir com a API do Discord.

* [Google ADK](https://developers.google.com/assistant/sdk): Para processamento de linguagem natural e busca de informações.

* [dotenv](https://github.com/theskumar/python-dotenv): Para carregar variáveis de ambiente a partir de um arquivo `.env`.

## Pré-requisitos

* Python 3.6 ou superior

* Conta no Discord e permissão para adicionar bots a um servidor

* Chave de API do Google Cloud

## Instalação

1.  Clone este repositório:

    ```bash
    git clone [https://github.com/seu-usuario/KnowLow2.git](https://github.com/seu-usuario/KnowLow2.git)
    ```

2.  Crie um arquivo `.env` e adicione o token do seu bot e a chave de API do Google:

    ```
    DISCORD_TOKEN=seu_token_do_discord
    GOOGLE_API_KEY=sua_chave_de_api_do_google
    ```

3.  Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4.  Execute o bot:

    ```bash
    python main.py
    ```
