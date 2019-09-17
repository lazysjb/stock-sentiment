import re
import string

from nltk.corpus import stopwords

from nlp.twokenize import (
    normalizeTextForTagger, tokenize
)


_CASH_TAG_PATTERN = '\$[A-Z]{2,4}'
_PUNCTUATION_SET = set(string.punctuation)
# Important words that should move out of stop word list
_NON_STOP_WORDS = {
    'above',
    "aren't",
    'below',
    "couldn't",
    "didn't",
    "doesn't",
    "don't",
    "down",
    "hadn't",
    "hasn't",
    "haven't",
    "isn't",
    'more',
    'not',
    'off',
    'on',
    'out',
    "shouldn't",
    'under',
    'up',
    "wasn't",
    "won't",
    "wouldn't",
}
_NLTK_STOP_WORDS = set(stopwords.words('english')) - _NON_STOP_WORDS


def token_is_cash_tag(token):
    """Define tokens with $ and 2-4 letter CAPS as ticker"""
    search_result = re.search(_CASH_TAG_PATTERN, token)
    if search_result is None:
        return False
    else:
        return True


def token_matches_ticker(token, ticker):
    """Returns true if token matches ticker"""
    return token.lower() == ticker.lower()


def token_is_punct(token):
    """Returns true if token consists of only punctuation symbols"""
    if set(token).issubset(_PUNCTUATION_SET):
        return True
    else:
        return False


def token_is_stopword(token):
    return token.lower() in _NLTK_STOP_WORDS


def token_is_non_ascii(token):
    """To remove tokens not convertible to ascii"""
    pass


def process_token(token, lowercase=True, stem=True):
    """Apply processing to raw token"""
    tok = token

    if lowercase:
        tok = tok.lower()

    return tok


def twit_tokenize(raw_twit, ticker=None, normalize=True):
    twit = raw_twit

    if normalize:
        twit = normalizeTextForTagger(twit)

    tokenized_init = tokenize(twit)
    tokenized_result = []

    for tok in tokenized_init:
        if token_is_cash_tag(tok):
            continue

        if token_is_punct(tok):
            continue

        if (ticker is not None) and (token_matches_ticker(tok, ticker)):
            continue

        if token_is_stopword(tok):
            continue

        processed_tok = process_token(tok, lowercase=True, stem=False)
        tokenized_result.append(processed_tok)

    return tokenized_result
