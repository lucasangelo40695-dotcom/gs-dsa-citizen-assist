"""Citizen Assist AI – ponto de entrada do sistema.

Uso:
    python main.py            # carrega os 20 serviços de exemplo (dados/servicos_exemplo.json)
    python main.py --vazio    # começa com a lista vazia
"""
import argparse
import json
import os
import sys

from citizen_assist.menu import Menu
from citizen_assist.lista_encadeada import ListaEncadeada
from citizen_assist.modelos import Servico

RAIZ = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_EXEMPLO = os.path.join(RAIZ, "dados", "servicos_exemplo.json")


def carregar_exemplo(caminho=ARQUIVO_EXEMPLO):
    """Lê a base de exemplo e insere cada serviço na lista encadeada."""
    lista = ListaEncadeada()
    with open(caminho, encoding="utf-8") as f:
        for registro in json.load(f):
            lista.inserir(Servico.de_dict(registro))
    return lista


def main():
    for fluxo in (sys.stdout, sys.stdin):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Citizen Assist AI – catálogo de serviços ao cidadão")
    parser.add_argument("--vazio", action="store_true", help="inicia com a lista vazia")
    args = parser.parse_args()

    if args.vazio:
        lista = ListaEncadeada()
    else:
        lista = carregar_exemplo()
        print(f"{len(lista)} serviço(s) de exemplo carregado(s).")

    Menu(lista).executar()


if __name__ == "__main__":
    main()
