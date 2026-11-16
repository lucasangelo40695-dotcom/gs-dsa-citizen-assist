"""Algoritmos de ordenação implementados pela equipe sobre os nós da lista.

Os dois algoritmos reorganizam os próprios nós (trocam as referências
'proximo'); os objetos Servico não são copiados e nenhuma função pronta de
ordenação (sorted, list.sort) é usada.

* Merge Sort  – O(n log n) em qualquer caso; estável. Algoritmo padrão do menu.
* Insertion Sort – O(n²) no pior caso e O(n) se a lista já estiver ordenada; estável.
"""
from .busca import normalizar

CRITERIOS = {
    "id": lambda s: s.id,
    "titulo": lambda s: normalizar(s.titulo),
    "categoria": lambda s: (normalizar(s.categoria), normalizar(s.titulo)),
}


def chave_do_criterio(criterio):
    if criterio not in CRITERIOS:
        raise ValueError(f"critério inválido: {criterio!r}")
    return CRITERIOS[criterio]


# ----------------------------------------------------------------- Merge Sort
def merge_sort(cabeca, chave, decrescente=False):
    """Ordena a lista que começa em 'cabeca' e retorna a nova cabeça."""
    if cabeca is None or cabeca.proximo is None:  # 0 ou 1 nó: já ordenada
        return cabeca
    esquerda, direita = _dividir(cabeca)
    esquerda = merge_sort(esquerda, chave, decrescente)
    direita = merge_sort(direita, chave, decrescente)
    return _intercalar(esquerda, direita, chave, decrescente)


def _dividir(cabeca):
    """Divide a lista ao meio com dois ponteiros: 'lento' anda 1 nó e 'rapido' anda 2."""
    lento, rapido = cabeca, cabeca.proximo
    while rapido is not None and rapido.proximo is not None:
        lento = lento.proximo
        rapido = rapido.proximo.proximo
    meio = lento.proximo
    lento.proximo = None  # corta a ligação entre as duas metades
    return cabeca, meio


def _vem_antes(a, b, chave, decrescente):
    # '<=' (e '>=') mantém a ordem original dos empates: ordenação estável
    return chave(a.dado) >= chave(b.dado) if decrescente else chave(a.dado) <= chave(b.dado)


def _intercalar(a, b, chave, decrescente):
    """Junta duas listas ordenadas religando os nós, sem criar nós novos."""
    sentinela = cauda = _Sentinela()
    while a is not None and b is not None:
        if _vem_antes(a, b, chave, decrescente):
            cauda.proximo, a = a, a.proximo
        else:
            cauda.proximo, b = b, b.proximo
        cauda = cauda.proximo
    cauda.proximo = a if a is not None else b  # o que sobrou já está ordenado
    return sentinela.proximo


class _Sentinela:
    """Nó auxiliar que evita tratar a primeira inserção como caso especial."""
    proximo = None


# ----------------------------------------------------------------- Insertion Sort
def insertion_sort(cabeca, chave, decrescente=False):
    """Retira cada nó da lista original e o insere na posição certa da lista ordenada."""
    ordenada = None      # cabeça da parte já ordenada
    fim_ordenada = None  # último nó da parte ordenada (atalho para o caso já ordenado)
    atual = cabeca
    while atual is not None:
        seguinte = atual.proximo
        atual.proximo = None
        if ordenada is None:
            ordenada = fim_ordenada = atual
        elif _vem_antes(fim_ordenada, atual, chave, decrescente):
            fim_ordenada.proximo = atual          # maior ou igual a todos: vai para o fim, O(1)
            fim_ordenada = atual
        elif not _vem_antes(ordenada, atual, chave, decrescente):
            atual.proximo = ordenada              # menor que todos: vira a nova cabeça
            ordenada = atual
        else:
            anterior = ordenada                   # procura o último nó que vem antes de 'atual'
            while _vem_antes(anterior.proximo, atual, chave, decrescente):
                anterior = anterior.proximo
            atual.proximo = anterior.proximo
            anterior.proximo = atual
        atual = seguinte
    return ordenada


ALGORITMOS = {"merge": merge_sort, "insertion": insertion_sort}
