# O comando 'import' traz ferramentas (bibliotecas) para dentro do nosso código[cite: 3].
# 'pandas' é a principal ferramenta do Python para lidar com tabelas. O 'as pd' cria um apelido curto para não termos que digitar "pandas" toda hora[cite: 3].
import pandas as pd # [0 espacos] Importa a biblioteca pandas, essencial para ler e manipular tabelas de dados.

# 'from ... import ...' pega uma ferramenta muito específica (mannwhitneyu) de dentro de uma caixa maior de ferramentas estatísticas (scipy.stats)[cite: 3].
from scipy.stats import mannwhitneyu # [0 espacos] Importa a funcao mannwhitneyu, para comparar dois grupos independentes.

# O comando 'input' pausa o programa, mostra a mensagem na tela e espera o aluno digitar algo. O que for digitado será guardado na "caixinha" (variável) chamada 'nome_arquivo'[cite: 3].
# [0 espacos] Solicita ao usuario que digite o nome do arquivo de texto (com a extensao .txt).
nome_arquivo = input("Digite o nome do arquivo de entrada (ex: input.txt): ") # [0 espacos] Guarda o nome digitado para usar na leitura.

# 'with open' é a forma segura de abrir arquivos no Python. O 'r' significa que vamos apenas ler (read) o arquivo. 'as arquivo' é o apelido que damos a este arquivo aberto[cite: 3].
# [0 espacos] Inspeciona a primeira linha do arquivo para descobrir a estrutura do cabecalho.
with open(nome_arquivo, 'r', encoding='latin-1') as arquivo: # [0 espacos] Abre apenas para checar o topo.
    
    # 'readline()' é um comando que lê estritamente a primeira linha do texto e para por aí[cite: 3].
    primeira_linha = arquivo.readline() # [4 espacos] Le apenas a primeira linha do arquivo de texto.
    
# O comando 'if' significa "Se". O 'in' significa "dentro". Estamos perguntando: "Se o símbolo "('" estiver dentro do texto da primeira linha..."[cite: 3]
# [0 espacos] Se a primeira linha contiver uma tupla em texto, significa que o arquivo tem apenas 1 linha de cabecalho.
if "('" in primeira_linha: # [0 espacos] Inicia a condicao para inspecionar os caracteres da linha lida.
    
    # Criamos a variável com o número 0. Para o Python, a primeira linha é sempre a linha zero[cite: 3].
    n_linhas_cabecalho = 0 # [4 espacos] Avisa ao Pandas para ler apenas a primeira linha como cabecalho.

# O 'else' significa "Senão". É o caminho que o código toma se a condição do 'if' for mentira[cite: 3].
else: # [0 espacos] Caminho alternativo caso nao possua os caracteres.
    
    # Usamos os colchetes [] para criar uma lista. Aqui indicamos as linhas 0 e 1[cite: 3].
    n_linhas_cabecalho = [0, 1] # [4 espacos] Avisa ao Pandas que as duas primeiras linhas formam o cabecalho.
    
# 'pd.read_csv' usa a ferramenta pandas para pegar o arquivo de texto no seu computador e transformar em uma tabela virtual interativa. Os argumentos dentro dos parênteses (sep, header, decimal) ensinam o Python como ler as quebras de coluna e os números[cite: 3].
# [0 espacos] Le o arquivo de texto informado separando as colunas pelo espaco de tabulacao ('\t').
# [0 espacos] decimal=',' garante que os numeros com virgula sejam compreendidos corretamente como decimais.
# [0 espacos] encoding='latin-1' resolve o erro de leitura de caracteres especiais (como o simbolo de micro).
dados = pd.read_csv(nome_arquivo, sep='\t', header=n_linhas_cabecalho, decimal=',', encoding='latin-1') # [0 espacos] Executa a leitura inteligente.

# Esta linha usa um conceito chamado "List Comprehension" (Compreensão de Lista). É um 'for' de uma linha só: "Crie uma lista com a coluna ('col') PARA CADA coluna ('for col') nos dados, SE ('if') a palavra 'Unnamed' NÃO ('not in') estiver no nome"[cite: 3].
# [0 espacos] Filtra as colunas para remover indices automaticos (espacos vazios que o Pandas chama de 'Unnamed').
colunas_validas = [col for col in dados.columns if 'Unnamed' not in str(col)] # [0 espacos] Mantem apenas os pares reais.

# Abre um arquivo de texto, mas agora usando 'w' (write), que significa "escrever". Se o arquivo não existir, o Python cria um novo em branco para você[cite: 3].
# [0 espacos] Abre um arquivo de texto no modo de escrita ('w') para salvar o relatorio final.
with open('Resultado_Mann_Whitney.txt', 'w') as arquivo_saida: # [0 espacos] Tudo que gravarmos aqui sera salvo no arquivo.

    # O comando 'for' cria um laço de repetição. A ferramenta 'range(0, tamanho, 2)' gera números pulando de 2 em 2 (0, 2, 4, 6...). 'len' serve para descobrir o tamanho total da lista[cite: 3].
    # [4 espacos] Cria um laco de repeticao (for) para passar apenas pelas colunas VALIDAS de duas em duas (pares).
    for i in range(0, len(colunas_validas), 2): # [4 espacos] Inicia o laco com o passo '2' para pegar sempre um par.
        
        # 'if' verifica se o próximo número (i + 1) é menor que o tamanho total ('len') da lista, garantindo que não vamos buscar uma coluna que não existe[cite: 3].
        # [8 espacos] Garante que nao vamos tentar ler uma coluna que nao existe caso o numero total seja impar.
        if i + 1 < len(colunas_validas): # [8 espacos] Verifica se existe uma segunda coluna para formar o par.
            
            # Usamos os colchetes [] para "pescar" um item específico dentro da lista usando sua posição (i)[cite: 3].
            # [12 espacos] Identifica as coordenadas das duas colunas que serao comparadas.
            coluna1 = colunas_validas[i] # [12 espacos] Pega a referencia da primeira coluna do par.
            coluna2 = colunas_validas[i+1] # [12 espacos] Pega a referencia da segunda coluna do par.
            
            # 'isinstance' é uma ferramenta do Python que faz uma pergunta: "A coluna1 é do tipo 'tuple' (um par de informações agrupadas)?"[cite: 3].
            # [12 espacos] Extrai os titulos (Amostra e Variavel) individualmente para CADA coluna.
            if isinstance(coluna1, tuple): # [12 espacos] Se o cabecalho for uma tupla original (2 linhas puras).
                # Pega o primeiro item do grupo (posição 0) e o segundo (posição 1)[cite: 3].
                amostra1 = coluna1[0] # [16 espacos] Isola a amostra da primeira coluna.
                variavel1 = coluna1[1] # [16 espacos] Isola a variavel da primeira coluna.
                amostra2 = coluna2[0] # [16 espacos] Isola a amostra da segunda coluna.
                variavel2 = coluna2[1] # [16 espacos] Isola a variavel da segunda coluna.
            
            # Senão (else), se o cabeçalho for apenas um texto comum[cite: 3]...
            else: # [12 espacos] Se o cabecalho for uma unica linha de texto (gerada pelo output_dados_mistos).
                
                # A ferramenta 'eval' avisa o Python: "Leia esse texto como se fosse um código de verdade", transformando o texto de volta em um par agrupado[cite: 3].
                titulos1 = eval(coluna1) # [16 espacos] Converte o texto da primeira coluna de volta em tupla.
                titulos2 = eval(coluna2) # [16 espacos] Converte o texto da segunda coluna de volta em tupla.
                amostra1 = titulos1[0] # [16 espacos] Isola a amostra da primeira coluna.
                variavel1 = titulos1[1] # [16 espacos] Isola a variavel da primeira coluna.
                amostra2 = titulos2[0] # [16 espacos] Isola a amostra da segunda coluna.
                variavel2 = titulos2[1] # [16 espacos] Isola a variavel da segunda coluna.
            
            # 'dropna()' é um comando do Pandas que joga fora todas as linhas que estão em branco ou vazias daquela coluna[cite: 3].
            # [12 espacos] Isola os valores e remove os vazios (NaN) de cada coluna para evitar erros no calculo.
            valores1 = dados[coluna1].dropna() # [12 espacos] Limpa os dados do primeiro grupo.
            valores2 = dados[coluna2].dropna() # [12 espacos] Limpa os dados do segundo grupo.
            
            # O 'if' (Se) verifica múltiplas coisas ao mesmo tempo usando o 'and' (E). O 'len' conta quantos valores sobraram. Lê-se: "Se o tamanho do grupo 1 for maior ou igual (>=) a 3 E o tamanho do grupo 2 for maior ou igual a 3"[cite: 3].
            # [12 espacos] O teste exige dados suficientes. Vamos garantir que cada grupo tenha pelo menos 3 valores.
            if len(valores1) >= 3 and len(valores2) >= 3: # [12 espacos] Inicia a estrutura condicional para grupos validos.
                
                # Aqui nós chamamos a ferramenta 'mannwhitneyu' que importamos lá no começo. Ela faz a conta matemática e nos devolve dois resultados, que salvamos em duas variáveis separadas por vírgula[cite: 3].
                # [16 espacos] Aplica o teste de Mann-Whitney U nos dois grupos limpos.
                estatistica, valor_p = mannwhitneyu(valores1, valores2) # [16 espacos] Salva os dois resultados em variaveis separadas.
                
                # O 'f' antes das aspas permite que coloquemos as variáveis (como {amostra1}) diretamente dentro do texto, substituindo pela palavra real[cite: 3].
                # [16 espacos] Monta o texto de cabecalho informando exatamente quem esta sendo comparado com quem.
                texto_comparacao = f"Comparando: {amostra1} ({variavel1}) VS {amostra2} ({variavel2})" # [16 espacos] Cria a frase.
                
                # 'print' mostra essa frase na tela preta do computador[cite: 3].
                print(texto_comparacao) # [16 espacos] Exibe a frase na tela.
                
                # '.write' pega a mesma frase e escreve ela de verdade dentro do nosso arquivo de texto. O '\n' no final funciona como a tecla "Enter", pulando para a linha de baixo[cite: 3].
                arquivo_saida.write(texto_comparacao + "\n") # [16 espacos] Salva a frase no arquivo txt.
                
                # O ': .4f' formata o número matemático limitando ele a ficar bonitinho com apenas 4 casas decimais ('f' de float)[cite: 3].
                # [16 espacos] Exibe e salva o valor da Estatistica U, formatado para 4 casas decimais.
                print(f"Estatistica U: {estatistica:.4f}") # [16 espacos] Exibe a variavel cortando decimais extras.
                arquivo_saida.write(f"Estatistica U: {estatistica:.4f}\n") # [16 espacos] Salva no arquivo txt.
                
                # O ': .4e' formata o número para notação científica ('e'). Essencial quando o número é minúsculo (ex: 0.00000001)[cite: 3].
                # [16 espacos] Exibe e salva o valor-p em notacao cientifica para evitar zerar numeros pequenos.
                print(f"Valor-p: {valor_p:.4e}") # [16 espacos] Formata em potencia de base 10.
                arquivo_saida.write(f"Valor-p: {valor_p:.4e}\n") # [16 espacos] Salva no arquivo txt.
                
                # O 'if' (Se) verifica qual foi a conclusão do teste. ' > ' significa "maior que"[cite: 3].
                # [16 espacos] Estrutura condicional para interpretar o valor-p com base no nivel de significancia de 5% (0.05).
                if valor_p > 0.05: # [16 espacos] Inicia uma sub-condicao. Tudo com 20 espacos ocorre se a condicao for verdadeira.
                    
                    # 'print' apenas joga a frase na tela[cite: 3].
                    # [20 espacos] Se for maior que 0.05, nao ha evidencias para afirmar que os grupos sao diferentes.
                    print("Conclusao: Nao ha diferenca significativa entre os grupos (Nao rejeita a Hipotese Nula).\n") # [20 espacos] Imprime a conclusao na tela.
                    
                    # '.write' grava a frase no relatório gerado[cite: 3].
                    arquivo_saida.write("Conclusao: Nao ha diferenca significativa entre os grupos (Nao rejeita a Hipotese Nula).\n\n") # [20 espacos] Salva no arquivo txt.
                
                # 'else' (Senão), que engloba o caminho caso o valor seja menor ou igual a 0.05[cite: 3].
                else: # [16 espacos] Caminho alternativo caso a afirmacao acima seja falsa (menor ou igual a 0.05).
                    
                    # [20 espacos] Se for menor ou igual a 0.05, a diferenca entre os dois grupos e significante.
                    print("Conclusao: Ha diferenca significativa entre os grupos (Rejeita a Hipotese Nula).\n") # [20 espacos] Imprime a conclusao alternativa.
                    arquivo_saida.write("Conclusao: Ha diferenca significativa entre os grupos (Rejeita a Hipotese Nula).\n\n") # [20 espacos] Salva no arquivo txt.
                    
            # 'else' (Senão). Este é o caminho se os grupos não tiverem dados suficientes (ex: só tem 2 linhas válidas)[cite: 3].
            else: # [12 espacos] Caminho alternativo (caso alguma coluna do par tenha menos de 3 numeros validos).
                alerta = f"Comparando: {amostra1} ({variavel1}) VS {amostra2} ({variavel2}) ignorada (dados insuficientes).\n" # [16 espacos] Monta o alerta.
                print(alerta) # [16 espacos] Imprime alerta na tela.
                arquivo_saida.write(alerta + "\n") # [16 espacos] Salva alerta no arquivo.

# Fora de todos os laços e repetições, usamos o 'print' para exibir uma mensagem final na tela dizendo que tudo acabou[cite: 3].
# [0 espacos] Informa que o arquivo de saida foi gerado com sucesso.
print("Processo concluido! O relatorio completo foi salvo em 'Resultado_Mann_Whitney.txt'.\n")

# Usamos um 'input' vazio no final só para travar o programa. Assim, a telinha preta não fecha rápido demais antes que os alunos possam ler os resultados finais[cite: 3].
# [0 espacos] Mantem a janela do terminal aberta no Windows para os alunos lerem os resultados.
input("Pressione Enter para fechar o programa...") # [0 espacos] O script pausa aqui ate alguem apertar a tecla Enter.