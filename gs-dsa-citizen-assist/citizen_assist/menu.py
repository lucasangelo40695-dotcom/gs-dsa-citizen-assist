"""Menu interativo em terminal, com validação das entradas.

As funções de entrada e saída são injetáveis (por padrão input e print), o que
permite executar o menu com entradas simuladas nos testes automatizados.
"""
from .lista_encadeada import ListaEncadeada, IdDuplicadoError
from .modelos import Servico, CATEGORIAS, REGIOES
from .analise import gerar_analise, formatar_analise

OPCOES = (
    ("1", "Cadastrar serviço"),
    ("2", "Consultar serviço por ID"),
    ("3", "Atualizar serviço"),
    ("4", "Excluir serviço"),
    ("5", "Pesquisar serviços"),
    ("6", "Ordenar e exibir serviços"),
    ("7", "Listar todos (percurso da lista)"),
    ("8", "Apresentar análise"),
    ("0", "Encerrar"),
)

CAMPOS_PESQUISA = (("titulo", "Título"), ("categoria", "Categoria"), ("local", "Local de atendimento"),
                   ("regiao", "Região"), ("descricao", "Descrição"))
CRITERIOS_ORDEM = (("id", "Identificador"), ("titulo", "Título"), ("categoria", "Categoria (e título)"))
ALGORITMOS_ORDEM = (("merge", "Merge Sort – O(n log n)"), ("insertion", "Insertion Sort – O(n²)"))

LIMITE_TEXTO = 200
MSG_VAZIA = "A lista está vazia: nenhum serviço cadastrado."


class Encerrar(Exception):
    pass


class Menu:
    def __init__(self, lista=None, entrada=input, saida=print):
        self.lista = lista if lista is not None else ListaEncadeada()
        self._entrada = entrada
        self.saida = saida

    # ------------------------------------------------------------- leitura validada
    def ler(self, prompt):
        try:
            return self._entrada(prompt).strip()
        except EOFError:  # Ctrl+Z / Ctrl+D ou fim das entradas simuladas
            raise Encerrar

    def ler_inteiro(self, prompt, minimo=1, maximo=None, permitir_vazio=True):
        """Repete até receber um inteiro válido. Vazio cancela (retorna None)."""
        while True:
            texto = self.ler(prompt)
            if texto == "" and permitir_vazio:
                return None
            try:
                valor = int(texto)
            except ValueError:
                self.saida(f"Entrada inválida: '{texto}' não é um número inteiro.")
                continue
            if valor < minimo or (maximo is not None and valor > maximo):
                faixa = f"entre {minimo} e {maximo}" if maximo is not None else f"maior ou igual a {minimo}"
                self.saida(f"Valor fora do intervalo: informe um número {faixa}.")
                continue
            return valor

    def ler_texto(self, prompt, obrigatorio=True):
        while True:
            texto = self.ler(prompt)
            if texto == "" and not obrigatorio:
                return None
            if texto == "":
                self.saida("Campo obrigatório: digite um valor.")
            elif len(texto) > LIMITE_TEXTO:
                self.saida(f"Texto muito longo: use no máximo {LIMITE_TEXTO} caracteres.")
            else:
                return texto

    def escolher(self, titulo, opcoes, obrigatorio=True):
        """Mostra opções numeradas e devolve o valor escolhido (None se vazio e opcional)."""
        self.saida(titulo)
        for i, op in enumerate(opcoes, 1):
            rotulo = op[1] if isinstance(op, tuple) else op
            self.saida(f"  {i} - {rotulo}")
        n = self.ler_inteiro("Opção: ", 1, len(opcoes), permitir_vazio=not obrigatorio)
        if n is None:
            return None
        op = opcoes[n - 1]
        return op[0] if isinstance(op, tuple) else op

    def confirmar(self, prompt):
        while True:
            r = self.ler(prompt + " (s/n): ").lower()
            if r in ("s", "sim"):
                return True
            if r in ("n", "nao", "não"):
                return False
            self.saida("Responda com 's' ou 'n'.")

    # ------------------------------------------------------------- operações
    def cadastrar(self):
        while True:
            id_novo = self.ler_inteiro("ID do serviço (inteiro positivo, Enter cancela): ")
            if id_novo is None:
                self.saida("Cadastro cancelado.")
                return
            if self.lista.buscar_por_id(id_novo) is None:
                break
            self.saida(f"ID duplicado: já existe um serviço com o ID {id_novo}. Informe outro.")
        titulo = self.ler_texto("Título: ")
        categoria = self.escolher("Categoria:", CATEGORIAS)
        descricao = self.ler_texto("Descrição / orientação: ")
        requisitos = self.ler_texto("Requisitos e documentos: ")
        local = self.ler_texto("Local de atendimento: ")
        regiao = self.escolher("Região:", REGIOES)
        try:
            self.lista.inserir(Servico(id_novo, titulo, categoria, descricao, requisitos, local, regiao))
        except IdDuplicadoError as e:
            self.saida(f"Erro: {e}.")
            return
        self.saida(f"Serviço {id_novo} cadastrado com sucesso. Total de registros: {len(self.lista)}.")

    def _pedir_existente(self, acao):
        if self.lista.esta_vazia():
            self.saida(MSG_VAZIA)
            return None
        id_busca = self.ler_inteiro(f"ID do serviço a {acao} (Enter cancela): ")
        if id_busca is None:
            self.saida("Operação cancelada.")
            return None
        servico = self.lista.buscar_por_id(id_busca)
        if servico is None:
            self.saida(f"Nenhum serviço encontrado com o ID {id_busca}.")
        return servico

    def consultar(self):
        servico = self._pedir_existente("consultar")
        if servico is not None:
            self.saida(servico.detalhes())

    def atualizar(self):
        servico = self._pedir_existente("atualizar")
        if servico is None:
            return
        self.saida(servico.detalhes())
        self.saida("Digite o novo valor ou pressione Enter para manter o atual.")
        novos = {}
        for campo, rotulo in (("titulo", "Título"), ("descricao", "Descrição"),
                              ("requisitos", "Requisitos"), ("local", "Local de atendimento")):
            valor = self.ler_texto(f"{rotulo} [{getattr(servico, campo)}]: ", obrigatorio=False)
            if valor is not None:
                novos[campo] = valor
        categoria = self.escolher(f"Categoria [{servico.categoria}] (Enter mantém):", CATEGORIAS, obrigatorio=False)
        if categoria is not None:
            novos["categoria"] = categoria
        regiao = self.escolher(f"Região [{servico.regiao}] (Enter mantém):", REGIOES, obrigatorio=False)
        if regiao is not None:
            novos["regiao"] = regiao
        if not novos:
            self.saida("Nenhuma alteração realizada.")
            return
        self.lista.atualizar(servico.id, **novos)
        self.saida(f"Serviço {servico.id} atualizado: {', '.join(novos)}.")

    def excluir(self):
        servico = self._pedir_existente("excluir")
        if servico is None:
            return
        self.saida(servico.resumo())
        if not self.confirmar("Confirma a exclusão"):
            self.saida("Exclusão cancelada.")
            return
        self.lista.remover(servico.id)
        self.saida(f"Serviço {servico.id} excluído. Total de registros: {len(self.lista)}.")

    def pesquisar(self):
        if self.lista.esta_vazia():
            self.saida(MSG_VAZIA)
            return
        campo = self.escolher("Pesquisar por:", CAMPOS_PESQUISA)
        termo = self.ler_texto("Termo de busca (aceita parte do texto): ")
        resultados = self.lista.pesquisar(campo, termo)
        if not resultados:
            self.saida(f"Nenhum serviço encontrado para '{termo}'.")
            return
        self.saida(f"{len(resultados)} serviço(s) encontrado(s):")
        for s in resultados:
            self.saida("  " + s.resumo())

    def ordenar(self):
        if self.lista.esta_vazia():
            self.saida(MSG_VAZIA)
            return
        criterio = self.escolher("Ordenar por:", CRITERIOS_ORDEM)
        decrescente = self.escolher("Sentido:", (("c", "Crescente"), ("d", "Decrescente"))) == "d"
        algoritmo = self.escolher("Algoritmo:", ALGORITMOS_ORDEM)
        self.lista.ordenar(criterio, algoritmo, decrescente)
        self.saida(f"Lista reorganizada com {dict(ALGORITMOS_ORDEM)[algoritmo].split(' –')[0]}:")
        self.listar()

    def listar(self):
        if self.lista.esta_vazia():
            self.saida(MSG_VAZIA)
            return
        for s in self.lista.percorrer():
            self.saida("  " + s.resumo())
        self.saida(f"Encadeamento: {self.lista.representacao()}")
        self.saida(f"Total de registros: {len(self.lista)}.")

    def analisar(self):
        self.saida(formatar_analise(gerar_analise(self.lista)))

    # ------------------------------------------------------------- laço principal
    def executar(self):
        acoes = {"1": self.cadastrar, "2": self.consultar, "3": self.atualizar, "4": self.excluir,
                 "5": self.pesquisar, "6": self.ordenar, "7": self.listar, "8": self.analisar}
        self.saida("=" * 52)
        self.saida(" CITIZEN ASSIST AI – Catálogo de serviços ao cidadão")
        self.saida("=" * 52)
        try:
            while True:
                self.saida("")
                for codigo, texto in OPCOES:
                    self.saida(f" {codigo} - {texto}")
                opcao = self.ler("Escolha uma opção: ")
                if opcao == "0":
                    break
                if opcao not in acoes:
                    self.saida(f"Opção inexistente: '{opcao}'. Escolha um número de 0 a 8.")
                    continue
                self.saida("")
                acoes[opcao]()
        except Encerrar:
            self.saida("\nEntrada encerrada.")
        self.saida("Sistema encerrado.")
