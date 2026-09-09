# O comando 'import' traz pacotes de ferramentas de fora para o nosso código. O 'pandas' é o melhor pacote para trabalhar com planilhas e tabelas. O 'as pd' é um apelido para não precisarmos digitar a palavra inteira toda vez.
import pandas as pd # [0 espacos] Importa a biblioteca pandas, essencial para ler e manipular tabelas de dados.

# O 'from ... import ...' pega uma ferramenta muito específica (wilcoxon) de dentro de uma caixa maior de estatística (scipy.stats).
from scipy.stats import wilcoxon # [0 espacos] Importa a funcao wilcoxon, para comparar duas amostras pareadas (nao parametricas).

# A função 'input' pausa o programa, mostra a mensagem na tela preta e espera o aluno digitar o nome do arquivo. O nome digitado será guardado na "caixinha" (variável) chamada 'nome_arquivo'.
# [0 espacos] Solicita ao usuario que digite o nome do arquivo de texto (com a extensao .txt).
nome_arquivo = input("Digite o nome do arquivo de entrada (ex: input.txt): ") # [0 espacos] Guarda o nome digitado para usar na leitura.

# 'with open' abre o arquivo de forma segura. O 'r' (read) significa que vamos apenas ler o texto. 'as arquivo' dá o apelido para o arquivo aberto.
# [0 espacos] Inspeciona a primeira linha do arquivo para descobrir a estrutura do cabecalho.
with open(nome_arquivo, 'r', encoding='latin-1') as arquivo: # [0 espacos] Abre apenas para checar o topo.
    
    # 'readline()' lê unicamente a primeira linha de texto do arquivo e para.
    primeira_linha = arquivo.readline() # [4 espacos] Le apenas a primeira linha do arquivo de texto.
    
# O 'if' (Se) verifica uma regra. O 'in' (em/dentro) checa se algo está contido. Lemos: "Se os caracteres "('" estiverem dentro da primeira linha..."
# [0 espacos] Se a primeira linha contiver uma tupla em texto, significa que o arquivo tem apenas 1 linha de cabecalho.
if "('" in primeira_linha: # [0 espacos] Inicia a condicao para inspecionar os caracteres da linha lida.
    
    # Em Python, a contagem sempre começa no zero. Aqui avisamos que o título da tabela está na linha 0.
    n_linhas_cabecalho = 0 # [4 espacos] Avisa ao Pandas para ler apenas a primeira linha como cabecalho.

# O 'else' (Senão) é o caminho alternativo caso a regra do 'if' seja mentira.
else: # [0 espacos] Caminho alternativo caso nao possua os caracteres.
    
    # Os colchetes [] criam uma lista. Avisamos que os títulos da tabela ocupam as linhas 0 e 1 juntas.
    n_linhas_cabecalho = [0, 1] # [4 espacos] Avisa ao Pandas que as duas primeiras linhas formam o cabecalho.
    
# 'pd.read_csv' usa a ferramenta do pandas para pegar o seu arquivo e transformá-lo numa tabela virtual. 'sep' diz que as colunas são separadas pelo espaço da tecla Tab, e 'decimal' avisa que os números usam vírgula.
# [0 espacos] Le o arquivo de texto informado separando as colunas pelo espaco de tabulacao ('\t').
# [0 espacos] decimal=',' garante que os numeros com virgula sejam compreendidos corretamente como decimais.
# [0 espacos] encoding='latin-1' resolve o erro de leitura de caracteres especiais (como o simbolo de micro).
dados = pd.read_csv(nome_arquivo, sep='\t', header=n_linhas_cabecalho, decimal=',', encoding='latin-1') # [0 espacos] Executa a leitura inteligente.

# Isso varre a nossa tabela inteira procurando por colunas invisíveis ou com erro (que o pandas chama de 'Unnamed') e as joga fora.
# [0 espacos] Filtra as colunas para remover indices automaticos (espacos vazios que o Pandas chama de 'Unnamed').
colunas_validas = [col for col in dados.columns if 'Unnamed' not in str(col)] # [0 espacos] Mantem apenas os pares reais.

# Agora o 'with open' usa a letra 'w' (write / escrever). Isso manda o Python criar um arquivo em branco no seu computador para salvarmos os resultados.
# [0 espacos] Abre um arquivo de texto no modo de escrita ('w') para salvar o relatorio final.
with open('Resultado_Test_Wilcoxon.txt', 'w') as arquivo_saida: # [0 espacos] Tudo que gravarmos aqui sera salvo no arquivo.

    # O laço 'for' cria uma repetição. A ferramenta 'range' vai pular de 2 em 2 colunas, garantindo que a gente sempre analise pares.
    # [4 espacos] Cria um laco de repeticao (for) para passar apenas pelas colunas VALIDAS de duas em duas (pares).
    for i in range(0, len(colunas_validas), 2): # [4 espacos] Inicia o laco com o passo '2' para pegar sempre um par.
        
        # Garante que, se a tabela tiver um número ímpar de colunas, o programa não tente formar um par com uma coluna que não existe.
        # [8 espacos] Garante que nao vamos tentar ler uma coluna que nao existe caso o numero total seja impar.
        if i + 1 < len(colunas_validas): # [8 espacos] Verifica se existe uma segunda coluna para formar o par.
            
            # Pega o nome das colunas usando a posição delas (i).
            # [12 espacos] Identifica as coordenadas das duas colunas que serao comparadas.
            coluna1 = colunas_validas[i] # [12 espacos] Pega a referencia da primeira coluna do par.
            coluna2 = colunas_validas[i+1] # [12 espacos] Pega a referencia da segunda coluna do par.
            
            # 'isinstance' faz uma pergunta: "O título da coluna1 é duplo (uma tupla)?".
            # [12 espacos] Extrai os titulos (Amostra e Variavel) individualmente para CADA coluna.
            if isinstance(coluna1, tuple): # [12 espacos] Se o cabecalho for uma tupla original (2 linhas puras).
                amostra1 = coluna1[0] # [16 espacos] Isola a amostra da primeira coluna.
                variavel1 = coluna1[1] # [16 espacos] Isola a variavel da primeira coluna.
                amostra2 = coluna2[0] # [16 espacos] Isola a amostra da segunda coluna.
                variavel2 = coluna2[1] # [16 espacos] Isola a variavel da segunda coluna.
                
            # Se for uma linha única de texto normal, usamos a ferramenta 'eval', que ensina o Python a ler esse texto como se fosse um par verdadeiro.
            else: # [12 espacos] Se o cabecalho for uma unica linha de texto (gerada pelo output_dados_mistos).
                titulos1 = eval(coluna1) # [16 espacos] Converte o texto da primeira coluna de volta em tupla.
                titulos2 = eval(coluna2) # [16 espacos] Converte o texto da segunda coluna de volta em tupla.
                amostra1 = titulos1[0] # [16 espacos] Isola a amostra da primeira coluna.
                variavel1 = titulos1[1] # [16 espacos] Isola a variavel da primeira coluna.
                amostra2 = titulos2[0] # [16 espacos] Isola a amostra da segunda coluna.
                variavel2 = titulos2[1] # [16 espacos] Isola a variavel da segunda coluna.
            
            # O 'dropna()' vai apagar as linhas vazias. Como o teste é PAREADO, se faltar um dado de um lado, a linha inteira é apagada para os grupos não desalinharem.
            # [12 espacos] O Teste de Wilcoxon exige dados pareados. Isolamos o par e removemos as linhas vazias (NaN) juntas.
            pares_limpos = dados[[coluna1, coluna2]].dropna() # [12 espacos] Limpa os dados garantindo alinhamento perfeito.
            valores1 = pares_limpos[coluna1] # [12 espacos] Separa os dados limpos do primeiro grupo.
            valores2 = pares_limpos[coluna2] # [12 espacos] Separa os dados limpos do segundo grupo.
            
            # O comando 'len' conta quantas linhas sobraram. Precisamos de pelo menos 3 para a matemática não dar erro.
            # [12 espacos] O teste exige dados suficientes. Vamos garantir que tenhamos pelo menos 3 pares de valores validos.
            if len(valores1) >= 3: # [12 espacos] Inicia a estrutura condicional para os pares validos.
                
                # Executa o cálculo estatístico de Wilcoxon. Ele nos devolve dois números que salvamos nessas duas palavras à esquerda.
                # [16 espacos] Aplica o Teste de Wilcoxon nos dois grupos limpos e dependentes.
                estatistica, valor_p = wilcoxon(valores1, valores2) # [16 espacos] Salva os resultados em variaveis separadas.
                
                # O 'f' na frente das aspas deixa você injetar os nomes reais (variáveis) dentro do texto.
                # [16 espacos] Monta o texto informando exatamente quem esta sendo comparado com quem.
                texto_comparacao = f"Comparando: {amostra1} ({variavel1}) VS {amostra2} ({variavel2})" # [16 espacos] Cria a frase.
                
                # 'print' escreve a frase na tela, e o '.write' escreve essa mesma frase dentro do nosso arquivo. O '\n' aperta a tecla Enter para ir para a linha de baixo.
                print(texto_comparacao) # [16 espacos] Exibe a frase na tela.
                arquivo_saida.write(texto_comparacao + "\n") # [16 espacos] Salva a frase no arquivo txt.
                
                # O formato ':.4f' corta as casas decimais extras do número, deixando só 4 números depois da vírgula.
                # [16 espacos] Exibe e salva o valor da Estatistica W, formatado para mostrar apenas 4 casas decimais.
                print(f"Estatistica W: {estatistica:.4f}") # [16 espacos] Exibe a variavel cortando decimais extras.
                arquivo_saida.write(f"Estatistica W: {estatistica:.4f}\n") # [16 espacos] Salva no arquivo txt.
                
                # O formato ':.4e' exibe o número em notação científica, para evitar que números super pequenos pareçam um zero absoluto.
                # [16 espacos] Exibe e salva o valor-p em notacao cientifica (elevado) para evitar zerar numeros pequenos.
                print(f"Valor-p: {valor_p:.4e}") # [16 espacos] Formata em potencia de base 10.
                arquivo_saida.write(f"Valor-p: {valor_p:.4e}\n") # [16 espacos] Salva no arquivo txt.
                
                # Se o valor matemático (valor-p) for maior que 0.05, imprimimos uma conclusão...
                # [16 espacos] Estrutura condicional para interpretar o valor-p com base no nivel de significancia de 5% (0.05).
                if valor_p > 0.05: # [16 espacos] Inicia uma sub-condicao. Tudo com 20 espacos ocorre se a condicao for verdadeira.
                    # [20 espacos] Se for maior que 0.05, nao ha diferenca estatistica entre os pares.
                    print("Conclusao: Nao ha diferenca significativa entre os pares (Nao rejeita a Hipotese Nula).\n") # [20 espacos] Imprime.
                    arquivo_saida.write("Conclusao: Nao ha diferenca significativa entre os pares (Nao rejeita a Hipotese Nula).\n\n") # [20 espacos] Salva.
                    
                # Senão (else), ou seja, se for menor que 0.05, imprimimos a conclusão oposta.
                else: # [16 espacos] Caminho alternativo caso a afirmacao acima seja falsa (menor ou igual a 0.05).
                    # [20 espacos] Se for menor ou igual a 0.05, a diferenca entre os pares e estatisticamente significante.
                    print("Conclusao: Ha diferenca significativa entre os pares (Rejeita a Hipotese Nula).\n") # [20 espacos] Imprime.
                    arquivo_saida.write("Conclusao: Ha diferenca significativa entre os pares (Rejeita a Hipotese Nula).\n\n") # [20 espacos] Salva.
                    
            # Esse é o caminho caso o programa tenha apagado muitas linhas em branco e não tenha sobrado o mínimo de 3 pares.
            else: # [12 espacos] Caminho alternativo (caso o par tenha menos de 3 linhas validas apos remocao de vazios).
                alerta = f"Comparando: {amostra1} ({variavel1}) VS {amostra2} ({variavel2}) ignorada (dados insuficientes).\n" # [16 espacos] Monta o alerta.
                print(alerta) # [16 espacos] Imprime alerta na tela.
                arquivo_saida.write(alerta + "\n") # [16 espacos] Salva alerta no arquivo.

# Informamos na tela que o arquivo de texto foi salvo com sucesso lá na pasta do computador.
# [0 espacos] Informa que o arquivo de saida foi gerado com sucesso.
print("Processo concluido! O relatorio completo foi salvo em 'Resultado_Test_Wilcoxon.txt'.\n")

# Colocamos um comando de 'input' solto no final só para a tela preta travar e ficar esperando. Assim os alunos conseguem ler as respostas antes da tela fechar sozinha.
# [0 espacos] Mantem a janela do terminal aberta no Windows para os alunos lerem os resultados.
input("Pressione Enter para fechar o programa...") # [0 espacos] O script pausa aqui ate alguem apertar a tecla Enter.