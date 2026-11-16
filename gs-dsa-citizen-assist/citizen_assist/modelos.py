"""Modelo dos registros (Servico) e do nó da lista encadeada (No)."""

CATEGORIAS = (
    "Saúde",
    "Assistência social",
    "Documentação e cidadania",
    "Educação e qualificação",
    "Serviços urbanos",
)

REGIOES = ("Centro", "Norte", "Sul", "Leste", "Oeste")

# campos textuais que podem ser pesquisados e atualizados
CAMPOS_TEXTO = ("titulo", "categoria", "descricao", "requisitos", "local", "regiao")


class Servico:
    """Um serviço ou orientação ao cidadão."""

    def __init__(self, id, titulo, categoria, descricao, requisitos, local, regiao):
        self.id = id
        self.titulo = titulo
        self.categoria = categoria
        self.descricao = descricao
        self.requisitos = requisitos
        self.local = local
        self.regiao = regiao

    @classmethod
    def de_dict(cls, d):
        return cls(int(d["id"]), d["titulo"], d["categoria"], d["descricao"],
                   d["requisitos"], d["local"], d["regiao"])

    def resumo(self):
        return f"[{self.id:>3}] {self.titulo} ({self.categoria} – {self.regiao})"

    def detalhes(self):
        return (
            f"ID .........: {self.id}\n"
            f"Título .....: {self.titulo}\n"
            f"Categoria ..: {self.categoria}\n"
            f"Descrição ..: {self.descricao}\n"
            f"Requisitos .: {self.requisitos}\n"
            f"Local ......: {self.local}\n"
            f"Região .....: {self.regiao}"
        )

    def __repr__(self):
        return f"Servico(id={self.id}, titulo={self.titulo!r})"


class No:
    """Nó da lista simplesmente encadeada: guarda o dado e a referência ao próximo nó."""

    def __init__(self, dado, proximo=None):
        self.dado = dado
        self.proximo = proximo
