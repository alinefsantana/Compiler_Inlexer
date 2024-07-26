import time
import psutil

def memory_usage():
    process = psutil.Process()
    mem = process.memory_info().rss / 1024 / 1024
    return mem

start_time = time.time()


class Token:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f'Token({self.tipo}, {repr(self.valor)})'

class NumList:
    def __init__(self, name, type, scope = 0, line = 0):
        self.name = name
        self.type = type
        self.scope = scope
        self.line = line
    
    def __str__(self):
        return f'ProcedureList({self.nome})'

class VarList:
    def __init__(self, value, position = 0, scope = 0, procedure = 0, type = None):
        self.value = value
        self.position = position
        self.scope = scope
        self.procedure = procedure
        self.type = type

        def __str__(self):
            return f'VarList({self.value}, {self.position}, {self.scope})'

class Lexer:
    def __init__(self, codigo_pascal):
        self.codigo_fonte = codigo_pascal
        self.tokens = self.tokenizar()

    def tokenizar(self):

        start_time = time.time();
        # Define uma lista de palavras reservadas
        palavras_reservadas = [
            'var', 'begin', 'end', 'if', 'then', 'else',
            'while', 'do', 'not', 'and', 'or'
        ]

        palavras_tipo = [
            'integer', 'real', 'boolean'
        ]

        palavras_procedimento = [
            'procedure', 'program'
        ]

        # Inicializa uma lista vazia para armazenar os tokens
        tokens = []
        lista_variaveis = []
        lista_procedimentos = []
        lista_numeros = []
        num_comp = None

        linha_atual = 1

        escopo = 0
        posicao = 0
        procedimento = 0
        controle_proc = 0
        repeat = 0

        cont_tipo = 0
        muda_escopo = 0
        cont_num = 0
        flag_num = 0

        # Divide o código fonte em linhas e percorre cada linha
        for linha in self.codigo_fonte.split('\n'):
            # Remove espaços em branco no início e no final da linha
            linha = linha.strip()

            # Se a linha estiver vazia, passa para a próxima linha
            if not linha:
                linha_atual += 1
                continue

            # Inicializa um índice para percorrer a linha
            indice = 0

            # Enquanto houver caracteres na linha
            while indice < len(linha):
                # Ignora espaços em branco
                if linha[indice].isspace():
                    indice += 1
                    continue

                # Verifica se é uma palavra reservada, identificador ou número
                if linha[indice].isidentifier() or linha[indice] == '_':
                    # Encontra o final da palavra
                    fim_palavra = indice
                    while (fim_palavra < len(linha) and
                           (linha[fim_palavra].isalnum() or linha[fim_palavra] == '_')):
                        fim_palavra += 1

                    # Extrai a palavra
                    palavra = linha[indice:fim_palavra]

                    # Verifica se é uma palavra reservada
                    if palavra in palavras_reservadas:

                        tokens.append(Token('Palavra reservada', palavra))

                        if palavra == 'end':
                            escopo = 0
                            posicao = 0

                        if palavra == 'begin':
                            posicao = 1

                    elif palavra in palavras_tipo:

                        tokens.append(Token('Palavra reservada', palavra))
                            
                        cont_aux = 1

                        while (cont_aux<=cont_tipo):

                            if palavra == 'integer':
                                lista_variaveis[len(lista_variaveis)-cont_aux].type = 'integer'
                            elif palavra == 'real':
                                lista_variaveis[len(lista_variaveis)-cont_aux].type = 'real'
                            elif palavra == 'boolean':
                                lista_variaveis[len(lista_variaveis)-cont_aux].type = 'boolean'
                                
                            #print(lista_variaveis[len(lista_variaveis)-cont_aux].type)
                        
                            cont_aux+=1
                        
                        cont_tipo = 0

                    elif palavra in palavras_procedimento:

                        tokens.append(Token('Palavra reservada', palavra))

                        if palavra == 'procedure':
                            escopo = 1
                            procedimento = procedimento + 1

                        controle_proc = 1
                    else:

                        tokens.append(Token('Identificador', palavra))

                        if controle_proc == 1:

                            a = len(lista_procedimentos) - 1
                            e = len(lista_variaveis) - 1
                            catchError = 0

                            while (a>=0):
                                if palavra == lista_procedimentos[a].value:
                                    catchError = 1
                                a = a - 1

                            while (e>=0):
                                if palavra == lista_variaveis[e].value:
                                    catchError = 1
                                e = e - 1    
                            
                            if catchError == 1:
                                end_time = time.time()
                                total_time = end_time - start_time
                                print("Total time for Inlexer: ")
                                print(total_time)
                                raise SyntaxError("REPETICAO DE PROCEDIMENTO")

                            lista_procedimentos.append(VarList(palavra, 0, 1, procedimento))
                            controle_proc = 0

                        elif posicao == 0:

                            flag_num = 0

                            a = len(lista_procedimentos) - 1
                            catchError = 0

                            while (a>=0):
                                if palavra == lista_procedimentos[a].value:
                                    catchError = 1
                                a = a - 1
                            
                            if catchError == 1:
                                raise SyntaxError("REPETICAO DE PROCEDIMENTO (2)")
                            
                            e = len(lista_variaveis) - 1
                            catchError = 0

                            while(e>=0):

                                if palavra == lista_variaveis[e].value:
                                    catchError = 1
                                    
                                e = e-1

                            if catchError == 1:
                                raise SyntaxError("VARIAVEL DUPLA EM POS 0")
                            
                            lista_variaveis.append(VarList(palavra, posicao, escopo, procedimento))

                            cont_tipo = cont_tipo + 1

                        elif posicao == 1:

                            flag_num = 1

                            repeat = 0

                            a = len(lista_procedimentos) - 1
                            catchError = 0
                            while (a>=0):

                                if palavra == lista_procedimentos[a].value:
                                    catchError = 1
                                a = a - 1
                            
                            if catchError == 1:
                                repeat = 1
                            
                            e = len(lista_variaveis) - 1

                            while(e>=0):

                                if palavra == lista_variaveis[e].value:
                                    repeat = 1
                                    if muda_escopo == 1:
                                        #print("PALAVRA DE ESCOPO 1:", palavra)
                                        #print("TIPO A SER ATRIBUIDO:", lista_variaveis[e].type)
                                        lista_numeros.append(NumList(palavra, lista_variaveis[e].type, muda_escopo, linha_atual))
                                        #print("ACOLHIDO: ", lista_numeros[len(lista_numeros)-1].type)
                                    elif muda_escopo == 0:
                                        num_comp = lista_variaveis[e].type

                                    if lista_variaveis[e].scope == 1 and lista_variaveis[e].position == 0 and escopo == 0:
                                        raise SyntaxError("INCOMPATIBILIDADE DE ESCOPO")
                                    
                                e = e - 1

                            if repeat == 0:
                                end_time = time.time()
                                tempo = end_time - start_time
                                print(f"Tempo: {tempo* 1000:.3f} ms")
                                print(f'Memória utilizada: {memory_usage()} MB')
                                raise SyntaxError("VARIAVEL EM POSIÇÃO 1 SEM REPETIÇÃO")

                        if posicao == 1 and escopo == 1:

                            a = len(lista_procedimentos) - 1
                            catchError = 0

                            while (a>=0):

                                if palavra == lista_procedimentos[a].value:
                                    catchError = 1
                                a = a - 1
                            
                            if catchError == 1:
                                end_time = time.time()
                                tempo = end_time - start_time
                                print(f"Tempo: {tempo* 1000:.3f} ms")
                                print(f'Memória utilizada: {memory_usage()} MB')
                                raise SyntaxError("PROCEDIMENTO DENTRO DE PROCEDIMENTO")

                    # Atualiza o índice para o próximo caractere após a palavra
                    indice = fim_palavra
                elif linha[indice].isdigit():
                    # Encontra o final do número
                    fim_numero = indice
                    while fim_numero < len(linha) and linha[fim_numero].isdigit():
                        fim_numero += 1
                    if (fim_numero < len(linha) and
                            linha[fim_numero] == '.' and
                            fim_numero + 1 < len(linha) and
                            linha[fim_numero + 1].isdigit()):
                        fim_numero += 1
                        while (fim_numero < len(linha) and
                               linha[fim_numero].isdigit()):
                            fim_numero += 1

                    # Extrai o número
                    numero = linha[indice:fim_numero]
                    if '.' in numero:
                        tokens.append(Token('Numero real', numero))
                        lista_numeros.append(NumList(numero, 'real', muda_escopo, linha_atual))
                    else:
                        tokens.append(Token('Numero inteiro', numero))
                        lista_numeros.append(NumList(numero, 'integer', muda_escopo, linha_atual))

                    # Atualiza o índice para o próximo caractere após o número
                    indice = fim_numero
                elif linha[indice] == ':' and indice + 1 < len(linha) and linha[indice + 1] == '=':
                    tokens.append(Token('Atribuicao', ':='))
                    indice += 2
                    muda_escopo = 1
                elif (linha[indice] == '<' or linha[indice] == '>') and (linha[indice + 1] == '=' or linha[indice + 1] == '>') and indice + 1 < len(linha):
                    tokens.append(Token('Correlacional', linha[indice]))
                    indice += 2
                    muda_escopo = 1
                else:
                    # Verifica se é um operador, delimitador ou comentário
                    if linha[indice] == '{':
                        # Ignora o comentário e vai para o próximo caractere '}'
                        fim_comentario = linha.find('}', indice)
                        if fim_comentario == -1:
                            print(f"Erro: Comentário aberto não fechado na linha {linha_atual}")
                            return []
                        else:
                            indice = fim_comentario + 1
                    else:
                        # Verifica se é um delimitador
                        delimitadores = [';', '(', ')', '.', ':', ',', '{', '}']
                        if linha[indice] in delimitadores:
                            tokens.append(Token('Delimitador', linha[indice]))
                            indice += 1
                        # Verifica se é um operador aditivo
                        elif linha[indice] in ['+', '-', 'or']:
                            tokens.append(Token('Operador aditivo', linha[indice]))
                            indice += 1
                        # Verifica se é um operador multiplicativo
                        elif linha[indice] in ['*', '/', 'and']:
                            tokens.append(Token('Operador multiplicativo', linha[indice]))
                            indice += 1
                        elif linha[indice] in ['=', '<', '>']:
                            tokens.append(Token('Correlacional', linha[indice]))
                            indice += 1
                            muda_escopo = 1
                        # Erro se nenhum caractere reconhecido
                        else:
                            print(f"Erro: Símbolo não reconhecido na linha {linha_atual}")
                            return []
                            
                    ###if (linha[indice-1]=='=' and linha[indice-2]==':'):
                        #tokens.append(Token('Atribuicao', linha[indice-1]))
                        #tokens.append(Token('Atribuicao', linha[indice-2]))

            
            if flag_num == 1:


                N = len(lista_numeros) - 1
                #print("TAM DA LISTA NUM:", len(lista_numeros))
                #print("ULTIMO ITEM: ", lista_numeros[len(lista_numeros)-1].name)
                #print("TIPO DO ULTIMO:", lista_numeros[len(lista_numeros)-1].type)
                #print("num comp:", num_comp)

                while(N >= 0):
                    if lista_numeros[N].line == linha_atual:
                        #print("entrou")
                        #print("LISTA N:", lista_numeros[N].name)
                        #print("TIPO N:", lista_numeros[N].type)
                        lista_numeros
                        if num_comp == 'integer' and (lista_numeros[N].type != 'integer'):
                            end_time = time.time()
                            tempo = end_time - start_time
                            print(f"Tempo total: {tempo* 1000:.3f} ms")
                            print(f'Memória utilizada: {memory_usage()} MB')
                            raise SyntaxError("ERRO INTEGER := REAL OR BOOLEAN")
                        elif num_comp == 'real' and lista_numeros[N].type == 'boolean':
                            end_time = time.time()
                            tempo = end_time - start_time
                            print(f"Tempo total: {tempo* 1000:.3f} ms")
                            print(f'Memória utilizada: {memory_usage()} MB')
                            raise SyntaxError("ERRO REAL := BOOLEAN")
                        elif num_comp == 'boolean' and lista_numeros[N].type != 'boolean':
                            end_time = time.time()
                            tempo = end_time - start_time
                            print(f"Tempo total: {tempo* 1000:.3f} ms")
                            print(f'Memória utilizada: {memory_usage()} MB')
                            raise SyntaxError("ERRO BOOLEAN := NON BOOLEAN")
                    N = N - 1


            linha_atual += 1
            muda_escopo = 0

        print("Lexico terminado")
        return tokens