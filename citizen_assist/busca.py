"""Algoritmos de busca sobre a lista encadeada.

A lista encadeada não permite acesso direto à posição i (não há índice), então
a busca binária não se aplica: chegar ao meio da lista já custaria O(n).
Por isso é usada a busca sequencial (linear), que percorre os nós a partir da
cabeça comparando cada registro com o valor procurado.
"""
import unicodedata


def normalizar(texto):
    """Minúsculas e sem acentos, para que 'saude' encontre 'Saúde'."""
    decomposto = unicodedata.normalize("NFD", str(texto))
    sem_acento = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return " ".join(sem_acento.casefold().split())


def busca_sequencial_por_id(cabeca, id_procurado):
    """Retorna o nó cujo serviço tem o id procurado, ou None se não existir.

    Melhor caso O(1) (está na cabeça), pior caso O(n) (está no fim ou não existe).
    """
    atual = cabeca
    while atual is not None:
        if atual.dado.id == id_procurado:
            return atual
        atual = atual.proximo
    return None


def busca_sequencial_por_atributo(cabeca, campo, termo):
    """Retorna, na ordem da lista, todos os serviços cujo campo contém o termo.

    A comparação ignora maiúsculas e acentos e aceita trecho do texto
    ('identidade' encontra 'Emissão da Carteira de Identidade').
    Sempre percorre a lista inteira, porque pode haver vários resultados: O(n).
    Se nada for encontrado, a lista de resultados volta vazia.
    """
    alvo = normalizar(termo)
    resultados = []
    atual = cabeca
    while atual is not None:
        if alvo in normalizar(getattr(atual.dado, campo)):
            resultados.append(atual.dado)
        atual = atual.proximo
    return resultados
