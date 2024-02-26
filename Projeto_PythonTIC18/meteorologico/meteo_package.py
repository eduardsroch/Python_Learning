# Conteúdo de meu_pacote_meteorologico/meteo_package.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

def obter_dados():
    # URL do site
    link = "https://portal.inmet.gov.br/dadoshistoricos"
    
    # Configuração do cabeçalho da requisição
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # Fazendo a requisição HTTP
    requisicao = requests.get(link, headers=headers)
    
    # Verificando se a requisição foi bem sucedida
    if requisicao.status_code == 200:
        # Parseando o conteúdo HTML da página
        site = BeautifulSoup(requisicao.text, 'html.parser')
    else:
        # Exibindo mensagem de erro em caso de falha na requisição
        messagebox.showerror("Erro", "Erro na requisição")
        return None

    # Obtendo os anos e os links das postagens do site
    anos = site.find_all('article', class_='post-preview')
    ano = []
    link = []
    for i in anos:
        ano.append(i.find('a').string)
        link.append(i.find('a')['href'])
    return ano, link

def mostrar_erro():
    messagebox.showerror("Erro", "Erro na conexão com o site. Verifique sua conexão com a internet.")

def obter_estacoes(ano_selecionado):
    # Formatando o nome do arquivo
    nome_arquivo = ano_selecionado.replace(' ', '_').replace('(', '').replace(')', '')
    
    # Construindo o link para download do arquivo zip
    link = f"https://portal.inmet.gov.br/uploads/dadoshistoricos/{ano_selecionado}.zip"

    # Cria um diretório temporário para armazenar o arquivo zip
    temp_dir = 'temp_zip_folder'
    os.makedirs(temp_dir, exist_ok=True)
    print(f'Diretório temporário criado em: {temp_dir}')

    # Define o caminho completo para o arquivo zip
    zip_file_path = os.path.join(temp_dir, f'{nome_arquivo}.zip')

    # Tenta baixar o arquivo zip
    try:
        with requests.get(link, stream=True) as response:
            response.raise_for_status()
            with open(zip_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

        # Tenta descompactar o arquivo zip
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                # Cria um subdiretório se o ano for maior que 2019
                if int(ano_selecionado) > 2019:
                    temp_dir = os.path.join(temp_dir, ano_selecionado)
                    os.makedirs(temp_dir, exist_ok=True)
                zip_ref.extractall(temp_dir)

            # Retorna a lista de estações disponíveis
            if int(ano_selecionado) <= 2019:
                estacoes = os.path.join(temp_dir, ano_selecionado)
                estacoes = os.listdir(estacoes)
            else:
                estacoes = os.listdir(temp_dir)
            return estacoes
        except zipfile.BadZipFile:
            messagebox.showerror("Erro", f"Erro: O arquivo baixado para o ano {ano_selecionado} não é um arquivo zip válido.")
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro na requisição: {e}")
        return None

def obter_dados_estacao(ano_selecionado, estacao_selecionada):
    # Construindo o caminho do arquivo CSV
    caminho_arquivo_csv = f'temp_zip_folder/{ano_selecionado[4:8]}/{estacao_selecionada}'
    print(estacao_selecionada)
    print(caminho_arquivo_csv)

    try:
        # Lendo o arquivo CSV
        dados_estacao = pd.read_csv(caminho_arquivo_csv, encoding='iso-8859-1', decimal=',', delimiter=';', skiprows=8)

        print("Dados carregados:")
        print(dados_estacao.head())

        print("Colunas disponíveis:")
        print(dados_estacao.columns)

        return dados_estacao
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo CSV para a estação {estacao_selecionada} não encontrado.")
        return pd.DataFrame()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV para a estação {estacao_selecionada}: {e}")
        return pd.DataFrame()

def gerar_graficos(ano_selecionado, estacao_selecionada, janela):
    # Obtendo os dados da estação selecionada
    dados_estacao = obter_dados_estacao(ano_selecionado, estacao_selecionada)

    # Criando a figura e os subplots
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8, 6), dpi=100)
    
    # Configurando o índice do DataFrame
    index = pd.DatetimeIndex(dados_estacao.iloc[:, 0], name='Data')
    dados_estacao.drop(columns=dados_estacao.columns[0], axis=1, inplace=True)
    dados_estacao.set_index(index, inplace=True)
    
    # Tratando os dados de temperatura
    dados_estacao['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'] = dados_estacao['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].apply(
        lambda x: None if x < -14 else x)
    temp = dados_estacao.groupby(dados_estacao.index)['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].mean()
    temp.index = temp.index.strftime("%b")
    temp.plot(ax=ax, title="Temperatura Média Mensal", ylabel="Temperatura (°C)", color='blue')
    ax.set_xlabel("Mês", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(["Temperatura Média"], loc="upper right")
    
    # Tratando os dados de precipitação
    dados_estacao['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'] = dados_estacao['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].apply(
        lambda x: None if x < 0 else x)
    prec = dados_estacao.groupby(dados_estacao.index)['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].mean()
    prec.index = prec.index.strftime("%b")
    prec.plot(ax=ax2, title="Precipitação Mensal", ylabel="Precipitação (mm)", color='green')
    ax2.set_xlabel("Mês", fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend(["Precipitação"], loc="upper right")

    # Ajustando o espaçamento entre os subplots
    fig.subplots_adjust(wspace=0.5, hspace=0.5)

    # Criando o canvas para exibir a figura na janela
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.get_tk_widget().pack()

def main():
    # Criando a janela principal da interface gráfica
    root = tk.Tk()
    root.title('Dados Meteorológicos')
    root.geometry("800x600")

    # Obtendo os dados do site
    dados_site = obter_dados()

    if dados_site:
        ano, link = dados_site

        # Criando a label e a combobox para selecionar o ano
        label_ano = tk.Label(root, text='Selecione o Ano:', font=('Arial', 15))
        label_ano.pack()

        var_ano = tk.StringVar()
        combobox_ano = ttk.Combobox(root, textvariable=var_ano, values=ano, font=('Arial', 15))
        combobox_ano.pack()

        # Função para obter as estações com base no ano selecionado
        def obter_estacoes_selecionar_ano():
            ano_selecionado = var_ano.get()
            if ano_selecionado:
                estacoes = obter_estacoes(ano_selecionado[4:8])
                if estacoes:
                    var_estacoes.set('')
                    combobox_estacoes['values'] = estacoes
                else:
                    mostrar_erro()

        # Botão para obter as estações
        botao_obter_estacoes = ttk.Button(root, text='Obter Estações', command=obter_estacoes_selecionar_ano, style='TButton')
        botao_obter_estacoes.pack()

        # Criando a label e a combobox para selecionar a estação
        label_estacoes = tk.Label(root, text='Selecione a Estação:', font=('Arial', 15))
        label_estacoes.pack()

        var_estacoes = tk.StringVar()
        combobox_estacoes = ttk.Combobox(root, textvariable=var_estacoes, font=('Arial', 15))
        combobox_estacoes.pack()

        # Função para gerar os gráficos da estação selecionada
        def gerar_graficos_estacao():
            ano_selecionado = var_ano.get()
            estacao_selecionada = var_estacoes.get()
            if ano_selecionado and estacao_selecionada:
                nova_janela = tk.Toplevel(root)
                nova_janela.title(f'Gráficos - {estacao_selecionada}')
                gerar_graficos(ano_selecionado, estacao_selecionada, nova_janela)
            else:
                messagebox.showerror("Erro", "Selecione ano e estação antes de gerar os gráficos.")

        # Botão para gerar os gráficos
        botao_gerar_graficos = ttk.Button(root, text='Gerar Gráficos', command=gerar_graficos_estacao, style='TButton')
        botao_gerar_graficos.pack()

    else:
        mostrar_erro()

    # Configurando o estilo dos botões
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 15))

    # Iniciando o loop principal da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    main()
