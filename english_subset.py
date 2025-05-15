# sentence     = noun-phrase , verb-phrase , ? end of input ? ;
# noun-phrase  = article , { adjective } , noun ;                (* UPDATED *)
# verb-phrase  = [ adverb ] , verb , [ noun_phrase ] ;           (* UPDATED *)
# article      = "the" | "a" ;
# noun         = "man" | "ball" | "woman" | "table" ;
# verb         = "hit" | "took" | "saw" | "liked" ;
# adjective    = "digital" | "virtual" | "cyber" | "pixelated" ; (* NEW *)
# adverb       = "algorithmically" | "securely" | "wirelessly" | "recursively" ; (* NEW *)

class ParserError(Exception):

    def __init__(self, message):
        super().__init__(f'PARSER ERROR DETECTED:\n{message}')


class Parser:

    EOI = '? end of input ?'
    ADVERBS = ["algorithmically", "securely", "wirelessly", "recursively"]
    ARTICLES = ["the", "a"]
    ADJECTIVES = ["digital", "virtual", "cyber", "pixelated"]

    def __init__(self, source):
        self._tokens = iter(source.split() + [self.EOI])
        self.advance()

    def advance(self):
        try:
            self._current = next(self._tokens)
        except StopIteration:
            self._current = None

    def expect(self, expected_tokens):
        if self._current not in expected_tokens:
            token_found_str = f'"{self._current}"'
            expected_tokens_str = \
                ", ".join([f'"{token}"' for token in expected_tokens])
            message = (f'Found the token: {token_found_str}\n'
                       f'But was expecting one of: {expected_tokens_str}')
            raise ParserError(message)
        original_current = self._current
        self.advance()
        return original_current

    def sentence(self):
        self.noun_phrase()
        self.verb_phrase()
        self.expect([self.EOI])

    def noun_phrase(self):
        self.article()
        while self._current in self.ADJECTIVES:
            self.adjective()
        self.noun()

    def verb_phrase(self):
        if self._current in self.ADVERBS:
            self.adverb()
        self.verb()
        if self._current in self.ARTICLES:
            self.noun_phrase()

    def article(self):
        self.expect(self.ARTICLES)

    def noun(self):
        self.expect(["man", "ball", "woman", "table"])

    def verb(self):
        self.expect(["hit", "took", "saw", "liked"])

    def adjective(self):
        self.expect(self.ADJECTIVES)

    def adverb(self):
        self.expect(self.ADVERBS)

if __name__ == '__main__':
    # parser_example = Parser('the man hit the ball')
    # parser_example = Parser('a woman saw a table')
    # parser_example = Parser('a woman saw a table again')
    # parser_example = Parser('a woman saw')
    # parser_example = Parser('the virtual digital man algorithmically hit a pixelated ball')
    # parser_example = Parser('the cyber table wirelessly')
    parser_example = Parser('a woman recursively saw a digital ball')
    try:
        parser_example.sentence()
        print('Syntax OK!')
    except ParserError as e:
        print(e)
