# G13-TAI

# Assignment III - Teoria Algorítmica da Informação

92969 - Diogo Carvalho - Participação 1/3 

95278 - Diogo Cunha - Participação 1/3 

93367 - Rafael Baptista - Participação 1/3 


## Instruções de execução

### SampleCreation
Programa usado para a criação de samples.
```
python3 sampleCreation.py -ftarget path_do_ficheiro
```

```
Argumentos Opcionais:
-start      Definir o segundo em que a sample vai ser criada
-duration   Definir a duração da sample em segundos
-noise      Definir o volume do barulho a adicionar na sample
-type       Definir o tipo de barulho
```

```
Exemplo de uso:
python3 sampleCreation.py -ftarget "Adele - Easy On Me"
```

### PreProcesser
Programa usado para converter os ficheiros para .wav, e alterar a taxa de amostragem para 44100Hz.
```
Exemplo de uso:
python3 preprocessor.py
```

### MusicFinder
Programa capaz de reconhecer uma música dado uma sample com diversos compressores.

```
python3 musicfinder.py -ftarget path_da_sample
```

```
Argumentos Opcionais:
-compressor      Definir o compressor a ser usado. Por defeito é o gzip. ["gzip", "lzma", "bz2", "bzip2", "zlib", "lz4"]
-top             Definir o top de previsões de músicas. Por defeito é o top 1. [1, 3, 5, 10]
```

```
Exemplo de uso:
python3 musicfinder.py -ftarget sample01
```