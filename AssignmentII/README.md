# G13-TAI

# Assignment II - Teoria Algorítmica da Informação

#### 92969 - Diogo Carvalho - Participação 1/3 
#### 95278 - Diogo Cunha - Participação 1/3 
#### 93367 - Rafael Baptista - Participação 1/3 


## Instruções de execução

### Lang
Programa capaz de efetuar o cálculo do número de bits necessários para comprimir um texto alvo.

```
python3 lang.py -freference path_do_ficheiro -ftarget path_do_ficheiro -k tamanho_do_contexto -a smoothing_parameter
```

```
Argumentos Opcionais:
--multiplemodels    Usar modelos com tamanho de contextos diferentes
```

```
Exemplo de uso:
python3 src/lang.py -freference example/POR/portuguese-medium.txt -ftarget example/POR/portuguese-small.utf8 -k 4 -a 0.5
```

### Findlang
Programa capaz de reconhecer em que língua um determinado texto alvo está escrito.

```
python3 findlang.py -ftarget path_do_ficheiro -k tamanho_do_contexto -a smoothing_parameter
```

```
Argumentos Opcionais:
--multiplemodels    Usar modelos com tamanho de contextos diferentes
```

```
Exemplo de uso:
python3 src/findlang.py -ftarget example/POR/portuguese-small.utf8 -k 4 -a 0.5
```

### Locatelang
Programa capaz de reconhecer em que secções e respetivas línguas um determinado texto alvo escrito em várias línguas possui.

```
python3 locatelang.py -ftarget path_do_ficheiro -k tamanho_do_contexto -a smoothing_parameter
```

```
Exemplo de uso:
python3 src/locatelang.py -ftarget example/multilang1-PT-ENG-PT.txt -k 4 -a 0.5
```