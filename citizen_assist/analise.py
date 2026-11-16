"""Processamento dos registros: totais e distribuição por categoria e por região."""
from .modelos import CATEGORIAS, REGIOES


def contar_por(lista, campo, valores):
    """Conta, em um único percurso O(n), quantos serviços há para cada valor do campo."""
    contagem = {v: 0 for v in valores}
    for servico in lista.percorrer():
        valor = getattr(servico, campo)
        contagem[valor] = contagem.get(valor, 0) + 1
    return contagem


def gerar_analise(lista):
    total = len(lista)
    por_categoria = contar_por(lista, "categoria", CATEGORIAS)
    por_regiao = contar_por(lista, "regiao", REGIOES)
    predominante = None
    for categoria, qtd in por_categoria.items():
        if qtd > 0 and (predominante is None or qtd > por_categoria[predominante]):
            predominante = categoria
    sem_oferta = [c for c, qtd in por_categoria.items() if qtd == 0]
    return {
        "total": total,
        "por_categoria": por_categoria,
        "por_regiao": por_regiao,
        "categoria_predominante": predominante,
        "categorias_sem_servico": sem_oferta,
    }


def formatar_analise(analise):
    total = analise["total"]
    if total == 0:
        return "Nenhum serviço cadastrado: não há dados para analisar."

    def bloco(titulo, contagem):
        maior = max(len(k) for k in contagem)
        linhas = [titulo]
        for chave, qtd in contagem.items():
            pct = f"{100 * qtd / total:5.1f}".replace(".", ",")
            linhas.append(f"  {chave:<{maior}}  {qtd:>3}  {pct}%  {'█' * qtd}")
        return "\n".join(linhas)

    partes = [
        f"Total de serviços cadastrados: {total}",
        "",
        bloco("Serviços por categoria:", analise["por_categoria"]),
        "",
        bloco("Serviços por região de atendimento:", analise["por_regiao"]),
        "",
        f"Categoria com mais serviços: {analise['categoria_predominante']}",
    ]
    if analise["categorias_sem_servico"]:
        partes.append("Categorias sem nenhum serviço: " + ", ".join(analise["categorias_sem_servico"]))
    return "\n".join(partes)
