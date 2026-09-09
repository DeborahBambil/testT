# O comando 'import' traz ferramentas prontas (bibliotecas) para dentro do nosso código. 'pandas' é excelente para mexer com tabelas. 'as pd' é apenas um apelido curto.
import pandas as pd # [0 espacos] Importa a biblioteca pandas, essencial para ler e manipular tabelas de dados.

# 'from ... import ...' pega uma ferramenta muito específica (ttest_rel) de uma grande caixa de matemática (scipy.stats). Ela serve para comparar duas coisas conectadas (pareadas).
from scipy.stats import ttest_rel # [0 espacos] Importa a funcao ttest_rel, para comparar medias de amostras pareadas/dependentes.

# O 'input' faz uma pergunta na tela e pausa o programa esperando o aluno digitar algo. O que for digitado vira o 'nome_arquivo'.
# [0 espacos] Solicita ao usuario que digite o nome do arquivo de texto (com a extensao .txt).
nome_arquivo = input("Digite o nome do arquivo de entrada (ex: input.txt): ") # [0 espacos] Guarda o nome digitado para usar na leitura.

# 'with open' é a forma segura de abrir arquivos. O 'r' (read) diz que vamos apenas espiar o texto, sem alterar nada.
# [0 espacos] Inspeciona a primeira linha do arquivo para descobrir a estrutura do cabecalho.
with open(nome_arquivo, 'r', encoding='latin-1') as arquivo: # [0 espacos] Abre apenas para checar o topo.
    
    # 'readline()' lê estritamente a primeira linha do texto e para por aí.
    primeira_linha = arquivo.readline() # [4 espacos] Le apenas a primeira linha do arquivo de texto.
    
# O 'if' (Se) verifica uma condição. O 'in' significa dentro. "Se o texto da primeira linha contiver os símbolos "('"...
# [0 espacos] Se a primeira linha contiver uma tupla em texto, significa que o arquivo tem apenas 1 linha de cabecalho.
if "('" in primeira_linha: # [0 espacos] Inicia a condicao para inspecionar os caracteres da linha lida.
    
    # A contagem no Python começa do zero. Isso avisa que a primeira linha é o cabeçalho.
    n_linhas_cabecalho = 0 # [4 espacos] Avisa ao Pandas para ler apenas a primeira linha como cabecalho.

# 'else' (Senão) indica o que fazer se a afirmação acima for mentira.
else: # [0 espacos] Caminho alternativo caso nao possua os caracteres.
    
    # Avisa que os títulos ocupam as linhas 0 e 1 juntas.
    n_linhas_cabecalho = [0, 1] # [4 espacos] Avisa ao Pandas que as duas primeiras linhas formam o cabecalho.
    
# 'pd.read_csv' usa a mágica do pandas para transformar o arquivo de texto em uma tabela virtual interativa. 'sep' diz que o espaço Tab divide as colunas.
# [0 espacos] Le o arquivo de texto informado separando as colunas pelo espaco de tabulacao ('\t').
# [0 espacos] decimal=',' garante que os numeros com virgula sejam compreendidos corretamente como decimais.
# [0 espacos] encoding='latin-1' resolve o erro de leitura de caracteres especiais (como o simbolo de micro).
dados = pd.read_csv(nome_arquivo, sep='\t', header=n_linhas_cabecalho, decimal=',', encoding='latin-1') # [0 espacos] Executa a leitura inteligente.

# Isso varre as colunas e descarta aquelas chamadas 'Unnamed', que são espaços vazios ou erros de leitura invisíveis.
# [0 espacos] Filtra as colunas para remover indices automaticos (espacos vazios que o Pandas chama de 'Unnamed').
colunas_validas = [col for col in dados.columns if 'Unnamed' not in str(col)] # [0 espacos] Mantem apenas os pares reais.

# 'with open' agora usa a letra 'w' (write), que significa modo de escrita. Se esse arquivo não existir, o Python cria ele em branco para você.
# [0 espacos] Abre um arquivo de texto no modo de escrita ('w') para salvar o relatorio final.
with open('Resultado_Test_Pareado.txt', 'w', encoding='latin-1') as arquivo_saida: # [0 espacos] Tudo que gravarmos aqui sera salvo no arquivo.

    # O laço 'for' cria uma repetição. A ferramenta 'range' pulará de 2 em 2, garantindo que peguemos as colunas sempre formando casais/pares.
    # [4 espacos] Cria um laco de repeticao (for) para passar apenas pelas colunas VALIDAS de duas em duas (pares).
    for i in range(0, len(colunas_validas), 2): # [4 espacos] Inicia o laco com o passo '2' para pegar sempre um par.
        
        # Garante que não vamos tentar parear a última coluna com nada, caso a tabela seja ímpar.
        # [8 espacos] Garante que nao vamos tentar ler uma coluna que nao existe caso o numero total seja impar.
        if i + 1 < len(colunas_validas): # [8 espacos] Verifica se existe uma segunda coluna para formar o par.
            
            # Pega as colunas pelas suas posições, como se fosse um endereço.
            # [12 espacos] Identifica as coordenadas das duas colunas que serao comparadas.
            coluna1 = colunas_validas[i] # [12 espacos] Pega a referencia da primeira coluna do par.
            coluna2 = colunas_validas[i+1] # [12 espacos] Pega a referencia da segunda coluna do par.
            
            # 'isinstance' faz a pergunta: "O título da coluna1 é um par verdadeiro (uma tupla)?".
            # [12 espacos] Extrai os titulos (Amostra e Variavel) individualmente para CADA coluna.
            if isinstance(coluna1, tuple): # [12 espacos] Se o cabecalho for uma tupla original (2 linhas puras).
                amostra1 = coluna1[0] # [16 espacos] Isola a amostra da primeira coluna.
                variavel1 = coluna1[1] # [16 espacos] Isola a variavel da primeira coluna.
                amostra2 = coluna2[0] # [16 espacos] Isola a amostra da segunda coluna.
                variavel2 = coluna2[1] # [16 espacos] Isola a variavel da segunda coluna.
                
            # Senão, usamos a ferramenta 'eval' que obriga o Python a ler um texto normal como se fosse código, revelando as duas partes do título.
            else: # [12 espacos] Se o cabecalho for uma unica linha de texto (gerada pelo output_dados_mistos).
                titulos1 = eval(coluna1) # [16 espacos] Converte o texto da primeira coluna de volta em tupla.
                titulos2 = eval(coluna2) # [16 espacos] Converte o texto da segunda coluna de volta em tupla.
                amostra1 = titulos1[0] # [16 espacos] Isola a amostra da primeira coluna.
                variavel1 = titulos1[1] # [16 espacos] Isola a variavel da primeira coluna.
                amostra2 = titulos2[0] # [16 espacos] Isola a amostra da segunda coluna.
                variavel2 = titulos2[1] # [16 espacos] Isola a variavel da segunda coluna.
            
            # ATENÇÃO AQUI: Como o teste é pareado (linha a linha), se um valor de um lado estiver vazio, o 'dropna()' apaga a linha inteira para não desalinhar o par!
            # [12 espacos] O Teste T Pareado exige o mesmo numero de amostras. Isolamos o par e removemos vazios juntos.
            pares_limpos = dados[[coluna1, coluna2]].dropna() # [12 espacos] Limpa garantindo que os pares fiquem alinhados.
            valores1 = pares_limpos[coluna1] # [12 espacos] Separa os dados limpos do primeiro grupo.
            valores2 = pares_limpos[coluna2] # [12 espacos] Separa os dados limpos do segundo grupo.
            
            # Verifica se pelo menos 3 linhas (pares) sobreviveram à limpeza para a matemática funcionar.
            # [12 espacos] O teste exige dados suficientes. Vamos garantir que tenhamos pelo menos 3 pares de valores validos.
            if len(valores1) >= 3: # [12 espacos] Inicia a estrutura condicional para os pares validos.
                
                # Chama a ferramenta 'ttest_rel'. Ela calcula as diferenças linha por linha e devolve dois resultados numéricos.
                # [16 espacos] Aplica o Teste T Pareado nos dois grupos limpos e dependentes.
                estatistica, valor_p = ttest_rel(valores1, valores2) # [16 espacos] Salva os resultados em variaveis separadas.
                
                # Monta a frase que avisa quais amostras estão brigando, usando a formatação 'f' para incluir variáveis no texto.
                # [16 espacos] Monta o texto informando exatamente quem esta sendo comparado com quem.
                texto_comparacao = f"Comparando: {amostra1} ({variavel1}) VS {amostra2} ({variavel2})" # [16 espacos] Cria a frase.
                
                # 'print' escreve na tela e '.write' grava no arquivo de texto.
                print(texto_comparacao) # [16 espacos] Exibe a frase na tela.
                arquivo_saida.write(texto_comparacao + "\n") # [16 espacos] Salva a frase no arquivo txt.
                
                # ':.4f' corta os números exagerados para deixar apenas 4 casas decimais.
                # [16 espacos] Exibe e salva o valor da Estatistica t, formatado para mostrar apenas 4 casas decimais.
                print(f"Estatistica t: {estatistica:.4f}") # [16 espacos] Exibe a variavel cortando decimais extras.
                arquivo_saida.write(f"Estatistica t: {estatistica:.4f}\n") # [16 espacos] Salva no arquivo txt.
                
                # ':.4e' exibe os números em formato científico (ex: 1.0e-05), necessário para números muito pequenos.
                # [16 espacos] Exibe e salva o valor-p em notacao cientifica (elevado) para evitar zerar.
                print(f"Valor-p: {valor_p:.4e}") # [16 espacos] Formata em potencia de base 10.
                arquivo_saida.write(f"Valor-p: {valor_p:.4e}\n") # [16 espacos] Salva no arquivo txt.
                
                # A condição analisa o valor-p para ver se passou de 0.05 ou não, escolhendo qual conclusão imprimir.
                # [16 espacos] Estrutura condicional para interpretar o valor-p com significancia de 5% (0.05).
                if valor_p > 0.05: # [16 espacos] Inicia sub-condicao. Tudo com 20 espacos ocorre se for verdadeira.
                    # [20 espacos] Se for maior que 0.05, as medias pareadas sao estatisticamente iguais.
                    print("Conclusao: As medias pareadas sao iguais (Nao rejeita a Hipotese Nula).\n") # [20 espacos] Imprime a conclusao.
                    arquivo_saida.write("Conclusao: As medias pareadas sao iguais (Nao rejeita a Hipotese Nula).\n\n") # [20 espacos] Salva no arquivo txt.
                else: # [16 espacos] Caminho alternativo caso a afirmacao acima seja falsa.
                    # [20 espacos] Se for menor ou igual a 0.05, as medias pareadas sao estatisticamente diferentes.
                    print("Conclusao: As medias pareadas sao diferentes (Rejeita a Hipotese Nula).\n") # [20 espacos] Imprime a conclusao alternativa.
                    arquivo_saida.write("Conclusao: As medias pareadas sao diferentes (Rejeita a Hipotese Nula).\n\n") # [20 espacos] Salva no arquivo txt.
                    
            # Caminho caso as colunas fiquem muito vazias depois da limpeza pareada.
            else: # [12 espacos] Caminho alternativo (caso o par tenha menos de 3 linhas validas apos limpeza).
                alerta = f"Comparando: {amostra1} ({variavel1}) VS {amostra2} ({variavel2}) ignorada (dados insuficientes).\n" # [16 espacos] Monta o alerta.
                print(alerta) # [16 espacos] Imprime alerta na tela.
                arquivo_saida.write(alerta + "\n") # [16 espacos] Salva alerta no arquivo.

# Informa ao usuário que tudo acabou bem.
# [0 espacos] Informa que o arquivo de saida foi gerado com sucesso.
print("Processo concluido! O relatorio completo foi salvo em 'Resultado_Test_Pareado.txt'.\n")

# O 'input' segura a janela do terminal aberta. Se não colocar isso, a tela preta pisca e fecha e ninguém consegue ler os resultados!
# [0 espacos] Mantem a janela do terminal aberta no Windows para os alunos lerem os resultados.
input("Pressione Enter para fechar o programa...") # [0 espacos] O script pausa aqui ate alguem apertar a tecla Enter.