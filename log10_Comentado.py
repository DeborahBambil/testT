# O comando 'import' traz ferramentas externas (bibliotecas) para dentro do nosso código.
# 'pandas' é uma ferramenta incrível para trabalhar com tabelas e planilhas. 'as pd' é um apelido curto para ela.
import pandas as pd
# 'numpy' traz superpoderes matemáticos para o Python (como calcular logaritmos). Apelidamos de 'np'.
import numpy as np
# 'os' é a biblioteca que permite ao Python conversar com o sistema do seu computador (como checar se um arquivo existe).
import os
# 'ast' é uma ferramenta que ajuda o Python a ler um texto e entender se ele tem a estrutura de um código (como ler uma lista que está escrita em texto).
import ast

# Cria uma "caixinha" (variável) chamada 'lista_path' e guarda o texto 'lista.txt' nela.
# [0 espacos] Define o nome ou caminho padrao do arquivo de texto que contem a lista de variaveis alvo.
lista_path = 'lista.txt'

# O 'if' (Se) verifica uma condição. Aqui, usamos 'not' (Não) junto com 'os.path.exists' (o arquivo existe?).
# Na prática: "Se o arquivo lista.txt NÃO existir, faça o seguinte...".
# [0 espacos] Verifica se o arquivo 'lista.txt' realmente existe.
if not os.path.exists(lista_path):
    # O 'print' mostra uma mensagem de erro na tela do computador.
    print(f"Erro: O arquivo {lista_path} não foi encontrado!")
# O 'else' (Senão) diz o que fazer se a condição acima for falsa (ou seja, se o arquivo EXISTIR, o programa vem para cá).
else:
    # 'with open' abre o arquivo em modo de leitura ('r' de read). O 'encoding' ajuda a ler caracteres especiais e acentos.
    # O 'as f' simplesmente dá o apelido 'f' para o nosso arquivo aberto.
    # [4 espacos] Abre o arquivo 'lista.txt' e normaliza os símbolos de micro.
    with open(lista_path, 'r', encoding='utf-8') as f:
        # Isso é uma forma rápida de ler todas as linhas do arquivo de uma vez. O 'strip()' tira os espaços em branco que sobram no começo ou fim.
        # O 'replace' procura símbolos esquisitos de formatação e troca pelo símbolo correto de micro (µ) para padronizar.
        variaveis_alvo = [linha.strip().replace('Ã‚Âµm', 'µm').replace('Âµm', 'µm') for linha in f if linha.strip()]

    # O 'input' pausa o programa, faz uma pergunta na tela e espera o usuário digitar o nome do arquivo que quer analisar.
    # [4 espacos] Pede para o usuario digitar o nome do arquivo de entrada.
    nome_arquivo = input("Digite o nome do arquivo de entrada: ")

    # Verifica novamente se o NOVO arquivo que o usuário acabou de digitar realmente existe.
    if not os.path.exists(nome_arquivo):
        print(f"Erro: O arquivo {nome_arquivo} não foi encontrado!")
    # Se o arquivo de entrada existir, continuamos.
    else:
        # Abre o arquivo de entrada apenas para espiar a primeira linha.
        # [8 espacos] Detecta se o arquivo possui cabeçalho duplo (MultiIndex) ou simples.
        with open(nome_arquivo, 'r', encoding='latin-1') as f:
            # 'readline()' lê apenas a primeira linha do arquivo e para.
            linha1 = f.readline()
        
        # Cria uma regra para o cabeçalho (os títulos das colunas). Ele tenta adivinhar se o cabeçalho tem uma linha (0) ou duas linhas ([0, 1]) olhando se há formatações específicas na primeira linha.
        # Se a linha contiver tabs e não parecer uma string de tupla, assume-se MultiIndex [0, 1]
        header_choice = [0, 1] if '\t' in linha1 and not "('" in linha1 else 0
        
        # 'pd.read_csv' usa o pandas para ler o arquivo de texto e transformá-lo numa tabela virtual (chamada DataFrame).
        # Ele avisa que as colunas são separadas por espaços (tabulação='\t') e que os números decimais usam vírgula (decimal=',').
        dados = pd.read_csv(nome_arquivo, sep='\t', header=header_choice, decimal=',', encoding='latin-1')
        
        # Cria uma tabela totalmente vazia com a mesma quantidade de linhas da original. Ela vai guardar nossos dados transformados no final.
        dados_finais = pd.DataFrame(index=dados.index)

        # Cria um 'set' (um conjunto como se fosse uma sacola sem itens repetidos) e um 'dicionário' (para guardar informações em pares) vazios.
        # [8 espacos] Etapa 1: Mapear colunas e identificar bases para transformação (Regra do Par)
        bases_para_transformar = set()
        mapeamento_colunas = {}

        # O 'for' (Para cada) é um laço de repetição. Ele vai olhar, uma por uma, cada coluna (col) da nossa tabela de dados.
        for col in dados.columns:
            # Transforma o nome da coluna em texto puro ('str').
            col_str = str(col)
            # O 'try' (Tentar) manda o Python tentar executar o bloco abaixo. Se der algum erro estranho, ele não trava, pula para o 'except'.
            try:
                # Verifica se a coluna tem um título duplo (tupla).
                # Caso o pandas tenha lido como MultiIndex (Tupla real)
                if isinstance(col, tuple):
                    # Junta as duas partes do título com um traço no meio.
                    nome_completo = f"{col[0]} - {col[1]}"
                    nome_base = str(col[1])
                # Senão se ('elif') o texto do título começar com parênteses...
                # Caso o cabeçalho venha como string de tupla "('A', 'B')"
                elif col_str.startswith("("):
                    # Transforma esse texto com parênteses em um par de palavras real usando a ferramenta 'ast'.
                    par = ast.literal_eval(col_str)
                    nome_completo = f"{par[0]} - {par[1]}"
                    nome_base = str(par[1])
                # Senão ('else'), é um título simples de uma linha só.
                else:
                    nome_completo = col_str
                    nome_base = col_str
            # Se deu erro no meio da tentativa de descobrir o título, ele apenas copia o texto bruto.
            except:
                nome_completo = col_str
                nome_base = col_str
            
            # Guarda as informações do nome que descobrimos no nosso dicionário.
            mapeamento_colunas[col] = {"completo": nome_completo, "base": nome_base}
            
            # Limpa o texto, trocando os caracteres bagunçados pelo símbolo de micro (µ) correto.
            # Normalização para busca
            n_busca = nome_completo.replace('Âµm', 'µm').replace('Ã‚Âµm', 'µm')
            b_busca = nome_base.replace('Âµm', 'µm').replace('Ã‚Âµm', 'µm')

            # Verifica se o nome da nossa coluna atual está dentro daquela lista de variáveis que o usuário colocou no arquivo 'lista.txt'.
            # Se estiver na lista, marcamos essa 'base' (variável) para sofrer LOG10 em todos os pares
            if any(v.replace('Âµm', 'µm') in n_busca for v in variaveis_alvo) or \
               any(v.replace('Âµm', 'µm') in b_busca for v in variaveis_alvo):
                # Se estiver na lista, nós adicionamos essa coluna na nossa "sacola" de variáveis que precisam ser transformadas com cálculo matemático.
                bases_para_transformar.add(b_busca)

        # Agora fazemos um novo laço de repetição. Vamos olhar todas as colunas de novo, mas agora para fazer os cálculos.
        # [8 espacos] Etapa 2: Aplicar a transformação
        for col in dados.columns:
            # Resgata o nome limpo da coluna que guardamos no dicionário.
            info = mapeamento_colunas[col]
            b_normalizada = info["base"].replace('Âµm', 'µm').replace('Ã‚Âµm', 'µm')

            # Se esta coluna específica estiver na nossa "sacola" de variáveis marcadas para transformação...
            if b_normalizada in bases_para_transformar:
                # Troca vírgulas por pontos (que é como a matemática do Python funciona) e força todos os dados a virarem números de verdade para podermos calcular.
                # Converte para numérico e aplica LOG10 em valores > 0
                valores = pd.to_numeric(dados[col].astype(str).str.replace(',', '.'), errors='coerce')
                
                # A ferramenta 'apply' aplica uma regra em todos os números da coluna. 
                # A regra ('lambda x') diz: Se o número for maior que 0 e existir, calcule o logaritmo na base 10 ('np.log10(x)'). Senão, deixe como está.
                transformados = valores.apply(lambda x: np.log10(x) if pd.notnull(x) and x > 0 else x)
                
                # Salva esses novos números transformados na nossa tabela vazia.
                dados_finais[col] = transformados
                
                # Mostra na tela que a mágica foi feita para esta coluna.
                print(f"Variavel: {info['completo']} -> TRANSFORMADA (Regra do Par: {b_normalizada})")
            
            # Senão ('else'), se a coluna não foi marcada para transformação...
            else:
                # Apenas copia os números originais sem alterar nada e guarda na tabela nova.
                dados_finais[col] = dados[col]
                # Mostra na tela que não mexeu nesta coluna.
                print(f"Variavel: {info['completo']} -> Mantida original")

        # Garante que as colunas da nova tabela tenham exatamente os mesmos nomes da tabela original.
        # [8 espacos] Salva mantendo a estrutura original
        dados_finais.columns = dados.columns
        
        # Cria o nome do arquivo final apagando '.txt' do nome original e colando '_log10.txt' no final.
        nome_saida = nome_arquivo.replace('.txt', '') + '_log10.txt'
        
        # 'to_csv' pega a nossa tabela virtual com todos os resultados e a salva no seu computador como um arquivo de texto. 'float_format' pede para usar 4 casas decimais após a vírgula.
        dados_finais.to_csv(nome_saida, sep='\t', decimal=',', index=False, float_format='%.4f')
        
        # Pula uma linha (\n) e avisa o usuário que o programa terminou com sucesso.
        print(f"\nSucesso! Arquivo '{nome_saida}' gerado com transformações pareadas.")