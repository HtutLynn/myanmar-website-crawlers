import re

class Tokenizer():
    #TO-DO multithreading for very large file
    def __init__(self,bySpace = False):
        self.bySpace= bySpace
        

    def tokenize(self,data):
        if type(data) == list:
            if any(isinstance(datum, int) for datum in data):
                raise ValueError('all elements in the list must be type of string. ')
            else:
                return list(map(self.get_token,data))
        elif type(data) == str:
            return self.get_token(data)
        else:
            raise ValueError('data must be string or list of string')

    def get_token(self,string):
        if self.bySpace:
            return string.strip(' ').split(' ')
        else:
            return list(
            filter(lambda s: not(s.isspace()),
            re.sub(r'(?:(?<!.\([က-အ][္်]|\([က-အ][ှျ][္်])(?<!္)([က-ဪဿ၊-၏]|[ ]+|((?:[၀-၉0-9]+[.]){2})[၀-၉0-9]+|((?:[၀-၉0-9]+[-]){2})[၀-၉0-9]+|[+-]?([၀-၉0-9]*[.])?[၀-၉0-9]+|[\-]|[^က-၏\.?!, )(]+|[.,?!)(])(?![ှျ]?[့္်]))',
            r'𝕊\1', string).strip('𝕊').split('𝕊'))
            )