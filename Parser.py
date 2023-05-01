from scanner import Scanner

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.expresiones = []

    def next(self):
        self.token = self.tokens.pop(0)

    def match(self, expected):
        if self.token[0] == expected:
            t = self.token
            self.next()
            return t
        else:
            raise RuntimeError(f'Se esperaba {expected!r}, pero se encontró {self.token!r}')

    def parse(self):
        while self.peek() is not None:
            if self.peek()[0] == "---":  # Agregamos el manejo de comentarios
                self.consume("---")
                self.expresiones.append("---")
            else:
                self.expresiones.append(self.parse_stmt())
        return self.expresiones

    def consume(self, expected_type=None):
        if expected_type is not None:
            if self.peek()[0] == expected_type:
                token = self.tokens[self.pos]
                self.pos += 1
                return token
            else:
                raise RuntimeError(f"Error inesperado: {self.peek()[0]} en la línea {self.peek()[2]}. Se esperaba {expected_type}.")
        else:
            token = self.tokens[self.pos]
            self.pos += 1
            return token

    def accept(self, token_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_type:
            token_value = self.tokens[self.pos][1]
            self.pos += 1
            return token_value
        return None

    def accept_json_content(self):
        json_content = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != "PUNTOCOMA":
            json_content.append(self.tokens[self.pos][1])
            self.pos += 1
        if json_content:
            return "".join(json_content)
        else:
            raise SyntaxError(f"Se esperaba contenido JSON en la línea {self.tokens[self.pos][2]}")

    def expect(self, *expected_types):
        if self.pos >= len(self.tokens):
            raise Exception("Error inesperado: fin de archivo")

        token_type, token_value, line_num, start_pos, end_pos = self.tokens[self.pos]

        if token_type in expected_types:
            self.pos += 1
            return token_value
        else:
            expected_str = " o ".join(expected_types)
            raise Exception(f"Error inesperado: {token_type} en la línea {line_num}. Se esperaba {expected_str}.")

    def saltar_espacioBlanco(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == "GUION":
            self.pos += 1

    def parse(self):
        expresiones = []
        try:
            while self.pos < len(self.tokens):
                if self.accept("CREAR_DB"):
                    self.expect("ID")
                    self.saltar_espacioBlanco()
                    self.expect("IGUAL")
                    self.expect("NEW")
                    self.expect("CREAR_DB")
                    self.expect("IPAREN")
                    self.expect("DPAREN")
                    self.expect("PUNTOCOMA")
                    expresiones.append(("CREAR_DB", self.tokens[self.pos - 7][1]))

                elif self.accept("ELIMINAR_DB"):
                    self.expect("ID")
                    self.saltar_espacioBlanco()
                    self.expect("IGUAL")
                    self.expect("NEW")
                    self.expect("ELIMINAR_DB")
                    self.expect("IPAREN")
                    self.expect("DPAREN")
                    self.expect("PUNTOCOMA")
                    expresiones.append(("ELIMINAR_DB",self.tokens[self.pos - 7][1]))

                elif self.accept("CREAR_COLECCION"):
                    self.expect("ID")
                    self.saltar_espacioBlanco()
                    self.expect("IGUAL")
                    self.expect("NEW")
                    self.expect("CREAR_COLECCION")
                    self.expect("IPAREN")                    
                    collection_name = self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("ID")
                    collection_name = self.tokens[self.pos - 1][1]
                    self.expect("OPCOMILLAS", "CLCOMILLAS","NMCOMILLAS", "PCOMILLAS")
                    self.expect("DPAREN")
                    self.expect("PUNTOCOMA")
                    expresiones.append(("CREAR_COLECCION", collection_name))

                elif self.accept("ELIMINAR_COLECCION"):
                    self.expect("ID")
                    self.saltar_espacioBlanco()
                    self.expect("IGUAL")
                    self.expect("NEW")
                    self.expect("ELIMINAR_COLECCION")
                    self.expect("IPAREN")
                    collection_name = self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("ID")
                    collection_name = self.tokens[self.pos - 1][1]
                    self.expect("OPCOMILLAS", "CLCOMILLAS","NMCOMILLAS", "PCOMILLAS")
                    self.expect("DPAREN")
                    self.expect("PUNTOCOMA")
                    expresiones.append(("ELIMINAR_COLECCION", collection_name))

                elif self.accept("INSERTAR_UNICO"):
                    self.expect("ID")
                    self.saltar_espacioBlanco()
                    self.expect("IGUAL")
                    self.expect("NEW")
                    self.expect("INSERTAR_UNICO")
                    self.expect("IPAREN")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("ID")
                    self.tokens[self.pos - 1][1]
                    self.expect("OPCOMILLAS", "CLCOMILLAS","NMCOMILLAS", "PCOMILLAS")
                    self.expect("COMA")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("ICORCH")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("ID")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("DOSPUNTOS")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("ID")
                    self.expect("ID")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("COMA")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("ID")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("DOSPUNTOS")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("ID")
                    self.expect("ID")
                    self.expect("NMCOMILLAS")
                    self.expect("DCORCH")
                    self.expect("NMCOMILLAS", "PCOMILLAS", "OPCOMILLAS", "CLCOMILLAS")
                    self.expect("DPAREN")
                    self.expect("PUNTOCOMA")
                    self.saltar_espacioBlanco()
                    json_content = self.accept_json_content()
                    expresiones.append(("INSERTAR_UNICO", json_content))

                elif self.accept("ACTUALIZAR_UNICO"):
                    self.saltar_espacioBlanco()
                    self.expect("IGUAL")
                    self.expect("NEW")
                    self.expect("ACTUALIZAR_UNICO")
                    self.expect("IPAREN")
                    json_query = self.accept_json_content()
                    self.expect("COMA")
                    json_update = self.accept_json_content()
                    self.expect("DPAREN")
                    self.expect("PUNTOCOMA")
                    expresiones.append(("ACTUALIZAR_UNICO", json_query, json_update))

                elif self.accept("ELIMINAR_UNICO"):
                    self.saltar_espacioBlanco()
                    self.expect("IGUAL")
                    self.expect("NEW")
                    self.expect("ELIMINAR_UNICO")
                    self.expect("IPAREN")
                    json_query = self.accept_json_content()
                    self.expect("DPAREN")
                    self.expect("PUNTOCOMA")
                    expresiones.append(("ELIMINAR_UNICO", json_query))

                elif self.accept("BUSCAR_TODO"):
                    self.saltar_espacioBlanco()
                    self.expect("ID")
                    self.expect("IGUAL")
                    self.expect("NEW")
                    self.expect("BUSCAR_TODO")
                    self.expect("IPAREN")
                    self.expect("OPCOMILLAS", "CLCOMILLAS","NMCOMILLAS", "PCOMILLAS")
                    self.expect("ID")
                    collection_name = self.tokens[self.pos - 1][1]
                    self.expect("OPCOMILLAS", "CLCOMILLAS","NMCOMILLAS", "PCOMILLAS")
                    self.expect("DPAREN")
                    self.expect("PUNTOCOMA")
                    expresiones.append(("BUSCAR_TODO",collection_name))

                elif self.accept("BUSCAR_UNICO"):
                    self.saltar_espacioBlanco()
                    self.expect("ID")
                    self.expect("IGUAL")
                    self.expect("NEW")
                    self.expect("BUSCAR_UNICO")
                    self.expect("IPAREN")
                    self.expect("OPCOMILLAS", "CLCOMILLAS","NMCOMILLAS", "PCOMILLAS")
                    self.expect("ID")
                    collection_name = self.tokens[self.pos - 1][1]
                    self.expect("OPCOMILLAS", "CLCOMILLAS","NMCOMILLAS", "PCOMILLAS")
                    self.expect("DPAREN")
                    self.expect("PUNTOCOMA")
                    expresiones.append(("BUSCAR_UNICO",collection_name))

                elif self.accept("ID"):
                    self.saltar_espacioBlanco()
                    self.expect("IGUAL")
                    self.saltar_espacioBlanco()
                    self.expect("ID")
                    self.saltar_espacioBlanco()
                    self.expect("PUNTOCOMA")
                    expresiones.append(("ASSIGNMENT", self.tokens[self.pos - 3][1], self.tokens[self.pos - 1][1]))

                else:
                    raise SyntaxError(f"Error de sintaxis en la línea {self.tokens[self.pos][2]}")

        except Exception as e:
            print(f"Error: {e}")

        return expresiones

if __name__ == '__main__':
    input_str = """
    # (Your input file content goes here)
    """
    scanner = Scanner(input_str)
    tokens = scanner.initToken()
    parser = Parser(tokens)
    parser.parse()
