# O comando 'import' serve para trazer "caixas de ferramentas" (bibliotecas) externas para o nosso código.
# 'pandas' é uma ferramenta incrível para ler e mexer com tabelas de dados. O 'as pd' é apenas um apelido curto para não termos que digitar "pandas" toda hora.
import pandas as pd

# 'numpy' é a ferramenta que faz cálculos matemáticos avançados. O 'as np' é o apelido curtinho dela.
import numpy as np

# 'os' (Operating System) é a ferramenta que permite que o Python converse com o seu computador, para ler e checar arquivos e pastas.
import os

# Solicita o nome do arquivo
# O comando 'input' escreve uma mensagem na tela e pausa o programa esperando o usuário digitar algo.
# O que o usuário digitar será guardado dentro da variável (uma "caixa") chamada 'nome_arquivo'.
nome_arquivo = input("Digite o nome do arquivo de entrada (ex: input.txt): ")

# Aqui o código toma uma decisão: 'if' significa "se", e 'not os.path.exists' verifica se o arquivo NÃO existe no computador.
if not os.path.exists(nome_arquivo):
    # Se o arquivo não existir, o 'print' vai exibir (imprimir) essa mensagem de erro na tela para o usuário.
    # Esse 'f' antes das aspas permite que coloquemos o conteúdo da caixa {nome_arquivo} no meio do texto.
    print(f"Erro: O arquivo {nome_arquivo} não foi encontrado!")
    
# 'else' significa "senão". Ou seja, se a condição acima for falsa (se o arquivo existir sim), faça o que vem abaixo:
else:
    # Detecta se o arquivo tem cabeçalho duplo ou simples
    # O comando 'with open' abre o arquivo para leitura ('r' de read). 'encoding='latin-1'' garante que o Python entenda acentos do português. 
    # O 'as f' apelida o arquivo aberto de 'f'. O 'with' garante que o arquivo seja fechado corretamente depois.
    with open(nome_arquivo, 'r', encoding='latin-1') as f:
        # 'f.readline()' manda o Python ler apenas a primeiríssima linha do arquivo e guarda na caixa 'primeira_linha'.
        primeira_linha = f.readline()
    
    # Faz uma checagem rápida no texto da primeira linha. Se encontrar o texto "('", ele entende que é um cabeçalho simples (0). Senão, duplo [0, 1].
    n_linhas_cabecalho = 0 if "('" in primeira_linha else [0, 1]

    # Lê os dados mantendo a estrutura original
    # 'pd.read_csv' é a função do pandas que lê tabelas de texto.
    # 'sep='\t'' avisa que as colunas no arquivo original estão separadas por um "Tab" (espaçamento).
    # 'decimal=','" avisa que os números quebrados usam vírgula (ex: 2,5) em vez de ponto, como no Brasil.
    # Tudo isso vira uma tabela virtual guardada na variável 'dados'.
    dados = pd.read_csv(nome_arquivo, sep='\t', header=n_linhas_cabecalho, decimal=',', encoding='latin-1')
    
    # 'pd.DataFrame' cria uma tabela nova, totalmente em branco, mas com a mesma quantidade de linhas (index) da tabela original ('dados.index').
    dados_transformados = pd.DataFrame(index=dados.index)

    # O 'for' cria um laço de repetição. Significa: "Para cada coluna dentro da lista de colunas da minha tabela 'dados', faça os passos abaixo:"
    for coluna in dados.columns:
        
        # Identifica o nome da variável para checar o '%'
        # 'isinstance(coluna, tuple)' verifica se o nome da coluna é uma dupla de nomes (um cabeçalho duplo).
        if isinstance(coluna, tuple):
            # Se for duplo, ele pega a segunda parte do nome '[1]' e transforma em texto puro com o 'str()'.
            nome_variavel = str(coluna[1])
            
        # 'else' significa "senão" (ou seja, se for um cabeçalho simples de uma linha só).
        else:
            # Pega o nome da coluna diretamente e garante que é um texto com 'str()'.
            nome_variavel = str(coluna)

        # Copia todos os dados (as linhas) referentes apenas à coluna atual e guarda na caixa 'valores_coluna'.
        valores_coluna = dados[coluna]

        # Aplica a transformação se for percentual
        # O 'if' verifica se existe o símbolo de porcentagem '%' dentro do texto do nome da coluna.
        if '%' in nome_variavel:
            
            # Converte para numérico caso necessário e aplica asin(sqrt(x/100))
            # O Python calcula números usando ponto em vez de vírgula. Então pegamos a coluna, garantimos que é texto ('astype(str)'),
            # trocamos a vírgula por ponto ('.replace(',', '.')') e mandamos o pandas forçar para número ('pd.to_numeric').
            # O 'errors='coerce'' transforma qualquer texto que não possa virar número (tipo um espaço vazio) num valor em branco sem quebrar o código.
            v_num = pd.to_numeric(valores_coluna.astype(str).str.replace(',', '.'), errors='coerce')
            
            # Chama as ferramentas matemáticas (np): divide por 100, tira a raiz quadrada ('np.sqrt') e aplica o arco-seno ('np.arcsin').
            transformados = np.arcsin(np.sqrt(v_num / 100))
            
            # Pega essa coluna com os resultados matemáticos e insere na nossa nova tabela em branco que criamos lá em cima.
            dados_transformados[coluna] = transformados
            
            # Mostra na tela uma mensagem avisando que essa coluna específica sofreu a matemática.
            print(f"Variavel: {nome_variavel} -> TRANSFORMADA (Arco-seno)")
            
        # O 'else' age se NÃO houver símbolo de '%' no nome da coluna.
        else:
            # Se não é percentual, apenas copia a coluna original exatamente como estava para a tabela nova.
            dados_transformados[coluna] = valores_coluna
            
            # Mostra na tela avisando que a coluna foi copiada sem sofrer alteração.
            print(f"Variavel: {nome_variavel} -> Mantida original")

    # Define nome de saída
    # Pega o nome do arquivo inicial (ex: "input.txt"), recorta o ".txt" (troca por nada '') e cola a frase '_transformada.txt' no final (fica "input_transformada.txt").
    nome_saida = nome_arquivo.replace('.txt', '') + '_transformada.txt'

    # Exporta mantendo o cabeçalho duplo e o formato original
    # Copia a linha de nomes de cabeçalhos da tabela velha para a tabela nova.
    dados_transformados.columns = dados.columns
    
    # 'to_csv' é o comando que pega a nossa tabela virtual pronta e salva ela no computador como um arquivo de texto.
    # 'index=False' evita que ele salve uma coluna extra de numeração de linhas que não precisamos.
    # 'float_format='%.4f'' garante que os números decimais terão no máximo 4 casas após a vírgula.
    dados_transformados.to_csv(nome_saida, sep='\t', decimal=',', index=False, float_format='%.4f')

    # Imprime uma mensagem final na tela para o usuário saber que o trabalho acabou com sucesso. O '\n' pula uma linha antes do texto para ficar mais organizado na tela.
    print(f"\nProcesso concluído! O arquivo '{nome_saida}' foi gerado mantendo o cabeçalho.")