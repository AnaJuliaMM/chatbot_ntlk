from functools import lru_cache
 
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
 
 
# ---------------------------------------------------------------------------
# 1. Recursos do NLTK (carregados uma única vez)
# ---------------------------------------------------------------------------
 
RECURSOS_NLTK = {
    "rslp": "stemmers/rslp",
    "stopwords": "corpora/stopwords",
    "punkt_tab": "tokenizers/punkt_tab",
}
 
 
@lru_cache(maxsize=1)
def carregar_recursos():
    """Baixa os pacotes do NLTK só se ainda não existirem e devolve
    as stopwords e o stemmer prontos para uso."""
    for pacote, caminho in RECURSOS_NLTK.items():
        try:
            nltk.data.find(caminho)
        except LookupError:
            nltk.download(pacote, quiet=True)
 
    stopwords_ptbr = set(stopwords.words("portuguese"))
    stemmer = RSLPStemmer()
    return stopwords_ptbr, stemmer
 
 
# ---------------------------------------------------------------------------
# 2. Dicionários do chatbot
# ---------------------------------------------------------------------------
 
ENTIDADES = {
    "maquina": ["máquin", "maquin", "equip", "ativ", "maquinari", "disposi"],
    "manutencao": ["ajust", "repar", "manutenç", "manutenc", "intervenç",
                   "intervenca", "consert", "revis", "revisa", "regul"],
}

INTENCOES = {
    "comprar": ["compr", "vend", "adquir"],
    "consultar": ["consult", "ver", "dispon", "disponibil"],
    "agendar": ["agend", "program", "marc"],
    "cancelar": ["cancel", "anul", "abort", "sust", "revog", "invalid"],
}

MATRIZ_RESPOSTA = {
    "maquina": {
        "comprar": "Mando o PIX na chave XXX",
        "consultar": "Segue o nosso catálogo em anexo",
    },
    "manutencao": {
        "agendar": "Informe o local e o horário",
        "cancelar": "Agendamento cancelado com sucesso",
    },
}

# ---------------------------------------------------------------------------
# 3. Funções de processamento
# ---------------------------------------------------------------------------
 
def identificar_tokens(mensagem):
    return word_tokenize(mensagem.lower(), language="portuguese")
 
 
def remover_stopwords(tokens):
    stopwords_ptbr, _ = carregar_recursos()
    return [t for t in tokens if t not in stopwords_ptbr and t.isalpha()]
 
 
def criar_stemmings(tokens):
    _, stemmer = carregar_recursos()
    return [stemmer.stem(t) for t in tokens]
 
 
def buscar_no_dicionario(stemmings, dicionario):
    """Devolve a primeira chave do dicionário cujo radical aparece na mensagem.
    Serve tanto para entidades quanto para intenções."""
    for token in stemmings:
        for chave, radicais in dicionario.items():
            if token in radicais:
                return chave
    return None
 
 
def identificar_entidade(lista_stemmings):
    for token in lista_stemmings:
        for entidade, lista_sinonimos in ENTIDADES.items():
            if token in lista_sinonimos:
                return entidade
 
 
def identificar_intencao(lista_stemmings):
    for token in lista_stemmings:
        for intencao, lista_sinonimos in INTENCOES.items():
            if token in lista_sinonimos:
                return intencao
 
 
def responder(entidade, intencao):
    if (entidade in MATRIZ_RESPOSTA) and (intencao in MATRIZ_RESPOSTA[entidade]):
        return MATRIZ_RESPOSTA[entidade][intencao]
    return "Desculpe, não posso ajudar!"
 
 
# ---------------------------------------------------------------------------
# 4. Função principal (é a única que o app.py precisa chamar)
# ---------------------------------------------------------------------------
 
def processar_mensagem(mensagem):
    tokens = identificar_tokens(mensagem)
    tokens_filtrados = remover_stopwords(tokens)
    stemmings = criar_stemmings(tokens_filtrados)
 
    entidade = identificar_entidade(stemmings)
    intencao = identificar_intencao(stemmings)
 
    return responder(entidade, intencao)