# O comando 'import' traz "caixas de ferramentas" prontas para usarmos. 'pandas' é excelente para tabelas. 'as pd' é um apelido para economizar digitação.
import pandas as pd # [0 espacos] Importa a biblioteca pandas, essencial para ler e manipular tabelas de dados.

# 'from ... import ...' pega uma ferramenta muito específica (shapiro) de dentro de uma caixa maior de matemática (scipy.stats).
from scipy.stats import shapiro # [0 espacos] Importa a funcao shapiro, responsavel por realizar o teste estatistico.

# 'input' pausa o programa, exibe a mensagem na tela e espera o usuário digitar. O texto digitado é guardado na "caixinha" (variável) 'nome_arquivo'.
# [0 espacos] Solicita ao usuario que digite o nome do arquivo de texto (com a extensao .txt).
nome_arquivo = input("Digite o nome do arquivo de entrada (ex: input.txt): ") # [0 espacos] Guarda o nome digitado para usar na leitura.

# 'with open' abre o arquivo de forma segura. O 'r' (read) significa que vamos apenas ler. 'as arquivo' dá um apelido temporário a ele.
# [0 espacos] Inspeciona a primeira linha do arquivo para descobrir a estrutura do cabecalho.
with open(nome_arquivo, 'r', encoding='latin-1') as arquivo: # [0 espacos] Abre apenas para checar o topo.
    
    # 'readline()' lê estritamente a primeira linha do texto e para.
    primeira_linha = arquivo.readline() # [4 espacos] Le apenas a primeira linha do arquivo de texto.
    
# O 'if' significa "Se". O 'in' significa "dentro". Pergunta: "Se os caracteres "('" estiverem no texto da primeira linha...".
# [0 espacos] Se a primeira linha contiver uma tupla em texto, significa que o arquivo tem apenas 1 linha de cabecalho.
if "('" in primeira_linha: # [0 espacos] Inicia a condicao para inspecionar os caracteres da linha lida.
    
    # Para o Python, a contagem começa do zero. Isso diz que o título da tabela está na linha 0.
    n_linhas_cabecalho = 0 # [4 espacos] Avisa ao Pandas para ler apenas a primeira linha como cabecalho.

# O 'else' significa "Senão". Se a condição de cima for mentira, o programa faz isso.
else: # [0 espacos] Caminho alternativo caso nao possua os caracteres.
    
    # Os colchetes [] criam uma lista. Indica que os títulos ocupam as linhas 0 e 1 juntas.
    n_linhas_cabecalho = [0, 1] # [4 espacos] Avisa ao Pandas que as duas primeiras linhas formam o cabecalho.

# 'pd.read_csv' é o feitiço do pandas para pegar seu arquivo de texto e transformar numa tabela virtual. 'sep' diz que as colunas são separadas por 'Tab' e 'decimal' avisa que usamos vírgula para números quebrados.
# [0 espacos] Le o arquivo de texto informado separando as colunas pelo espaco de tabulacao ('\t').
# [0 espacos] decimal=',' garante que os numeros com virgula sejam compreendidos corretamente como decimais.
# [0 espacos] encoding='latin-1' resolve o erro de leitura de caracteres especiais (como o simbolo de micro).
dados = pd.read_csv(nome_arquivo, sep='\t', header=n_linhas_cabecalho, decimal=',', encoding='latin-1') # [0 espacos] Executa a leitura inteligente.

# Isso varre os nomes das colunas e joga fora colunas invisíveis ou com erro ('Unnamed'). É um 'for' de uma linha só.
# [0 espacos] Filtra as colunas para remover indices automaticos (espacos vazios que o Pandas chama de 'Unnamed').
colunas_validas = [col for col in dados.columns if 'Unnamed' not in str(col)] # [0 espacos] Mantem apenas as colunas reais.

# Os colchetes vazios [] criam uma lista em branco, como se fosse uma folha de papel nova para anotarmos nomes depois.
# [0 espacos] Cria uma lista vazia para guardar os nomes das variaveis que deram distribuicao NAO normal.
variaveis_nao_normais = [] # [0 espacos] Inicia a lista que vai virar o nosso arquivo de texto no final.

# O 'for' (Para cada) cria um laço de repetição. Ele vai olhar uma coluna de cada vez da nossa tabela.
# [0 espacos] Cria um laco de repeticao (for) para passar por cada uma das colunas validas da nossa tabela.
for coluna in colunas_validas: # [0 espacos] Inicia o laco. Tudo que estiver recuado abaixo sera repetido para cada coluna.
    
    # 'isinstance' faz uma pergunta: "O título desta coluna é uma tupla (um título duplo de duas linhas)?".
    # [4 espacos] Extrai os titulos (Amostra e Variavel) individualmente, suportando ambos os formatos de cabecalho.
    if isinstance(coluna, tuple): # [4 espacos] Se o cabecalho for uma tupla original (2 linhas puras).
        amostra = coluna[0] # [8 espacos] Isola a amostra.
        variavel = coluna[1] # [8 espacos] Isola a variavel.
        
        # O 'f' antes do texto permite colocar o valor das variáveis dentro das chaves {} para montar o nome bonitinho.
        nome_exibicao = f"{amostra} - {variavel}" # [8 espacos] Formata o nome completo.
        
    # Senão (else), caso seja uma linha de texto única....
    else: # [4 espacos] Se o cabecalho for uma unica linha de texto (gerada por scripts de transformacao).
        
        # O 'try' manda o Python "tentar" fazer uma ação que pode dar erro, sem travar o programa.
        try: # [8 espacos] Tenta converter o texto em tupla real.
            
            # 'eval' lê o texto como se fosse um código, separando a amostra da variável.
            titulos = eval(coluna) # [12 espacos] Converte o texto em tupla.
            amostra = titulos[0] # [16 espacos] Isola a amostra.
            variavel = titulos[1] # [16 espacos] Isola a variavel.
            nome_exibicao = f"{amostra} - {variavel}" # [16 espacos] Formata o nome completo.
            
        # 'except' é o plano B: se a tentativa de cima (try) falhar, ele faz o que está aqui.
        except: # [8 espacos] Caminho alternativo caso nao seja tupla.
            
            # Apenas pega o título original transformado em texto (str).
            nome_exibicao = str(coluna) # [12 espacos] Usa o texto da coluna diretamente.
            
    # [4 espacos] Isola os valores pertencentes apenas a coluna atual do laco.
    valores_coluna = dados[coluna] # [4 espacos] Atribui os dados isolados a uma nova variavel temporaria.
    
    # 'dropna()' joga fora todos os buracos em branco (valores ausentes) daquela coluna para não quebrar a matemática.
    # [4 espacos] Remove qualquer valor vazio (NaN) da coluna, evitando que o teste de erro por falta de dados.
    valores_limpos = valores_coluna.dropna() # [4 espacos] Executa a limpeza dos espacos vazios.
    
    # O comando 'len' (de length) conta quantos números sobraram. O teste precisa de maior ou igual (>=) a 3.
    # [4 espacos] O teste de Shapiro-Wilk exige pelo menos 3 numeros. O comando 'len' verifica se temos essa quantidade.
    if len(valores_limpos) >= 3: # [4 espacos] Inicia a estrutura condicional. Tudo com recuo de 8 espacos so ocorre se isso for verdade.
        
        # Chama a ferramenta matemática 'shapiro'. Ela faz o cálculo e nos entrega dois números, guardados separadamente.
        # [8 espacos] Aplica o teste nos dados limpos. Ele devolve dois resultados: a estatistica W e o valor-p.
        estatistica, valor_p = shapiro(valores_limpos) # [8 espacos] Salva os dois resultados da funcao em variaveis separadas.
        
        # O 'print' escreve coisas na tela preta do computador.
        # [8 espacos] Imprime na tela o nome da variavel.
        print(f"Variavel: {nome_exibicao}") # [8 espacos] Formata o texto para exibir os nomes das colunas.
        
        # O ':.4f' corta o número para exibir no máximo 4 casas decimais ('f' de float).
        # [8 espacos] Exibe o valor da Estatistica W, formatado para mostrar apenas 4 casas decimais.
        print(f"Estatistica W: {estatistica:.4f}") # [8 espacos] Exibe a variavel 'estatistica' cortando decimais extras.
        
        # O ':.4e' exibe o número em notação científica (com aquele 'e' no final), ótimo para números absurdamente pequenos.
        # [8 espacos] Exibe o valor-p em notacao cientifica (elevado) para evitar zerar numeros muito pequenos.
        print(f"Valor-p: {valor_p:.4e}") # [8 espacos] A formatacao '.4e' transforma o numero em potencia de base 10.
        
        # Se (if) o valor for maior (>) que 0.05....
        # [8 espacos] Estrutura condicional para interpretar o valor-p com base no nivel de significancia de 5% (0.05).
        if valor_p > 0.05: # [8 espacos] Inicia uma sub-condicao. Tudo com 12 espacos ocorre se a condicao for verdadeira.
            # [12 espacos] Se for maior que 0.05, nao ha evidencias para rejeitar a normalidade.
            print("Conclusao: A distribuicao parece normal (Nao rejeita a Hipotese Nula).\n") # [12 espacos] Imprime a conclusao na tela.
            
        # Senão (else), caso o valor seja menor ou igual a 0.05....
        else: # [8 espacos] Caminho alternativo caso a afirmacao acima seja falsa (menor ou igual a 0.05).
            # [12 espacos] Se for menor ou igual a 0.05, os dados fogem do padrao de uma curva normal.
            print("Conclusao: A distribuicao NAO e normal (Rejeita a Hipotese Nula).\n") # [12 espacos] Imprime a conclusao alternativa.
            
            # '.append()' é o comando para adicionar um novo item no final daquela nossa lista que criamos em branco lá em cima.
            # [12 espacos] Adiciona o nome desta variavel na nossa lista de variaveis NAO normais.
            variaveis_nao_normais.append(nome_exibicao) # [12 espacos] Guarda o nome formatado na lista.
            
    # Caminho alternativo caso a coluna não tenha 3 números.
    else: # [4 espacos] Caminho alternativo do primeiro 'if' (caso a coluna tenha menos de 3 numeros validos).
        # [8 espacos] Mensagem de alerta caso a coluna tenha menos de 3 valores validos para analise.
        print(f"Variavel: {nome_exibicao} ignorada (dados insuficientes).\n") # [8 espacos] Informa ao usuario que a coluna foi pulada.

# Abre um arquivo chamado 'lista.txt' no modo 'w' (write / escrever). Se ele não existir, o Python cria um novo. 'utf-8' lida com os acentos no Windows.
# [0 espacos] Apos o fim do laco, vamos salvar a nossa lista em um arquivo de texto (.txt).
# [0 espacos] encoding='utf-8' evita erros ao escrever caracteres especiais (como o simbolo de micro) no Windows.
with open('lista.txt', 'w', encoding='utf-8') as arquivo_lista: # [0 espacos] Abre (ou cria) o arquivo 'lista.txt' no modo de escrita.
    
    # Novo laço de repetição. Para cada 'nome_var' guardado dentro da nossa lista...
    # [4 espacos] Cria um novo laco para escrever cada variavel da nossa lista dentro do arquivo.
    for nome_var in variaveis_nao_normais: # [4 espacos] Passa por cada nome salvo na lista.
        
        # Escreve o nome no arquivo. O '\n' aperta o "Enter" invisível para a próxima anotação ficar na linha de baixo.
        arquivo_lista.write(nome_var + '\n') # [8 espacos] Escreve o nome e pula uma linha ('\n') para organizar o arquivo.

# Finaliza mostrando quantos itens a nossa lista tem, usando o comando de contagem 'len'.
# [0 espacos] Informa ao usuario que o arquivo final foi criado e salvo na mesma pasta.
print(f"Processo concluido! Os nomes de {len(variaveis_nao_normais)} variaveis NAO normais foram salvos em 'lista.txt'.\n") # [0 espacos] Imprime o aviso final na tela.

# Pausa o programa esperando a tecla Enter. Isso impede a tela de piscar e fechar rápido demais para os alunos lerem.
# [0 espacos] Mantem a janela do terminal aberta no Windows para os alunos lerem os resultados.
input("Pressione Enter para fechar o programa...") # [0 espacos] O script pausa aqui ate alguem apertar a tecla Enter.