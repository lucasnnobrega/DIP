# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

# %%
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import scipy.io.wavfile
from scipy import fftpack
import pydub
from pydub.playback import play
import math

# %%
'''
N = 10

Cos_table = [
    [math.cos((2*n+1)*k * math.pi/2*N) for k in range(N)] for n in range(N)
]
Cos_table = []
for n in range(N):
    aux = []
    for k in range(N):
        # aux.append(math.cos((2*n+1)*(k * math.pi/2*N)))
        aux.append(math.cos((((2*n)+1)*(k * (math.pi/(2*N))))))
    Cos_table.append(aux)


Cos_table
'''
# %%
'''
import time

a = 10

for i in range(10):
    time.sleep(0.9)
    print("#"*i, " "*(9-i), "|", i, end="\r")
'''
# %%


def dct1D(vector):
    N = len(vector)
    X = np.zeros(N)

    print("Running my DCT")
    '''
    to_prompt = "Are you sure? N = " + str(N)
    input(to_prompt)

    # Creating a matrix to reuse the values of Cos already calculated
    Cos_table = (
        (math.cos((2*n+1)*k * math.pi/(2*N)) for k in range(N)) for n in range(N)
    )
    print("Cos_table Created")
    '''

    for k in range(N):
        Ak = math.sqrt(1.0/N) if k == 0 else math.sqrt(2.0/N)
        sum = 0
        for n in range(N):
            # f1 = ((2*(math.pi)*k*n)/2*N)
            # f2 = ((k*(math.pi))/2*N)
            # sum += vector[n] * math.cos(f1+f2)
            # sum += vector[n] * math.cos(((2*math.pi*k*n)/2*N)+((k*math.pi)/2*N))
            # sum += vector[n] * Cos_table[k][n]

            sum += vector[n] * math.cos(((2*n+1)*k*math.pi)/(2*N))

        X[k] = Ak * sum

        # print("#"*k, " "*(9-k), "|", k, end="\r")

        print("k: ", k, " | N: ", N)

    return X


def dct1D_G(vector):
    N = len(vector)

    print("Running my DCT")

    for k in range(N):
        Ak = math.sqrt(1.0/N) if k == 0 else math.sqrt(2.0/N)
        sum = 0
        for n in range(N):
            sum += vector[n] * math.cos((2*n+1)*k * math.pi/(2*N))

        yield Ak * sum


# %%
# CalculaIDCT


# %%
def idct1D(vector):

    N = len(vector)
    x = np.zeros(N)

    for n in range(N):
        sum = 0

        for k in range(N):
            f1 = ((2*math.pi*k*n)/2*N)
            f2 = ((k*math.pi)/2*N)
            CK = math.sqrt(1.0/N) if k == 0 else math.sqrt(2.0/N)
            #sum += vector[n] * math.cos(f1+f2)
            sum += CK * vector[k] * math.cos((f1)+(f2))
            #sum += alpha * vector[k] * math.cos((math.pi * (2*n+1) * k) / (2*N))

        x[n] = sum

    return x

# %% [markdown]
# # Função para plotagem do gráfico com a DCT Filtrada

# %%


def plotaDCTs(dct, dctFiltrada):
    plt.figure('Domínio da Frequência')
    plt.subplot(211)
    plt.plot(dct, linewidth=0.1, alpha=1.0, color='blue')
    plt.ylabel('Frequencia')
    plt.title('DCT')
    plt.subplot(212)
    plt.plot(dctFiltrada, linewidth=0.1, alpha=1.0, color='blue')
    plt.ylabel('Frequencia')
    plt.title('DCT Filtrada')
    plt.show()


# %%
def desenhaGrafico(nomeArquivo, data):
    plt.figure(nomeArquivo)
    plt.plot(data, linewidth=0.1, alpha=1, color='red')
    plt.ylabel('Amplitude')
    plt.show()

# %%


x_slide = []

X_slide = [10, 5, 8.5, 2, 1, 1.5, 0, 0.1]

#x_slide = fftpack.idct(X_slide, norm='ortho')
x_slide = idct1D(X_slide)

print(x_slide)
desenhaGrafico("x_slide", x_slide)

'''

# %% [markdown]
# # DCTAudio


# %%
nomeArquivo = "MaisUmaSemana.wav"
rate, audioData = scipy.io.wavfile.read(nomeArquivo)
desenhaGrafico(nomeArquivo, audioData)


# %%
slide = []
DCT = dct1D(slide)
# DCT = dct1D(audioData)
print(type(DCT))
# DCT = fftpack.dct(audioData, norm='ortho')  # Calcula a Transformada Discreta


# print (DCT)
dctFiltrada = DCT.copy()
# print (dctFiltrada)


# %%
# Cria uma lista com os valores resultantes da Transformada Discreta
listaComDCT = dctFiltrada.tolist()
# print(listaComDCT)
Indices = []

# Percorre todo o array e troca os valores pelo seu módulo
for i in range(0, len(listaComDCT)):
    listaComDCT[i] = abs(listaComDCT[i])
    aux = listaComDCT.copy()

# print(listaComDCT)


# %%
numero_de_frequencias_desejadas = int(
    input("Digite o numero de frequencias desejadas"))


# %%
# Adiciona na lista os n índices de maior valor, com n = numero de amostras
for i in range(0, numero_de_frequencias_desejadas):
    Indices.append(listaComDCT.index(max(aux)))
    indiceAux = aux.index(max(aux))
    aux.pop(indiceAux)

    # dctFiltrada = DCT.copy()

print(Indices)


# %%
# Preserva os DCT's de tamanho igual aos da lista de IndiceMaximo verificando se eles estão na lista e zera os demais
for i in range(0, len(dctFiltrada)):
    if i not in Indices:
        dctFiltrada[i] = 0

dctFiltrada = np.asarray(dctFiltrada)

AudioTransformado = fftpack.idct(DCT, norm='ortho')
AudioTransformado = AudioTransformado.astype("int16")
scipy.io.wavfile.write("audioTransformado.wav", rate, AudioTransformado)

AudioTransformadoImportantes = fftpack.idct(dctFiltrada, norm='ortho')
AudioTransformadoImportantes = AudioTransformadoImportantes.astype("int16")
scipy.io.wavfile.write("AudioTransformadoImportantes.wav",
                       rate, AudioTransformadoImportantes)

plotaDCTs(DCT, dctFiltrada)

'''
