"""Testes do menu com entradas simuladas (casos normais, inválidos e lista vazia)."""
import unittest

from citizen_assist.menu import Menu
from citizen_assist.lista_encadeada import ListaEncadeada
from citizen_assist.modelos import Servico


def executar(entradas, lista=None):
    fila = list(entradas)
    saidas = []

    def entrada(prompt):
        saidas.append(prompt)
        if not fila:
            raise EOFError
        return fila.pop(0)

    menu = Menu(lista, entrada=entrada, saida=lambda *a: saidas.append(" ".join(map(str, a))))
    menu.executar()
    return menu, "\n".join(saidas)


def lista_exemplo():
    lista = ListaEncadeada()
    lista.inserir(Servico(2, "Emissão de CPF", "Documentação e cidadania", "d", "r", "Correios", "Centro"))
    lista.inserir(Servico(1, "Vacinação", "Saúde", "d", "r", "UBS", "Leste"))
    return lista


CADASTRO_VALIDO = ["1", "7", "Coleta seletiva", "5", "Recolhimento de recicláveis", "Nenhum", "Central 156", "3"]


class TestMenu(unittest.TestCase):
    def test_cadastro_valido(self):
        menu, saida = executar(CADASTRO_VALIDO + ["0"])
        self.assertIn("Serviço 7 cadastrado com sucesso", saida)
        s = menu.lista.buscar_por_id(7)
        self.assertEqual((s.categoria, s.regiao), ("Serviços urbanos", "Sul"))

    def test_cadastro_com_id_duplicado_pede_outro(self):
        menu, saida = executar(["1", "1", "9", "Título", "1", "desc", "req", "local", "1", "0"], lista_exemplo())
        self.assertIn("ID duplicado: já existe um serviço com o ID 1", saida)
        self.assertEqual(menu.lista.ids(), [2, 1, 9])

    def test_entradas_invalidas_no_cadastro(self):
        entradas = ["1", "abc", "-5", "8", "", "Título", "9", "x", "2", "desc", "req", "local", "1", "0"]
        menu, saida = executar(entradas)
        self.assertIn("'abc' não é um número inteiro", saida)
        self.assertIn("Valor fora do intervalo", saida)
        self.assertIn("Campo obrigatório", saida)
        self.assertEqual(menu.lista.buscar_por_id(8).categoria, "Assistência social")

    def test_opcao_inexistente(self):
        _, saida = executar(["42", "x", "0"])
        self.assertIn("Opção inexistente: '42'", saida)
        self.assertIn("Opção inexistente: 'x'", saida)

    def test_consulta_existente_e_inexistente(self):
        _, saida = executar(["2", "1", "2", "99", "0"], lista_exemplo())
        self.assertIn("Título .....: Vacinação", saida)
        self.assertIn("Nenhum serviço encontrado com o ID 99", saida)

    def test_operacoes_com_lista_vazia(self):
        _, saida = executar(["2", "3", "4", "5", "6", "7", "8", "0"])
        self.assertEqual(saida.count("A lista está vazia"), 6)
        self.assertIn("não há dados para analisar", saida)

    def test_atualizar_mantendo_campos_com_enter(self):
        menu, saida = executar(["3", "1", "Vacinação contra gripe", "", "", "", "", "2", "0"], lista_exemplo())
        s = menu.lista.buscar_por_id(1)
        self.assertEqual((s.titulo, s.descricao, s.categoria, s.regiao), ("Vacinação contra gripe", "d", "Saúde", "Norte"))
        self.assertIn("atualizado: titulo, regiao", saida)

    def test_excluir_com_confirmacao_e_cancelamento(self):
        menu, saida = executar(["4", "1", "talvez", "n", "4", "1", "s", "0"], lista_exemplo())
        self.assertIn("Exclusão cancelada", saida)
        self.assertIn("Responda com 's' ou 'n'", saida)
        self.assertEqual(menu.lista.ids(), [2])

    def test_pesquisa_com_e_sem_resultado(self):
        _, saida = executar(["5", "2", "saude", "5", "1", "passaporte", "0"], lista_exemplo())
        self.assertIn("1 serviço(s) encontrado(s)", saida)
        self.assertIn("Nenhum serviço encontrado para 'passaporte'", saida)

    def test_ordenar_pelo_menu(self):
        menu, saida = executar(["6", "1", "1", "2", "0"], lista_exemplo())
        self.assertEqual(menu.lista.ids(), [1, 2])
        self.assertIn("Insertion Sort", saida)
        self.assertIn("cabeça → [1] → [2] → None", saida)

    def test_analise(self):
        _, saida = executar(["8", "0"], lista_exemplo())
        self.assertIn("Total de serviços cadastrados: 2", saida)
        self.assertIn("Categorias sem nenhum serviço", saida)

    def test_fim_da_entrada_encerra_sem_erro(self):
        _, saida = executar(["1", "5"])
        self.assertIn("Sistema encerrado", saida)


if __name__ == "__main__":
    unittest.main()
