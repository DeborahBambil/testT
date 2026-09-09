import pandas as pd # [0 espacos] Importa a biblioteca pandas, essencial para ler e manipular tabelas de dados.
from scipy.stats import levene # [0 espacos] Importa a funcao levene, para comparar a variancia entre grupos independentes.
from scipy.stats import ttest_ind # [0 espacos] Importa a funcao ttest_ind, para comparar as medias de dois grupos independentes.

# [0 espacos] Solicita ao usuario que digite o nome do arquivo de texto (com a extensao .txt).
nome_arquivo = input("Digite o nome do arquivo de entrada (ex: input.txt): ") # [0 espacos] Guarda o nome digitado para usar na leitura.

# [0 espacos] Inspeciona a primeira linha do arquivo para descobrir se ele veio do script original ou do LOG10.
with open(nome_arquivo, 'r', encoding='latin-1') as arquivo: # [0 espacos] Abre apenas para checar o topo.
    primeira_linha = arquivo.readline() # [4 espacos] Le apenas a primeira linha do arquivo de texto.
    
# [0 espacos] Se a primeira linha contiver uma tupla em texto, significa que o arquivo tem apenas 1 linha de cabecalho.
if "('" in primeira_linha: # [0 espacos] Inicia a condicao para inspecionar os caracteres da linha lida.
    n_linhas_cabecalho = 0 # [4 espacos] Avisa ao Pandas para ler apenas a primeira linha como cabecalho.
else: # [0 espacos] Caminho alternativo caso nao possua os caracteres.
    n_linhas_cabecalho = [0, 1] # [4 espacos] Avisa ao Pandas que as duas primeiras linhas formam o cabecalho.
    
# [0 espacos] Le o arquivo de texto informado separando as colunas pelo espaco de tabulacao ('\t').
# [0 espacos] decimal=',' garante que os numeros com virgula sejam compreendidos corretamente como decimais.
# [0 espacos] encoding='latin-1' resolve o erro de leitura de caracteres especiais (como o simbolo de micro).
dados = pd.read_csv(nome_arquivo, sep='\t', header=n_linhas_cabecalho, decimal=',', encoding='latin-1') # [0 espacos] Executa a leitura inteligente.

# [0 espacos] Filtra as colunas para remover indices automaticos (espacos vazios que o Pandas chama de 'Unnamed').
colunas_validas = [col for col in dados.columns if 'Unnamed' not in str(col)] # [0 espacos] Mantem apenas os pares reais.

# [0 espacos] Define o nome fixo do arquivo de saida.
nome_saida = 'Resultado_Levene.txt' # [0 espacos] Define o nome do output.

# [0 espacos] Abre um arquivo de texto no modo de escrita ('w') para salvar o relatorio final.
with open(nome_saida, 'w', encoding='latin-1') as arquivo_saida: # [0 espacos] Tudo que gravarmos aqui sera salvo no arquivo.

    # [4 espacos] Cria um laco de repeticao (for) para passar apenas pelas colunas VALIDAS de duas em duas (pares).
    for i in range(0, len(colunas_validas), 2): # [4 espacos] Inicia o laco com o passo '2' para pegar sempre um par.
        
        # [8 espacos] Garante que nao vamos tentar ler uma coluna que nao existe caso o numero total seja impar.
        if i + 1 < len(colunas_validas): # [8 espacos] Verifica se existe uma segunda coluna para formar o par.
            
            # [12 espacos] Identifica as coordenadas das duas colunas que serao comparadas.
            coluna1 = colunas_validas[i] # [12 espacos] Pega a referencia da primeira coluna do par.
            coluna2 = colunas_validas[i+1] # [12 espacos] Pega a referencia da segunda coluna do par.
            
            # [12 espacos] Extrai os titulos (Amostra e Variavel) individualmente para CADA coluna.
            if isinstance(coluna1, tuple): # [12 espacos] Se o cabecalho for uma tupla original (2 linhas puras).
                amostra1 = coluna1[0] # [16 espacos] Isola a amostra da primeira coluna.
                variavel1 = coluna1[1] # [16 espacos] Isola a variavel da primeira coluna.
                amostra2 = coluna2[0] # [16 espacos] Isola a amostra da segunda coluna.
                variavel2 = coluna2[1] # [16 espacos] Isola a variavel da segunda coluna.
            else: # [12 espacos] Se o cabecalho for uma unica linha de texto (gerada pelo output_dados_mistos).
                titulos1 = eval(coluna1) # [16 espacos] Converte o texto da primeira coluna de volta em tupla.
                titulos2 = eval(coluna2) # [16 espacos] Converte o texto da segunda coluna de volta em tupla.
                amostra1 = titulos1[0] # [16 espacos] Isola a amostra da primeira coluna.
                variavel1 = titulos1[1] # [16 espacos] Isola a variavel da primeira coluna.
                amostra2 = titulos2[0] # [16 espacos] Isola a amostra da segunda coluna.
                variavel2 = titulos2[1] # [16 espacos] Isola a variavel da segunda coluna.
            
            # [12 espacos] Isola os valores e remove os vazios (NaN) de cada coluna para evitar erros no calculo.
            valores1 = dados[coluna1].dropna() # [12 espacos] Limpa os dados do primeiro grupo.
            valores2 = dados[coluna2].dropna() # [12 espacos] Limpa os dados do segundo grupo.
            
            # [12 espacos] O teste exige dados suficientes. Vamos garantir que cada grupo tenha pelo menos 3 valores.
            if len(valores1) >= 3 and len(valores2) >= 3: # [12 espacos] Inicia a estrutura condicional para grupos validos.
                
                # [16 espacos] Aplica o Teste de Levene nos dois grupos limpos para verificar a igualdade das variancias.
                estatistica_lev, valor_p_lev = levene(valores1, valores2) # [16 espacos] Salva os dois resultados em variaveis separadas.
                
                # [16 espacos] Monta o texto de cabecalho informando exatamente quem esta sendo comparado com quem.
                texto_comparacao = f"Comparando: {amostra1} ({variavel1}) VS {amostra2} ({variavel2})" # [16 espacos] Cria a frase.
                print(texto_comparacao) # [16 espacos] Exibe a frase na tela.
                arquivo_saida.write(texto_comparacao + "\n") # [16 espacos] Salva a frase no arquivo txt.
                
                # [16 espacos] Exibe e salva o valor da Estatistica W (Levene), formatado para 4 casas decimais.
                print(f"Estatistica W (Levene): {estatistica_lev:.4f}") # [16 espacos] Exibe a variavel cortando decimais extras.
                arquivo_saida.write(f"Estatistica W (Levene): {estatistica_lev:.4f}\n") # [16 espacos] Salva no arquivo txt.
                
                # [16 espacos] Exibe e salva o valor-p (Levene) em notacao cientifica para nao zerar.
                print(f"Valor-p (Levene): {valor_p_lev:.4e}") # [16 espacos] Formata em potencia de base 10.
                arquivo_saida.write(f"Valor-p (Levene): {valor_p_lev:.4e}\n") # [16 espacos] Salva no arquivo txt.
                
                # [16 espacos] Estrutura condicional para interpretar o valor-p de Levene com significancia de 5% (0.05).
                if valor_p_lev > 0.05: # [16 espacos] Inicia uma sub-condicao. Tudo com 20 espacos ocorre se for verdadeiro.
                    
                    # [20 espacos] Se for maior que 0.05, as variancias sao estatisticamente iguais.
                    print("Conclusao (Levene): As variancias sao iguais (Nao rejeita a Hipotese Nula).\n") # [20 espacos] Imprime.
                    arquivo_saida.write("Conclusao (Levene): As variancias sao iguais (Nao rejeita a Hipotese Nula).\n\n") # [20 espacos] Salva.
                    
                    # [20 espacos] Como as variancias sao iguais, aplicamos o Teste T Independente padrao.
                    estatistica_t, valor_p_t = ttest_ind(valores1, valores2) # [20 espacos] Executa o teste padrao.
                    
                    # [20 espacos] Exibe e salva a Estatistica t e o Valor-p.
                    print(f"Estatistica t (Padrao): {estatistica_t:.4f}") # [20 espacos] Exibe a estatistica t.
                    arquivo_saida.write(f"Estatistica t (Padrao): {estatistica_t:.4f}\n") # [20 espacos] Salva a estatistica t.
                    print(f"Valor-p (Teste T): {valor_p_t:.4e}") # [20 espacos] Exibe o valor-p elevado.
                    arquivo_saida.write(f"Valor-p (Teste T): {valor_p_t:.4e}\n") # [20 espacos] Salva o valor-p.
                    
                    if valor_p_t > 0.05: # [20 espacos] Interpreta o valor-p do Teste T.
                        print("Conclusao (Teste T): As medias sao iguais (Nao rejeita a Hipotese Nula).\n") # [24 espacos] Imprime conclusao final.
                        arquivo_saida.write("Conclusao (Teste T): As medias sao iguais (Nao rejeita a Hipotese Nula).\n\n") # [24 espacos] Salva conclusao final.
                    else: # [20 espacos] Caminho alternativo.
                        print("Conclusao (Teste T): As medias sao diferentes (Rejeita a Hipotese Nula).\n") # [24 espacos] Imprime conclusao final.
                        arquivo_saida.write("Conclusao (Teste T): As medias sao diferentes (Rejeita a Hipotese Nula).\n\n") # [24 espacos] Salva conclusao final.
                        
                else: # [16 espacos] Caminho alternativo caso variancias sejam diferentes (< 0.05).
                    
                    # [20 espacos] Se for menor ou igual a 0.05, as variancias sao estatisticamente diferentes.
                    print("Conclusao (Levene): As variancias sao diferentes (Rejeita a Hipotese Nula).\n") # [20 espacos] Imprime.
                    arquivo_saida.write("Conclusao (Levene): As variancias sao diferentes (Rejeita a Hipotese Nula).\n\n") # [20 espacos] Salva.
                    
                    # [20 espacos] Como as variancias sao diferentes, aplicamos o Teste T de Welch (equal_var=False).
                    estatistica_t, valor_p_t = ttest_ind(valores1, valores2, equal_var=False) # [20 espacos] Executa Welch.
                    
                    # [20 espacos] Exibe e salva a Estatistica t e o Valor-p.
                    print(f"Estatistica t (Welch): {estatistica_t:.4f}") # [20 espacos] Exibe a estatistica t.
                    arquivo_saida.write(f"Estatistica t (Welch): {estatistica_t:.4f}\n") # [20 espacos] Salva a estatistica t.
                    print(f"Valor-p (Teste de Welch): {valor_p_t:.4e}") # [20 espacos] Exibe o valor-p elevado.
                    arquivo_saida.write(f"Valor-p (Teste de Welch): {valor_p_t:.4e}\n") # [20 espacos] Salva o valor-p.
                    
                    if valor_p_t > 0.05: # [20 espacos] Interpreta o valor-p do Teste de Welch.
                        print("Conclusao (Teste de Welch): As medias sao iguais (Nao rejeita a Hipotese Nula).\n") # [24 espacos] Imprime conclusao final.
                        arquivo_saida.write("Conclusao (Teste de Welch): As medias sao iguais (Nao rejeita a Hipotese Nula).\n\n") # [24 espacos] Salva conclusao final.
                    else: # [20 espacos] Caminho alternativo.
                        print("Conclusao (Teste de Welch): As medias sao diferentes (Rejeita a Hipotese Nula).\n") # [24 espacos] Imprime conclusao final.
                        arquivo_saida.write("Conclusao (Teste de Welch): As medias sao diferentes (Rejeita a Hipotese Nula).\n\n") # [24 espacos] Salva conclusao final.
                
        else: # [8 espacos] Caminho alternativo caso os dados sejam insuficientes.
            alerta = f"Comparando: {amostra1} ({variavel1}) VS {amostra2} ({variavel2}) ignorada (dados insuficientes).\n" # [12 espacos] Monta o alerta.
            print(alerta) # [12 espacos] Imprime alerta na tela.
            arquivo_saida.write(alerta + "\n") # [12 espacos] Salva alerta no arquivo.

# [0 espacos] Informa que o arquivo de saida foi gerado com sucesso.
print(f"Processo concluido! O relatorio completo foi salvo em '{nome_saida}'.\n") # [0 espacos] Exibe o nome do arquivo gerado.

# [0 espacos] Mantem a janela do terminal aberta no Windows para os alunos lerem os resultados.
input("Pressione Enter para fechar o programa...") # [0 espacos] O script pausa aqui ate alguem apertar a tecla Enter.