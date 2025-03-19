import tiktoken
import nltk

nltk.download('punkt')

class TokenLimitedString:
    def __init__(self, max_tokens=2000, encoding_name="cl100k_base"):
        self.max_tokens = max_tokens
        self.encoder = tiktoken.get_encoding(encoding_name)
        self._sentences = []

    def add_data(self, new_data):
        new_sentences = nltk.sent_tokenize(new_data)
        self._sentences.extend(new_sentences)
        while True:
            current_tokens = self.encoder.encode(" ".join(self._sentences))
            if len(current_tokens) <= self.max_tokens:
                break
            self._sentences.pop(0)

    @property
    def tokens(self):
        return self.encoder.encode(" ".join(self._sentences))

    @property
    def value(self):
        return " ".join(self._sentences)

    @property
    def clear_memory(self):
        self._sentences = []
        return True
