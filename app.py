import streamlit as st
from PIL import Image
import io
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from pathlib import Path
from matplotlib.colors import to_hex

def get_palette(imagem_carregada, n_cores):
    
    with open('imagem.jpg', 'wb') as file:
        # Salva a imagem
        file.write(imagem_carregada.getbuffer())
        
        # Lê a imagem
        image = Image.open('imagem.jpg')
        
        #Transforma os Pixels em uma matriz
        N, M = image.size
        X = np.asarray(image).reshape((N*M), 3)
        
        # Cria e aplica o K-means
        model = KMeans(n_clusters=n_cores).fit(X)

        # Captura as cores médias dos grupos gerados no K-means
        cores = model.cluster_centers_.astype('uint8')[np.newaxis]
        cores_hex = [to_hex(cor/255) for cor in cores[0]]
        
        # Apaga a imagem
        try:
            Path('imagem.jpg').unlink()
        except:
            print("Erro ao apagar a imagem")
        
        # Retorna as cores
        return cores, cores_hex
    
def show(cores):
    figure = plt.figure()
    plt.imshow(cores)
    plt.axis('off')
    return figure

def download(figura):
    imagem = io.BytesIO()
    figura.savefig(imagem, format="png")
    plt.axis('off')
    return imagem
    

st.title("Gerador de Paletas")

# Campo de Input da Imagem
imagem = st.file_uploader(label="Carregue uma Imagem", type=["jpg","jpeg","png"])

# Divide a página em colunas
col1, col2 = st.columns([.7, .3])

#Quando uma imagem for fornecida na entrada, realiza as ações abaixo
if(imagem):
    # Cria um Preview da imagem da entrada redimensionada
    preview = Image.open(imagem).resize((320,320))

    # Exibe o preview da imagem
    col1.image(preview)
    
    # Campo de Input da quantidade de cores desejadas na paleta
    n_cores = col2.slider("Quantidade de Cores", min_value=2, max_value=8, value=5)
    
    botao_gerar_paleta = col2.button("Gerar Paleta")
    
    if(botao_gerar_paleta):
        # Recebe da função de gerar paleta as cores
        cores, cores_hex = get_palette(imagem, n_cores)
        
        # Recebe da função correspondente a figura da paleta
        figura = show(cores)
        
        # Exibe a figura da paleta
        st.pyplot(fig=figura)
        
        # Exibe as cores em hexadecimal
        st.code(f"{cores_hex}")
        
        # Exibe o botão para download da imagem da paleta gerada pela função correspondente
        col2.download_button("Baixar Paleta", download(figura), "paleta.png", "image/png")