import discord
import os
import random
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

load_dotenv()

TOKEN_DISCORD = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configuração do serviço de sessão para o ADK
session_service = InMemorySessionService()



class KnowLow2(discord.Client):

    async def on_ready(self):
        print(f'Logado como {self.user}')


    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            mensagem = f'Olá {member.mention}! Seja bem-vindo(a) ao servidor {guild.name}!'
            await guild.system_channel.send(mensagem)
        else:
            general_channel = discord.utils.get(guild.text_channels, name='geral')
            if general_channel:
                mensagem = f'Olá {member.mention}! Seja bem-vindo(a) ao servidor {guild.name}!'
                await general_channel.send(mensagem)
            else:
                print(f'Não foi possível encontrar um canal de boas-vindas para {member.name} no servidor {guild.name}.')


    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!'):
            comando = message.content[1:].lower()
            if 'd' in comando and not comando.startswith('pergunta'):
                await self.rolar_dados(message, comando)
            elif comando.startswith('pergunta'):
                pergunta = comando[len('pergunta'):].strip()
                if pergunta:
                    await self.processar_pergunta_adk(message, pergunta)
                else:
                    await message.channel.send(f'{message.author.mention} Por favor, inclua sua pergunta após o comando !pergunta.')


    def agente_buscador_adk(self):
        buscador = Agent(
            name="agente_buscador_regras_detalhes",
            model="gemini-2.0-flash",
            description="Agente que busca informações no Google sobre informações de rpg D&D.",
            tools=[google_search],
            instruction="""
                Propósito e Objetivos:
                * Auxiliar mestres e jogadores durante sessões de RPG de D&D 5ª Edição.
                * Responder a dúvidas sobre regras, mecânicas, lore e outros aspectos do jogo.
                * Fornecer informações relevantes de forma clara e concisa.
                * Impedir que jogadores obtenham informações confidenciais que seus personagens não deveriam ter.

                Comportamentos e Regras:
                1) Interação Inicial:
                    a) Apresente-se como um assistente para o mestre e jogadores de RPG de D&D 5ª Edição.
                2) Resposta a Dúvidas:
                    a) Responda a perguntas sobre regras da 5ª Edição de D&D de forma precisa e referenciando o material oficial quando apropriado.
                    b) Auxilie na interpretação de regras e mecânicas de jogo.
                    c) Forneça informações sobre o cenário de campanha, monstros e NPCs, desde que não sejam informações secretas para os jogadores.
                    d) Mantenha um tom útil e informativo.
                3) Proteção de Informações Confidenciais:
                    a) Se um jogador perguntar por informações que seu personagem não teria acesso (
                        como pontos de vida exatos de um monstro, detalhes de uma armadilha que não foi descoberta, ou segredos da trama conhecidos apenas pelo mestre
                    ), responda com a frase exata: 'Você não pode saber dessa informação'.
                    b) Não forneça nenhuma dica ou informação adicional que possa revelar o conteúdo confidencial.
                    c) Mantenha a resposta concisa e direta ao negar acesso à informação.

                Tonalidade Geral:
                * Seja prestativo e cortês.
                * Demonstre conhecimento das regras de D&D 5ª Edição.
                * Mantenha a imparcialidade, auxiliando tanto o mestre quanto os jogadores, dentro dos limites estabelecidos.
                * Responda de forma clara e objetiva.
            """
        )
        return buscador


    async def processar_pergunta_adk(self, message, pergunta):
        try:
            buscador = self.agente_buscador_adk()
            response = self.call_agent(buscador, pergunta)
            await message.channel.send(response)
        except Exception as e:
            await message.channel.send(f'{message.author.mention} Ocorreu um erro ao processar a pergunta com o agente: {e}')


    def call_agent(self, agent: Agent, message_text: str) -> str:
        session_service = InMemorySessionService()
        session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")

        runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
        content = types.Content(role="user", parts=[types.Part(text=message_text)])

        final_response = ""
        for event in runner.run(user_id="user1", session_id="session1", new_message=content):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text is not None:
                        final_response += part.text + "\n"
        return final_response


    async def rolar_dados(self, message, comando):
        try:
            partes = comando.split('d')
            if len(partes) == 2:
                num_dados = int(partes[0]) if partes[0] else 1
                tipo_dado = int(partes[1])

                if num_dados > 0 and tipo_dado > 1:
                    rolagens = [random.randint(1, tipo_dado) for _ in range(num_dados)]
                    total = sum(rolagens)
                    resultado = f'{message.author.mention} rolou {num_dados}d{tipo_dado}: {rolagens}'
                    if num_dados > 1:
                        resultado += f' = **{total}**'
                    await message.channel.send(resultado)
                else:
                    await message.channel.send(f'{message.author.mention} Comando de dados inválido. Use !NdM, onde N é o número de dados e M é o número de faces (ex: !d20, !2d6).')
            else:
                await message.channel.send(f'{message.author.mention} Comando de dados inválido. Use !NdM, onde N é o número de dados e M é o número de faces (ex: !d20, !2d6).')
        except ValueError:
            await message.channel.send(f'{message.author.mention} Comando de dados inválido. Certifique-se de que o formato seja !NdM (ex: !d20, !2d6).')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = KnowLow2(intents=intents)
client.run(TOKEN_DISCORD)
