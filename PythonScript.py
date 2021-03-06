#!/usr/bin/env pypy

import sys

# INITILIZE

ascii_ = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") # I know Python has isalpha function but this is my method ok

### -TYPE- ###

STRING = "STRING"
NUMBER = "NUMBER"
UNKNOWN = "UNKNOWN"

### -INDETIFIER- ###

ID = "ID"

### -OPERATOR- ###

OP = "OP"

### -OTHER- ###

PAREN = ["(",")"]
PAREN_ = "PAREN"
SEMICOLON = "SEMICOLON"
COMMENT = "COMMENT"

class Token():
    
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        
    def token(self):
        result = []
        result.append(self.type)
        if self.value:
            result.append(self.value)
        return result

class Lexer():
    
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.char = None
        self.Next()
        
    def Next(self):
        self.pos += 1
        if not self.pos > len(self.text) - 1:
            self.char = self.text[self.pos]
        else:
            self.char = "END"
            
    def Lexing(self):
        result = []
        
        while True:
            if self.char.isspace():
                pass
            elif self.char in ascii_:
                result.append(Token(ID, self.build_id()).token())
                continue
            elif self.char.isdigit():
                result.append(Token(NUMBER, self.build_num()).token())
                continue
            elif self.char in list("+-/*="):
                result.append(Token(OP, self.char).token())
            elif self.char in PAREN:
                result.append(Token(PAREN_, self.char).token())
            elif self.char == '"':
                self.Next()
                result.append(Token(STRING, self.build_string()).token())
                continue
            elif self.char == "END":
                break
            elif self.char == ";":
                result.append(Token(SEMICOLON).token())
            elif self.char == "#":
                self.Next()
                if self.char != "{":
                    result.append(Token(UNKNOWN, "#" + self.char).token())
                else:
                    result.append(Token(COMMENT, self.build_comment()).token())
            else:
                result.append(Token(UNKNOWN, self.char).token())
            self.Next()
        return result
                
    def build_id(self):
        result = ""
        assi = ascii_
        assi.append("_")
        
        while self.char in assi:
            result += self.char
            self.Next()
        return result
    
    def build_num(self):
        result = ""
        dot = 0
        
        while self.char.isdigit() or self.char == ".":
            if self.char.isspace():
                pass
            elif self.char == ".":
                dot += 1
                result += self.char
            else:
                result += self.char
            self.Next()
        if dot > 1:
            return f"ERROR:{result}"
        try:
            return int(result)
        except ValueError:
            return float(result)
        
    def build_string(self):
        result = ""
        
        while self.char not in ['"',"END"]:
            result += self.char
            self.Next()
        self.Next()
        return str(result)

    def build_comment(self):
        result = ""

        while self.char not in ["}","END"]:
            result += self.char
            self.Next()
        return result

class Parser():
    
    def __init__(self, tokens: list):
        self.tokens = tokens
        
    def action(self):
        result = ""
        for token in self.tokens:
            if token[0] == ID:
                if token[1] == "printCon":
                    result += "print"
                else:
                    print(f"Unknown ID: {token[1]}")
                    return None
            elif token[0] == PAREN_:
                result += token[1]
            elif token[0] == STRING:
                result += f"\"{token[1]}\""
            elif token[0] == SEMICOLON:
                result += "\n"
            elif token[0] == NUMBER:
                if type(token[1]) == str and token[1].startswith("ERROR"):
                    error = token[1].split(":")[1]
                    print(f"Build Number Error: {error}")
                    return None
                else:
                    result += str(token[1])
            elif token[0] == OP:
                result += token[1]
            elif token[0] == COMMENT:
                result += f"#{token[1]}\n"
            else:
                print(f"Unknown Tokens: {token[1]}")
                return None
        return result

if __name__ == "__main__":
    file_path = sys.argv[1]
    try:
        text = open(file_path, "r").read()
    except:
        print(f"File not found: {file_path}")
    else:
        text = text.splitlines()
        text = "".join(text)
        code = Lexer(text).Lexing()
        code = Parser(code).action()
        if code:
            try:
                exec(code)
            except Exception as Error:
                print(f"An Error Has Occured: " + Error.msg)