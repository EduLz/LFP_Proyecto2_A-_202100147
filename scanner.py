def is_alpha(c):
    return c.isalpha()

def is_alnum_or_underscore(c):
    return c.isalnum() or c == '_'

def is_delimiter(c):
    return c in r'{}()=,.;"\'\':}-$“”-* /'

def is_quote(c):
    return c in "\"'"


TRANSITION_TABLE = {
    'S0': {
        'is_alpha': 'S1',
        'is_delimiter': 'S2',
        'is_quote': 'S3',
    },
    'S1': {
        'is_alnum_or_underscore': 'S1',
        'not_is_alnum_or_underscore': 'S0'
    },
    'S2': {
        'not_is_delimiter': 'S0'
    },
    'S3': {
        'is_quote': 'S3_end',
    },
    'S3_end': {
        'not_is_quote': 'S0'
    },
}

def is_comment_start(input_str, i):
    return input_str[i:i+3] == '---'

class Scanner:
    def __init__(self, input_str):
        self.input_str = input_str
        self.tokens = []
        self.keywords = {
            "CrearBD": "CREAR_DB",
            "nueva": "NEW",
            "EliminarBD": "ELIMINAR_DB",
            "CrearColeccion": "CREAR_COLECCION",
            "EliminarColeccion": "ELIMINAR_COLECCION",
            "InsertarUnico": "INSERTAR_UNICO",
            "ActualizarUnico": "ACTUALIZAR_UNICO",
            "EliminarUnico": "ELIMINAR_UNICO",
            "BuscarTodo": "BUSCAR_TODO",
            "BuscarUnico": "BUSCAR_UNICO"
        }

        self.delimiters = {
            '{': 'ICORCH',
            '}': 'DCORCH',
            '(': 'IPAREN',
            ')': 'DPAREN',
            '=': 'IGUAL',
            ',': 'COMA',
            '.': 'PUNTO',
            ';': 'PUNTOCOMA',
            '"': 'NMCOMILLAS',
            "'": 'PCOMILLAS',
            ':': 'DOSPUNTOS',
            '$': 'DOLAR',
            '“': 'OPCOMILLAS',
            '”': 'CLCOMILLAS',
            '-': 'GUION',
            '*': 'ASTERISCO',
            '/': 'DIAGONAL'
            
        }

    def is_identifier(self, s):
        if s[0].isalpha() or s[0] == '_':
            return all(c.isalnum() or c == '_' for c in s[1:])
        return False

    def initToken(self):
        self.tokens = []
        state = 'S0'
        line_num = 1
        line_start = 0
        i = 0
        n = len(self.input_str)

        while i < n:
            c = self.input_str[i]

            if is_comment_start(self.input_str, i):
                while i < n and self.input_str[i] != '\n':
                    i += 1
                continue

            if state == 'S0':
                if is_alpha(c):
                    start = i
                    state = TRANSITION_TABLE[state]['is_alpha']
                elif c.isspace():
                    if c == '\n':
                        line_num += 1
                        line_start = i + 1
                    i += 1
                    continue
                elif is_delimiter(c):
                    state = TRANSITION_TABLE[state]['is_delimiter']
                    self.tokens.append((self.delimiters[c], c, line_num, i, i+1))
                elif is_quote(c):
                    start = i
                    state = TRANSITION_TABLE[state]['is_quote']
                else:
                    raise RuntimeError(f'{c!r} inesperado en la línea {line_num}')

            elif state == 'S1':
                if is_alnum_or_underscore(c):
                    state = TRANSITION_TABLE[state]['is_alnum_or_underscore']
                else:
                    token = self.input_str[start:i]
                    if token in self.keywords:
                        self.tokens.append((self.keywords[token], token, line_num, start, i))
                        if token == "nueva":
                            while self.input_str[i].isspace():
                                i += 1
                            if self.input_str[i:i+1] == "=":
                                i += 1
                                self.tokens.append(('IGUAL', '=', line_num, i-1, i))
                            else:
                                i -= 1  # Revert the index back to handle the next token properly
                    elif self.is_identifier(token):
                        self.tokens.append(('ID', token, line_num, start, i))
                    else:
                        raise RuntimeError(f'{token!r} no es una palabra clave ni un identificador válido en la línea {line_num}')
                    state = 'S0'
                    continue

            elif state == 'S2':
                state = 'S0'
                continue

            elif state == 'S3':
                if is_quote(c):
                    state = TRANSITION_TABLE[state]['is_quote']
                i += 1

            if state == 'S3_end':
                token = self.input_str[start + 1:i - 1]
                self.tokens.append(('STRING', token, line_num, start, i))
                state = 'S0'
                i += 1
            else:
                i += 1

        return self.tokens 
