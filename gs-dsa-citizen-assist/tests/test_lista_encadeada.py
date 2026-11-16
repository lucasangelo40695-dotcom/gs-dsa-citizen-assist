import unittest

from citizen_assist.lista_encadeada import ListaEncadeada, IdDuplicadoError
from citizen_assist.modelos import Servico


def servico(id, titulo="Serviço", categoria="Saúde", regiao="Centro"):
    return Servico(id, titulo, categoria, "descrição", "requisitos", "local", regiao)


def lista_com(*ids):
    lista = ListaEncadeada()
    for i in ids:
        lista.inserir(servico(i, f"Serviço {i}"))
    return lista


class TestInsercao(unittest.TestCase):
    def test_inserir_em_lista_vazia_define_cabeca_e_cauda(self):
        lista = ListaEncadeada()
        lista.inserir(servico(1))
        self.assertIs(lista.cabeca, lista.cauda)
        self.assertEqual(len(lista), 1)

    def test_insere_no_fim_mantendo_a_ordem(self):
        lista = lista_com(3, 1, 2)
        self.assertEqual(lista.ids(), [3, 1, 2])
        self.assertEqual(lista.cauda.dado.id, 2)
        self.assertIsNone(lista.cauda.proximo)

    def test_id_duplicado_e_recusado_sem_alterar_a_lista(self):
        lista = lista_com(1, 2)
        with self.assertRaises(IdDuplicadoError):
            lista.inserir(servico(2))
        self.assertEqual(lista.ids(), [1, 2])
        self.assertEqual(len(lista), 2)


class TestPercurso(unittest.TestCase):
    def test_percurso_de_lista_vazia_nao_gera_nada(self):
        self.assertEqual(list(ListaEncadeada().percorrer()), [])

    def test_representacao(self):
        self.assertEqual(lista_com(5, 7).representacao(), "cabeça → [5] → [7] → None")
        self.assertEqual(ListaEncadeada().representacao(), "cabeça → None (lista vazia)")


class TestRemocao(unittest.TestCase):
    def test_remover_cabeca(self):
        lista = lista_com(1, 2, 3)
        self.assertEqual(lista.remover(1).id, 1)
        self.assertEqual(lista.ids(), [2, 3])
        self.assertEqual(lista.cabeca.dado.id, 2)

    def test_remover_meio(self):
        lista = lista_com(1, 2, 3)
        lista.remover(2)
        self.assertEqual(lista.ids(), [1, 3])
        self.assertIs(lista.cabeca.proximo, lista.cauda)

    def test_remover_cauda_atualiza_a_cauda(self):
        lista = lista_com(1, 2, 3)
        lista.remover(3)
        self.assertEqual(lista.cauda.dado.id, 2)
        lista.inserir(servico(4))  # a cauda precisa estar correta para anexar no fim
        self.assertEqual(lista.ids(), [1, 2, 4])

    def test_remover_unico_elemento_esvazia_a_lista(self):
        lista = lista_com(1)
        lista.remover(1)
        self.assertTrue(lista.esta_vazia())
        self.assertIsNone(lista.cauda)
        self.assertEqual(len(lista), 0)

    def test_remover_inexistente_retorna_none(self):
        lista = lista_com(1, 2)
        self.assertIsNone(lista.remover(99))
        self.assertEqual(lista.ids(), [1, 2])

    def test_remover_de_lista_vazia_retorna_none(self):
        self.assertIsNone(ListaEncadeada().remover(1))


class TestAtualizacao(unittest.TestCase):
    def test_atualizar_campos(self):
        lista = lista_com(1)
        lista.atualizar(1, titulo="Novo título", regiao="Sul")
        s = lista.buscar_por_id(1)
        self.assertEqual((s.titulo, s.regiao), ("Novo título", "Sul"))

    def test_atualizar_inexistente_retorna_none(self):
        self.assertIsNone(lista_com(1).atualizar(5, titulo="x"))

    def test_atualizar_campo_invalido(self):
        with self.assertRaises(ValueError):
            lista_com(1).atualizar(1, id=9)


if __name__ == "__main__":
    unittest.main()
