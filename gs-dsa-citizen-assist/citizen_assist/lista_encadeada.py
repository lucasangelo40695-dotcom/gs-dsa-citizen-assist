"""Lista simplesmente encadeada de serviços, implementada pela equipe.

Guarda referências para o primeiro nó (cabeca) e para o último (cauda), além
da quantidade de nós. A cauda permite anexar no fim em O(1); o tamanho é
mantido a cada inserção e remoção para não precisar percorrer a lista.
"""
from .modelos import No, CAMPOS_TEXTO
from .busca import busca_sequencial_por_id, busca_sequencial_por_atributo
from .ordenacao import ALGORITMOS, chave_do_criterio


class IdDuplicadoError(ValueError):
    pass


class ListaEncadeada:
    def __init__(self):
        self.cabeca = None
        self.cauda = None
        self.tamanho = 0

    def __len__(self):
        return self.tamanho

    def esta_vazia(self):
        return self.cabeca is None

    # ------------------------------------------------------------- inserção
    def inserir(self, servico):
        """Insere no fim da lista. Recusa id repetido.

        A verificação de duplicidade é uma busca sequencial, O(n); o encadeamento
        no fim, graças à cauda, é O(1). Custo total: O(n).
        """
        if self.buscar_por_id(servico.id) is not None:
            raise IdDuplicadoError(f"já existe um serviço com o ID {servico.id}")
        novo = No(servico)
        if self.cabeca is None:      # lista vazia: o nó é cabeça e cauda
            self.cabeca = self.cauda = novo
        else:
            self.cauda.proximo = novo
            self.cauda = novo
        self.tamanho += 1
        return novo

    # ------------------------------------------------------------- percurso
    def percorrer(self):
        """Gera os serviços da cabeça até a cauda, seguindo as referências. O(n)."""
        atual = self.cabeca
        while atual is not None:
            yield atual.dado
            atual = atual.proximo

    def __iter__(self):
        return self.percorrer()

    def ids(self):
        return [s.id for s in self.percorrer()]

    def representacao(self):
        """Mostra o encadeamento, ex.: 'cabeça → [3] → [1] → [7] → None'."""
        if self.esta_vazia():
            return "cabeça → None (lista vazia)"
        return "cabeça → " + " → ".join(f"[{i}]" for i in self.ids()) + " → None"

    # ------------------------------------------------------------- busca
    def buscar_por_id(self, id_procurado):
        no = busca_sequencial_por_id(self.cabeca, id_procurado)
        return no.dado if no is not None else None

    def pesquisar(self, campo, termo):
        if campo not in CAMPOS_TEXTO:
            raise ValueError(f"campo inválido: {campo!r}")
        return busca_sequencial_por_atributo(self.cabeca, campo, termo)

    # ------------------------------------------------------------- atualização
    def atualizar(self, id_servico, **campos):
        """Altera os campos informados do serviço. Retorna o serviço ou None. O(n)."""
        servico = self.buscar_por_id(id_servico)
        if servico is None:
            return None
        for campo, valor in campos.items():
            if campo not in CAMPOS_TEXTO:
                raise ValueError(f"campo inválido: {campo!r}")
            setattr(servico, campo, valor)
        return servico

    # ------------------------------------------------------------- remoção
    def remover(self, id_servico):
        """Remove o nó com o id e devolve o serviço removido (ou None). O(n).

        Percorre mantendo o nó anterior, porque numa lista simplesmente
        encadeada é o anterior que precisa passar a apontar para o seguinte.
        """
        anterior, atual = None, self.cabeca
        while atual is not None and atual.dado.id != id_servico:
            anterior, atual = atual, atual.proximo
        if atual is None:            # lista vazia ou id inexistente
            return None
        if anterior is None:         # remoção da cabeça
            self.cabeca = atual.proximo
        else:                        # remoção do meio ou do fim
            anterior.proximo = atual.proximo
        if atual is self.cauda:      # removeu o último: a cauda volta para o anterior
            self.cauda = anterior
        atual.proximo = None
        self.tamanho -= 1
        return atual.dado

    # ------------------------------------------------------------- ordenação
    def ordenar(self, criterio="id", algoritmo="merge", decrescente=False):
        """Reordena os nós da própria lista e reajusta a cauda."""
        if algoritmo not in ALGORITMOS:
            raise ValueError(f"algoritmo inválido: {algoritmo!r}")
        chave = chave_do_criterio(criterio)
        self.cabeca = ALGORITMOS[algoritmo](self.cabeca, chave, decrescente)
        self.cauda = self.cabeca
        while self.cauda is not None and self.cauda.proximo is not None:
            self.cauda = self.cauda.proximo
