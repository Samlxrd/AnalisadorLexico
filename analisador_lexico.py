lines = 1
col = 1
last_col = 1
err = []    # Os erros serão armazenados nessa lista

alpha_low = "abcdefghijklmnopqrstuvwxyz"
alpha_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RESERVED_WORDS = ["programa", "fim_programa", "se", "senao", "entao", "imprima", "leia", "enquanto"]


def read_char():
    """
    Lê um caractere do arquivo e retorna.
    """

    global col
    global lines
    global last_col
    
    char = file.read(1)
    col += 1

    if char == '\n':
        lines += 1
        last_col = col
        col = 1

    return char

def retreat():
    """
    Retrocede uma posição no arquivo, decrementando em 1 a coluna atual.
    """

    current = file.tell()
    global col
    if col > 1:
        col -= 1
    file.seek(current-1)

def erro_lexico(current_state):
    """
    Recebe um estado e verifica qual erro corresponde a ele, e,
    adiciona na lista de erros:\n
    Posição no arquivo, linha, coluna e descrição do erro encontrado.

    """

    global col
    global err

    if col > 0:
        col -= 1


    match current_state:

        case 0:
            error_name = 'Caractere invalido.'

        case 4:
            error_name = 'Cadeia nao fechada.'

        case 1:
            error_name = 'Palavra reservada nao encontrada.'

        case 3:
            error_name = 'Palavra reservada nao encontrada.'

        case 7:
            error_name = "Moeda mal formatada, esperado '$'."
        
        case 8:
            error_name = 'Moeda mal formatada.'
        
        case 9:
            error_name = 'Moeda mal formatada.'
        
        case 10:
            error_name = 'Moeda mal formatada.'

        case 11:
            error_name = 'Moeda mal formatada.'

        case 12:
            error_name = 'Numero mal formatado.'

        case 15:
            error_name = 'Numero mal formatado.'

        case 19:
            error_name = 'Comentario nao terminado.'

        case 22:
            error_name = 'Nome de variavel mal formatado.'

        case 23:
            error_name = 'Nome de variavel mal formatado.'

        case 25:
            error_name = 'Atribuicao invalida, tente :='

    if col < 1:
        err.append([file.tell(), lines-1, last_col-1, error_name])
    else:
        err.append([file.tell(), lines, col, error_name])

    return -1

    """ # Essa parte era a implementação do método do desespero
    while True:
      char = read_char()

      if  char == '\n' or char == '' or char in ',()':
        return -1
    """
    
def get_token(current_state, palavra):
    """
    Recebe um estado e um lexema, retorna o token correspondente ao
    estado recebido, com o nome e lexema do token.
    """

    match current_state:

        case 0:
            tk = ""
            if palavra == '(':
                tk = "tk_ab_paren"
            elif palavra == ')':
                tk = "tk_fe_paren"
            elif palavra == '-':
                tk = "tk_subt"
            elif palavra == '+':
                tk = "tk_soma"
            elif palavra == ',':
                tk = "tk_virg"
            elif palavra == '*':
                tk = "tk_mult"
            elif palavra == '~':
                tk = "tk_neg"
            elif palavra == '&':
                tk = "tk_and"
            elif palavra == '|':
                tk = "tk_or"
            
            return [tk, palavra]

        case 3:
            if palavra in RESERVED_WORDS:
                return ["tk_"+palavra, palavra]
            erro_lexico(current_state)
            return ["ERR", "ERR"]
            
        case 4:
            return ["tk_cadeia", palavra]
        
        case 6: return ["tk_numero", palavra]
        
        case 11:
            return ["tk_moeda", palavra]
        
        case 13:
            return ["tk_numero", palavra]

        case 14:
            return ["tk_numero", palavra]

        case 16:
            return ["tk_numero", palavra]
        
        case 22:
            return ["tk_le", palavra]
        
        case 23:
            return ["tk_id", palavra]
        
        case 24:
            return ["tk_lt", palavra]
        
        case 25:
            return ["tk_atrb", palavra]
        
        case 26:
            return["tk_ge", palavra]
        case 27:
            return["tk_gt", palavra]

def proximo_token():
    """
    Busca no arquivo o próximo token, retornando o nome do token,
    lexema e sua posição (linha e coluna) no arquivo.
    """
    
    global lines
    global col

    pos = [lines, col]
    palavra = ""
    state = 0

    # Laço para reconhecimento dos estados
    while 1:
        if state == -1: # Significa que foi encontrado erro léxico e o lexema será descartado.
          return "ERR"
          
        match state:
            case 0:
                char = read_char()
                
                if char in " \n":   # Ignora
                    state = 0

                elif char in alpha_low:     # Palavra reservada
                    state = 1
                    palavra += char

                elif char == '"':           # Cadeia
                    state = 4
                    palavra += char

                elif char == "#":           # Comentário de única linha
                    state = 5

                elif char in "ABCDEF":
                    palavra += char
                    state = 6
                    
                elif char in "GHIJKLMNOPQRSTUVWXYZ":
                    palavra += char
                    state = 7

                elif char.isdigit():
                    palavra += char
                    state = 6

                elif char in '-~+*&|,()':
                    palavra += char

                    token, val = get_token(state, palavra)
                    return [token, val, pos]

                elif char == "'":           # Comentário de múltiplas linhas
                    state = 17

                elif char == '<':
                    palavra += char
                    state = 22

                elif char == '>':
                    palavra += char
                    state = 26

                elif char == ':':           # Atribuição
                    palavra += char
                    state = 25

                
                else:
                    state = erro_lexico(state)
                
            # Estado 1 (Palavra Reservada)
            case 1:
                char = read_char()

                if char in alpha_low:
                    state = 2
                    palavra += char

                else: state = erro_lexico(state)

            # Estado 2 (Palavra Reservada)
            case 2:
                char = read_char()
                if char == '':
                    state = 3

                elif char in alpha_low+'_':
                    state = 2
                    palavra += char
                
                else: state = 3

            # Estado 3 (Palavra Reservada)
            case 3:
                if char:
                    if char not in ' \n':
                            retreat()

                token, val = get_token(state, palavra)

                if token == 'ERR':
                    state = -1

                else:
                  return [token, val, pos]
            
            # Estado 1 (Cadeia)
            case 4:
                char = read_char()
                
                if char == '"':
                    palavra += char
                    token, val = get_token(state, palavra)
                    return [token, val, pos]
                
                elif char == '\n':
                    state = erro_lexico(state)
                
                else: palavra += char

            # Estado 1 (Comentário)
            case 5:
                char = read_char()
                
                if char == '\n':
                    return "COMMENT"

            # Estado 1 (A-F)
            case 6:
                char = read_char()

                # Estado moeda
                if char == '$':
                    palavra += char
                    state = 8
                
                # Estado Float
                elif char == '.':
                    palavra += char
                    state = 12

                # Mais digitos
                elif char in 'ABCDEF' or char.isdigit():
                    palavra += char
                    state = 13

                # Estado Notação científica
                elif char == 'e':
                    palavra += char
                    state = 15

                else:
                    if char:
                        if char not in ' \n':
                            retreat()

                    token, val = get_token(state, palavra)
                    return [token, val, pos]
                    
            
            # Estado 1 (G-Z)
            case 7:
                char = read_char()

                if char == '$':
                    palavra += char
                    state = 8
                else:
                    state = erro_lexico(state)


            # Estado Tratamento Moeda (Ter pelo menos 1 digito)
            case 8:
                char = read_char()

                if char.isdigit():
                    palavra += char
                    state = 9
                else: state = erro_lexico(state)

            # Estado Tratamento Moeda
            case 9:
                char = read_char()

                if char.isdigit():
                    palavra += char
                elif char == '.':
                    palavra += char
                    state = 10
                else:
                    state = erro_lexico(state)

            case 10:
                char = read_char()

                if char.isdigit():
                    palavra += char
                    state = 11
                else:
                    state = erro_lexico(state)

            case 11:
                char = read_char()

                if char.isdigit():
                    palavra += char
                    token, val = get_token(state, palavra)
                    return [token, val, pos]
                else:
                    state = erro_lexico(state)

            # Estado 1 (Float)
            case 12:
                char = read_char()

                if char in "ABCDEF" or char.isdigit():
                    palavra += char
                    state = 14
                else:
                    state = erro_lexico(state)
                
            case 13:
                char = read_char()

                if char in "ABCDEF"or char.isdigit():
                    palavra += char
                
                # Tratamento de Float
                elif char == '.':
                    palavra += char
                    state = 12

                # Tratamento notação científica
                elif char == 'e':
                    palavra += char
                    state = 15

                # Leu outro, retorna token
                else: 
                    if char:
                        if char not in ' \n':
                            retreat()
                    token, val = get_token(state, palavra)
                    return [token, val, pos]
                
            case 14:
                char = read_char()
                
                if char in "ABCDEF" or char.isdigit():
                    palavra += char
                
                # Tratamento notação cientifica
                elif char == 'e':
                    palavra += char
                    state = 15

                else:
                    if char:
                        if char not in ' \n':
                            retreat()

                    token, val = get_token(state, palavra)
                    return [token, val, pos]
            
            # Estado 1 (Notação científica)
            case 15:
                char = read_char()

                if char in "ABCDEF" or char.isdigit() or '-':
                    palavra += char
                    state = 16
                
                else:
                    state = erro_lexico(state)
            
            # Estado 2 (Notação científica)
            case 16:
                char = read_char()

                if char in alpha_uppercase or char.isdigit():
                    palavra += char
                else:
                    if char:
                        if char not in ' \n':
                            retreat()
                    token, val = get_token(state, palavra)
                    return [token, val, pos]
            
            # Estado 1 (Comentário várias linhas)
            case 17:
                char = read_char()
                
                if char == "'":
                    state = 18

            # Estado 2 (Comentário várias linhas)
            case 18:
                char = read_char()

                if char == "'":
                    state = 19

            # Estado 3 (Comentário várias linhas)
            case 19:
                char = read_char()

                if char == "'":
                    state = 20

                elif char == '':
                    state = erro_lexico(state)
                    return "ERR"
            
            # Estado 4 (Comentário várias linhas)
            case 20:
                char = read_char()

                if char == "'":
                    state = 21
                
                else:
                    state = 19

            # Estado 5 (Comentário várias linhas)
            case 21:
                char = read_char()

                if char == "'":
                    return 'COMMENT'
                
                else:
                    state = 19
            
            # Estado após ler '<'
            case 22:
                char = read_char()

                if char == '=':
                    palavra += char

                    token, val = get_token(state, palavra)
                    return [token, val, pos]
                
                elif char in alpha_low:
                    state = 23
                    palavra += char

                elif char == ' ':
                    state = 24

                    token, val = get_token(state, palavra)
                    return [token, val, pos]
                
                else:
                    state = erro_lexico(state)
            
            # Estado identificador
            case 23:
                char = read_char()

                if char in alpha_low or char.isdigit():
                    palavra += char

                elif char == '>':
                    palavra += char

                    token, val = get_token(state, palavra)
                    return [token, val, pos]
                
                else:
                    state = erro_lexico(state)
            
            # Estado atribuição
            case 25:
                char = read_char()

                if char == '=':
                    palavra += char

                    token, val = get_token(state, palavra)
                    return [token, val, pos]
                
                else:
                    state = erro_lexico(state)

            case 26:
                char = read_char()

                if char == '=':
                    palavra += char
                    state = 27
                    token, val = get_token(state, palavra)
                    return [token, val, pos]
                
                else:
                    if char:
                        if char not in ' \n':
                            retreat()
                    token, val = get_token(state, palavra)
                    return [token, val, pos]



        if char == '':
            token, val = get_token(state, palavra)
            return [token, val, pos, "FIM"]


# Abrindo os arquivos de entrada
# Basta inserir o nome dos arquivos na lista

arqs = ['ex1.cic', 'ex2.cic', 'ex3.cic']

# Analisa  e gera os relatórios de tokens, lexemas,
# ocorrências e erros nos arquivos informados.
for a in arqs:
    lines = 1
    last_col = 1
    col = 1
    err = []

    with open(a) as file:
        tk = None
        pairs = []

        while 1:
            tk = proximo_token()

            if tk:
                if tk[-1] == 'FIM':
                    tk.pop()
                    if tk[0] != '':
                        pairs.append(tk)
                    break

                if tk == 'COMMENT':
                    continue

                elif tk == 'ERR':
                    continue
                else:
                    pairs.append(tk)
            else:
                print("Leitura feita com sucesso.")
                break
            

    # Arquivos de saída

    with open('relatorio_'+a, "w") as arq:

        # Lista de Tokens reconhecidos
        column = ['LIN ', 'COL ', 'TOKEN', 'LEXEMA']
        arq.write('+------+------+-----------------+-----------------+\n')
        arq.write(f'| { column[0]:<3} | {column[1]:<4} | {column[2]:<15} | {column[3]:<15} |\n')
        for tk in pairs:
            lin, col = tk[-1]
            if tk[0] == 'tk_id':
                arq.write('+------+------+-----------------+-----------------+\n')
                arq.write(f'| {lin:<4} | {col:<4} | {tk[0]:<15} | {tk[1]:<15} |\n')
            else:
                strg = ''
                arq.write('+------+------+-----------------+-----------------+\n')
                arq.write(f'| {lin:<4} | {col:<4} | {tk[0]:<15} | {strg:<15} |\n')

        arq.write('+------+------+-----------------+-----------------+\n\n\n')


        # Armazenando os Tokens sem repetições
        all_tokens = [x[0] for x in pairs]
        nonrep_tokens = []
        for tk in all_tokens:
            if tk not in nonrep_tokens:
                nonrep_tokens.append(tk)
        
        # Contagem de ocorrência dos Tokens
        tokens_count = []
        for tk in nonrep_tokens:
            tokens_count.append([tk, all_tokens.count(tk)])

        # Ordenar por ocorrencia
        tokens_count.sort(key=lambda x: x[1], reverse=True)
        
        t = 0
        column = ['TOKEN', 'Usos']

        arq.write('+-----------------+----------+\n')
        arq.write(f'| {column[0]:<15} | {column[1]:<8} |\n')

        for tk in tokens_count:
            arq.write('+-----------------+----------+\n')
            arq.write(f'| {tk[0]:<15} | {tk[1]:<8} |\n')
            t += tk[1]

        strg = 'TOTAL'
        arq.write('+-----------------+----------+\n')
        arq.write(f'| {strg:<15} | {t:<8} |\n')
        arq.write('+-----------------+----------+')

    # Se não tiver erros no arquivo testado,
    # não será gerado arquivo para identificação de erros
    if len(err) == 0:
            continue
    
    # Arquivo com identificação de erros

    curr_line = 1
    curr_col = 1
    line_error = False
    target_col = []

    with open('erros_'+a, 'w') as arq_err:
        with open(a) as arq_b:
            text = '[' + str(curr_line) + '] '
            arq_err.write(text)

            while True:
                try:
                    char = arq_b.read(1)
                    
                    # Se encontrar fim de arquivo e não encontrou a posição do erro
                    # Imprime o erro no final do arquivo.
                    if char == '':
                        if len(err) > 0:
                            for e in err:
                                curr_col = 1
                                arq_err.write('\n')

                                while curr_col < e[2] + len(text):
                                    arq_err.write('-')
                                    curr_col += 1

                                arq_err.write('^\n')
                                arq_err.write(e[3]+'\n')
                        break
                except EOFError: break

                # Enquanto tiver erro na lista, procura erro e remove ele da lista.
                # Salva a coluna e indica na flag line_error que a linha contém erro.
                if len(err) > 0:
                    if [curr_line, curr_col] == [err[0][1], err[0][2]]:
                        target_col.append([curr_col, err[0][3]])
                        err.pop(0)
                        line_error = True

                curr_col += 1
                arq_err.write(char)

                if char == '\n':
                    curr_line += 1
                    curr_col = 1

                    if line_error == False:
                        text = '[' + str(curr_line) + '] '
                        arq_err.write(text)

                    # Se tiver erro na linha, percorre a coluna para apontá-lo.
                    else:
                        cc = curr_col
                        for t in target_col:
                            curr_col = cc

                            while curr_col < t[0] + len(text):
                                arq_err.write('-')
                                curr_col += 1

                            arq_err.write('^\n')
                        
                        for t in target_col:
                            error_msg = f'Erro lexico na linha {curr_line-1} coluna {t[0]}:\n'
                            arq_err.write(error_msg)
                            arq_err.write(t[1]+'\n')

                        text = '[' + str(curr_line) + '] '
                        arq_err.write(text)

                        curr_col = 1
                        target_col = []
                        line_error = False