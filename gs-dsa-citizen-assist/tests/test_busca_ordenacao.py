import random
import unittest

from citizen_assist.lista_encadeada import ListaEncadeada
from citizen_assist.modelos import Servico
from citizen_assist.busca import normalizar


def montar(registros):
    lista = ListaEncadeada()
    for id, titulo, categoria in registros:
        lista.inserir(Servico(id, titulo, categoria, "d", "r", "Central 156", "Centro"))
    return lista


BASE = [
    (30, "Vacinação", "Saúde"),
    (10, "Emissão de CPF", "Documentação e cidadania"),
    (20, "Árvore: poda", "Serviços urbanos"),
    (40, "Consulta médica", "Saúde"),
]


class TestBusca(unittest.TestCase):
    def test_busca_por_id_encontrada_no_inicio_meio_e_fim(self):
        lista = montar(BASE)
        for id in (30, 20, 40):
            self.assertEqual(lista.buscar_por_id(id).id, id)

    def test_busca_por_id_inexistente(self):
        self.assertIsNone(montar(BASE).buscar_por_id(99))

    def test_busca_em_lista_vazia(self):
        lista = ListaEncadeada()
        self.assertIsNone(lista.buscar_por_id(1))
        self.assertEqual(lista.pesquisar("titulo", "x"), [])

    def test_pesquisa_ignora_acentos_e_maiusculas(self):
        resultado = montar(BASE).pesquisar("categoria", "SAUDE")
        self.assertEqual([s.id for s in resultado], [30, 40])

    def test_pesquisa_por_trecho(self):
        self.assertEqual([s.id for s in montar(BASE).pesquisar("titulo", "cpf")], [10])

    def test_pesquisa_sem_resultado(self):
        self.assertEqual(montar(BASE).pesquisar("titulo", "passaporte"), [])

    def test_pesquisa_campo_invalido(self):
        with self.assertRaises(ValueError):
            montar(BASE).pesquisar("senha", "x")

    def test_normalizar(self):
        self.assertEqual(normalizar("  Documentação  e Cidadania "), "documentacao e cidadania")


class TestOrdenacao(unittest.TestCase):
    def verificar(self, criterio, esperado, decrescente=False):
        for algoritmo in ("merge", "insertion"):
            with self.subTest(algoritmo=algoritmo):
                lista = montar(BASE)
                lista.ordenar(criterio, algoritmo, decrescente)
                self.assertEqual(lista.ids(), esperado)
                self.assertIs(lista.cauda.dado.id, esperado[-1])
                self.assertIsNone(lista.cauda.proximo)
                self.assertEqual(len(lista), len(esperado))

    def test_ordenar_por_id(self):
        self.verificar("id", [10, 20, 30, 40])

    def test_ordenar_por_id_decrescente(self):
        self.verificar("id", [40, 30, 20, 10], decrescente=True)

    def test_ordenar_por_titulo_ignora_acento(self):
        # "Árvore" deve ficar no "A", e não depois do "Z"
        self.verificar("titulo", [20, 40, 10, 30])

    def test_ordenar_por_categoria_e_titulo(self):
        self.verificar("categoria", [10, 40, 30, 20])

    def test_ordenar_lista_vazia_e_unitaria(self):
        for algoritmo in ("merge", "insertion"):
            vazia = ListaEncadeada()
            vazia.ordenar("id", algoritmo)
            self.assertTrue(vazia.esta_vazia())
            self.assertIsNone(vazia.cauda)
            unitaria = montar(BASE[:1])
            unitaria.ordenar("titulo", algoritmo)
            self.assertEqual(unitaria.ids(), [30])

    def test_estabilidade(self):
        # mesmos títulos: a ordem original (por id) deve ser preservada
        registros = [(i, "Mesmo título", "Saúde") for i in (5, 3, 9, 1)]
        for algoritmo in ("merge", "insertion"):
            lista = montar(registros)
            lista.ordenar("titulo", algoritmo)
            self.assertEqual(lista.ids(), [5, 3, 9, 1])

    def test_aleatorio_igual_ao_resultado_esperado(self):
        gerador = random.Random(42)
        ids = gerador.sample(range(1, 10_000), 300)
        for algoritmo in ("merge", "insertion"):
            lista = montar([(i, f"S{i}", "Saúde") for i in ids])
            lista.ordenar("id", algoritmo)
            atual = lista.ids()
            self.assertTrue(all(atual[k] < atual[k + 1] for k in range(len(atual) - 1)))
            self.assertEqual(set(atual), set(ids))

    def test_criterio_e_algoritmo_invalidos(self):
        with self.assertRaises(ValueError):
            montar(BASE).ordenar("cor", "merge")
        with self.assertRaises(ValueError):
            montar(BASE).ordenar("id", "bubble")


if __name__ == "__main__":
    unittest.main()
