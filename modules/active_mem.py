import tiktoken
import nltk

nltk.download('punkt')

class TokenLimitedString:
    def __init__(self, max_tokens=2000, encoding_name="cl100k_base"):
        self.max_tokens = max_tokens
        self.encoder = tiktoken.get_encoding(encoding_name)
        self._sentences = []  # Stores sentences instead of raw tokens

    def add_data(self, new_data):
        # Break the new data into sentences
        new_sentences = nltk.sent_tokenize(new_data)
        self._sentences.extend(new_sentences)

        # Manage tokens to ensure we stay within the max token limit
        while True:
            # Tokenize the current text
            current_tokens = self.encoder.encode(" ".join(self._sentences))
            if len(current_tokens) <= self.max_tokens:
                break
            # Remove the oldest sentence if we're over the limit
            self._sentences.pop(0)

    @property
    def tokens(self):
        return self.encoder.encode(" ".join(self._sentences))

    @property
    def value(self):
        return " ".join(self._sentences)
    