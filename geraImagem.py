import torch
from diffusers import StableDiffusionPipeline
import os
import re
import time
import string
import psycopg2
import requests
import unicodedata
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv


def remover_pontuacoes(texto):
    """
    Remove as pontuações de um texto.
    :param texto: O texto original com pontuações.
    :return: O texto sem pontuações.
    """
    # Cria uma tabela de tradução que mapeia cada pontuação para None
    tabela_remocao = str.maketrans('', '', string.punctuation)
    
    # Remove as pontuações usando a tabela de tradução
    texto_sem_pontuacoes = texto.translate(tabela_remocao)
    
    return texto_sem_pontuacoes


def remover_diacriticos(texto):
    """
    Remove os diacríticos (acentos, til, etc.) de um texto.
    :param texto: O texto original com diacríticos.
    :return: O texto sem diacríticos.
    """
    # Normaliza o texto para decompor caracteres acentuados
    texto_normalizado = unicodedata.normalize('NFD', texto)
    
    # Remove os caracteres de diacríticos
    texto_sem_diacriticos = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
    
    return texto_sem_diacriticos


# Busca a data atual
def data_tempo():
    return datetime.now()


# Roda query para executar o PG
def conecta_pg(sql):
    """
    Roda query para executar

    Parameters:
    Sql = string

    Returns:
    tabela_sql = datatable
    """

    # Carrega as variáveis do ambiente
    load_dotenv()

    host_database = os.getenv("HOST")
    database_database = os.getenv("DATABASE")
    user_database = os.getenv("USER")
    password_database = os.getenv("PASSWORD")

    host = host_database # Endereço do servidor
    database = database_database  # Nome do banco de dados
    user = user_database  # Nome de usuário para acessar o banco de dados
    password = password_database  # Senha do usuário para acessar o banco de dados
    port = 5432

    # Estabelece a conexão com o banco de dados
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    cursor = connection.cursor()
    cursor.execute(sql)
    tabela_sql = cursor.fetchall()
    cursor.close()
    connection.close()

    # Retorna o resultado da consulta do SQL para o usuário
    return tabela_sql


# Roda query para executar o MySQL
def conecta_pg_insert(sql):
    """
    Roda query para executar o MySQL

    Parameters: 
    sql = string
    """

    # Carrega as variáveis do ambiente
    load_dotenv()

    host_database = os.getenv("HOST")
    database_database = os.getenv("DATABASE")
    user_database = os.getenv("USER")
    password_database = os.getenv("PASSWORD")

    host = host_database # Endereço do servidor
    database = database_database  # Nome do banco de dados
    user = user_database  # Nome de usuário para acessar o banco de dados
    password = password_database  # Senha do usuário para acessar o banco de dados
    port = 5432

    # Estabelece a conexão com o banco de dados
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


# Gerador de imagem
def gerar_imagem(caminho_arquivo, prompt, numero):
    # Carregar o modelo
    # pipeline = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    # pipeline = StableDiffusionPipeline.from_pretrained("dreamlike-art/dreamlike-photoreal-2.0")
    pipeline = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1-base")

    # Use GPU se disponível, caso contrário, use CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipeline = pipeline.to(device)

    # Prompt de entrada
    prompt = (
        prompt
    )

    # Gerar a imagem
    # image = pipeline(prompt).images[0]
    image = pipeline(prompt, height=1920, width=1080).images[0]
    # image = pipeline(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]

    prompt = remover_diacriticos(prompt[:10])
    prompt = remover_pontuacoes(prompt)

    # Salvar a imagem
    image.save(rf"{caminho_arquivo}\{str(numero)}. {prompt}.png")


# Itera sobre os textos
def acessa_resultados(tabela, caminho_arquivo):
    data_atual = data_tempo()

    numero = 1

    sql = f"""select * from youtube.{tabela} where utilizado = 'Mais relevante' and data_noticia::date = '{data_atual.strftime("%Y-%m-%d")}'"""
    tabela_sql = conecta_pg(sql=sql)

    for pk, titulo, descricao, url, conteudo, utilizado, texto_narrador, data_noticia, prompt_imagens, titulo_video, descricao_video, thumbnail, caminho_arquivo_tabela in tabela_sql:
        titulo_novo = remover_diacriticos(titulo)
        titulo_novo = remover_pontuacoes(titulo_novo)

        prompt_imagens_divididas = prompt_imagens.split("\n")

        caminho_salvar = rf"{caminho_arquivo}\Imagens"

        for prompt in prompt_imagens_divididas:
            gerar_imagem(caminho_arquivo=caminho_salvar, prompt=prompt, numero=numero)

            numero += 1

        gerar_imagem(caminho_arquivo=caminho_salvar, prompt=str(thumbnail).replace('"', ""), numero="Thumbnail")

        break
        


if __name__ == "__main__":
    # Exemplo de uso
    # acessa_resultados(tabela="frequencia_COMPANY_NAME", id_voice="36rVQA1AOIPwpA3Hg1tC", caminho_arquivo=rf"C:\Users\nicol\OneDrive\Cursos online\Youtube\Frequência COMPANY_NAME\Vídeos\Áudios")

    acessa_resultados(tabela="segredos_e_sombras", caminho_arquivo=rf"C:\Users\nicol\OneDrive\Cursos online\Youtube\Segredos e Sombras")