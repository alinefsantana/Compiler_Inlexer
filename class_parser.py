import time
import psutil

start_time = time.time()

def memory_usage():
    process = psutil.Process()
    mem = process.memory_info().rss / 1024 / 1024
    return mem

class Parser:

    #inicializa definindo variaveis para utilizar dentro do código
    def __init__(self, tokens):

        self.tokens = tokens
        self.token_atual = None
        self.indice_token = 0
        self.avancar()

    #essa função avança o índice da análise de tokens
    def avancar(self):
        if self.indice_token < len(self.tokens):
            self.token_atual = self.tokens[self.indice_token]
            self.indice_token += 1
        else:
            self.token_atual = None

    #essa função define parâmetros para avançar, apenas se for correspondente
    def avancar_se(self, tipo_token):
        if self.token_atual and self.token_atual.tipo == tipo_token:
            self.avancar()
        else:
            end_time = time.time()
            tempo = end_time - start_time
            print(f"Tempo: {tempo* 1000:.3f} ms")
            print(f'Memória utilizada: {memory_usage()} MB')
            raise SyntaxError(f"Esperado {tipo_token}, obtido {self.token_atual.tipo if self.token_atual else 'Nenhum'}")

    #essa inicia com a palavra reservada program e mais padrões do sistema e depois passa para verificar o programa
    def programa(self):
        self.avancar_se('Palavra reservada')
        self.avancar_se('Identificador')
        self.avancar_se('Delimitador')
        try:
            self.declaracoes_variaveis()
        except SyntaxError as e:
            raise SyntaxError(f"Nas declarações de variáveis: {e}")
        try:
            self.declaracoes_subprogramas()
        except SyntaxError as e:
            raise SyntaxError(f"Nas declarações de subprogramas: {e}")
        try:
            self.comando_composto()
        except SyntaxError as e:
            raise SyntaxError(f"No comando composto: {e}")
        self.avancar_se('Delimitador')

    #analisa as declarações de variaveis gerais
    def declaracoes_variaveis(self):
        if self.token_atual.tipo == 'Palavra reservada' and self.token_atual.valor == 'var':
            self.avancar_se('Palavra reservada')
            self.lista_declaracoes_variaveis()
        elif self.token_atual.tipo =='Palavra reservada':
          raise SyntaxError("Esperado 'var' nas declarações de variáveis")
        elif self.token_atual.valor == 'var':
          raise SyntaxError("Esperado 'var' nas declarações de variáveis")
        else:
            raise SyntaxError("Esperado 'var' nas declarações de variáveis")

    #analisa as declarações de variaveis individuais
    def lista_declaracoes_variaveis(self):
        self.lista_identificadores()
        self.avancar_se('Delimitador')
        self.especificacao_tipo()
        self.avancar_se('Delimitador')
        if self.token_atual.valor != 'begin':
            while self.token_atual.tipo == 'Identificador':
                self.lista_identificadores()
                self.avancar_se('Delimitador')
                self.especificacao_tipo()
                self.avancar_se('Delimitador')

    def lista_identificadores(self):
        self.avancar_se('Identificador')
        while self.token_atual.valor == ',':
            self.avancar_se('Delimitador')
            self.avancar_se('Identificador')

    #analisa as especificações de variaveis por tipo
    def especificacao_tipo(self):
        if self.token_atual.tipo == 'Palavra reservada':
            if self.token_atual.valor in ['integer', 'real', 'boolean']:
                self.avancar_se('Palavra reservada')
            else:
                raise SyntaxError(f"Tipo inválido: {self.token_atual.valor}")
        else:
            raise SyntaxError("Esperado especificação de tipo")

    #verifica se há declarações de procedimentos
    def declaracoes_subprogramas(self):
        while self.token_atual.tipo == 'Palavra reservada' and self.token_atual.valor == 'procedure':
            try:
                self.declaracao_subprograma()
            except SyntaxError as e:
                raise SyntaxError(f"Nas declarações de subprograma: {e}")

    #analisa declarações de procedimentos individuais
    def declaracao_subprograma(self):
        self.avancar_se('Palavra reservada')
        self.avancar_se('Identificador')
        if self.token_atual.valor == ';':
            self.avancar_se('Delimitador')
        else:
            try:
                self.argumentos()
            except SyntaxError as e:
                raise SyntaxError(f"Nos argumentos do procedimento: {e}")
        try:
            self.comando_composto()
        except SyntaxError as e:
            raise SyntaxError(f"No comando composto dentro do procedimento: {e}")

    #analisa os argumentos de um procedimento
    def argumentos(self):
      if self.token_atual.valor == '(':
          self.avancar_se('Delimitador')
          self.lista_parametros()
          if self.token_atual.tipo == 'Delimitador':
            self.avancar_se('Delimitador')
      else:
          raise SyntaxError("Esperado '(' nos argumentos do procedimento")

    #analisa lista de parametros de um procedimento
    def lista_parametros(self):
        self.lista_identificadores()
        self.avancar_se('Delimitador')
        self.especificacao_tipo()
        while self.token_atual.valor == ',':
            self.avancar_se('Delimitador')
            self.lista_identificadores()
            self.avancar_se('Delimitador')
            self.especificacao_tipo()
        if self.token_atual.valor == ')':
            self.avancar_se('Delimitador')
        if self.token_atual.valor == ';':
            self.avancar_se('Delimitador')
            self.declaracoes_variaveis()

    #analisa comandos compostos que começam com begin e terminam com end
    def comando_composto(self):
        if self.token_atual.valor=='begin':
            self.avancar_se('Palavra reservada')  # Avança após 'begin'
        try:
            self.comandos_opcionais()
        except SyntaxError as e:
            raise SyntaxError(f"Nos comandos opcionais: {e}")
        self.avancar_se('Palavra reservada')  # Avança após 'end'
        while self.token_atual.valor == ';':
            self.avancar_se('Delimitador')
            if self.token_atual.valor != 'begin':
                self.declaracoes_subprogramas()

    def comandos_opcionais(self):
        while self.token_atual and self.token_atual.valor != 'end':
            try:
                self.comando()
            except SyntaxError as e:
                raise SyntaxError(f"No comando: {e}")
            if self.token_atual.valor == ';':
                self.avancar_se('Delimitador')

    #analisa comandos individuais
    def comando(self):
        if self.token_atual.tipo == 'Identificador':
            try:
                self.atribuicao()
            except SyntaxError as e:
                raise SyntaxError(f"Na atribuição: {e}")
        elif self.token_atual.valor == 'begin':
            try:
                self.comando_composto()
            except SyntaxError as e:
                raise SyntaxError(f"No comando composto: {e}")
        elif self.token_atual.valor == 'if':
            try:
                self.if_statement()
            except SyntaxError as e:
                raise SyntaxError(f"No comando 'if': {e}")
        elif self.token_atual.valor == 'while':
            try:
                self.while_statement()
            except SyntaxError as e:
                raise SyntaxError(f"No comando 'while': {e}")
        elif self.token_atual.valor == 'then':
            try:
                self.avancar_se('Palavra reservada')
                self.comando()
            except SyntaxError as e:
                raise SyntaxError(f"No comando 'then': {e}")
        else:
            end_time = time.time()
            tempo = end_time - start_time
            print(f"Tempo: {tempo* 1000:.3f} ms")
            print(f'Memória utilizada: {memory_usage()} MB')
            raise SyntaxError(f"Comando inválido: {self.token_atual.valor}")

    #método que verifica atribuições
    def atribuicao(self):
        self.avancar_se('Identificador')
        if self.token_atual.valor == '(':
            self.avancar_se('Delimitador')
            self.avancar_se('Identificador')
            self.avancar_se('Delimitador')
        if self.token_atual.tipo == 'Atribuicao':
            self.avancar_se('Atribuicao')
            try:
                self.expressao()
            except SyntaxError as e:
                raise SyntaxError(f"Na expressão: {e}")

    #analisa estruturas condicionais do tipo if
    def if_statement(self):
        self.avancar_se('Palavra reservada')
        try:
            self.expressao()
        except SyntaxError as e:
            raise SyntaxError(f"Na expressão: {e}")
        self.avancar_se('Palavra reservada')
        try:
            self.comando()
        except SyntaxError as e:
            raise SyntaxError(f"No comando (ramo then): {e}")
        if self.token_atual.valor == 'else':
            self.avancar_se('Palavra reservada')
            try:
                self.comando()
            except SyntaxError as e:
                raise SyntaxError(f"No comando (ramo else): {e}")

    #analisa estruturas condicionais do tipo while
    def while_statement(self):
        self.avancar_se('Palavra reservada')
        try:
            self.expressao()
        except SyntaxError as e:
            raise SyntaxError(f"Na expressão: {e}")
        self.avancar_se('Palavra reservada')
        try:
            self.comando()
        except SyntaxError as e:
            raise SyntaxError(f"No comando: {e}")

    #inicio de análise de expressões
    def expressao(self):
        try:
            self.expressao_simples()
        except SyntaxError as e:
            raise SyntaxError(f"Na expressão simples: {e}")
        if self.token_atual.tipo == 'Correlacional':
            self.avancar_se('Correlacional')
            try:
                self.expressao_simples()
            except SyntaxError as e:
                raise SyntaxError(f"Na expressão simples: {e}")

    #analisa expressões simples,única palavra, ou com o uso de aditivos, etc
    def expressao_simples(self):
        if self.token_atual.valor in {'+', '-', 'and'}:
            self.avancar_se('Operador aditivo')
        try:
            self.termo()
        except SyntaxError as e:
            raise SyntaxError(f"No termo: {e}")
        while self.token_atual.valor in {'+', '-', 'or'}:
            self.avancar_se('Operador aditivo')
            try:
                self.termo()
            except SyntaxError as e:
                raise SyntaxError(f"No termo: {e}")

    #analisa combinação de fatores com operadores multiplicativos
    def termo(self):
        try:
            self.fator()
        except SyntaxError as e:
            raise SyntaxError(f"No fator: {e}")
        while self.token_atual.valor in {'*', '/'}:
            self.avancar_se('Operador multiplicativo')
            try:
                self.fator()
            except SyntaxError as e:
                raise SyntaxError(f"No fator: {e}")

    #analisa fatores gerais
    def fator(self):
        if self.token_atual.tipo == 'Identificador':
            self.avancar_se('Identificador')
        elif self.token_atual.tipo in {'Numero inteiro', 'Numero real'}:
            self.avancar_se(self.token_atual.tipo)
        elif self.token_atual.valor == 'not':
            self.avancar_se('Palavra reservada')
        elif self.token_atual.valor == '(':
            self.avancar_se('Delimitador')
            try:
                self.expressao()
            except SyntaxError as e:
                raise SyntaxError(f"Na expressão dentro dos parênteses: {e}")
            self.avancar_se('Delimitador')
        else:
            raise SyntaxError(f"Fator inválido: {self.token_atual.valor}")