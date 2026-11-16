# Citizen Assist AI – Global Solution DSA

Sistema em **Python** de gerenciamento e consulta de serviços e orientações ao cidadão, para o desafio **Citizen Tech** (GS 2026.2).
Trabalho da disciplina **Data Structures and Algorithms (DSA)**, 2º semestre.

## Integrantes

| Nome completo | RM |
|---|---|
| Lucas Angelo | 569530 |
| Gustavo Guedes | 569779 |
| Gabriel Rodrigues | 569322 |

## Recorte e objetivo

Muitos cidadãos não sabem onde ser atendidos nem quais documentos levar para usar um serviço público. O grupo escolheu montar
**um catálogo único de serviços ao cidadão de um município**, nas cinco categorias sugeridas no enunciado (saúde, assistência social,
documentação e cidadania, educação e qualificação, serviços urbanos), com requisitos, local de atendimento e região da cidade.

O foco é a aplicação de estruturas de dados e algoritmos implementados pela equipe:
* os registros ficam em uma **lista simplesmente encadeada própria** (classes `No` e `ListaEncadeada`, com cabeça, cauda e tamanho);
* **busca sequencial** por ID e por atributo, que ignora acentos e maiúsculas;
* **Merge Sort** e **Insertion Sort** feitos à mão, que religam os próprios nós (nenhum `sorted`/`list.sort`);
* CRUD completo, análise por categoria e região, menu com validação de todas as entradas.

## Modelo dos registros

| Campo | Tipo | Validação |
|---|---|---|
| `id` | int | inteiro ≥ 1, **único** |
| `titulo` | str | obrigatório (até 200 caracteres) |
| `categoria` | str | uma das 5 categorias |
| `descricao` | str | obrigatório |
| `requisitos` | str | obrigatório |
| `local` | str | obrigatório |
| `regiao` | str | Centro, Norte, Sul, Leste ou Oeste |

A base de exemplo [`dados/servicos_exemplo.json`](dados/servicos_exemplo.json) tem 20 serviços (4 por categoria). Os textos são ilustrativos,
escritos pelo grupo; não há integração com sistemas públicos reais (o enunciado não exige).

## Lista encadeada

```
cabeca                                                   cauda
  │                                                        │
  ▼                                                        ▼
[107 | •]──▶[203 | •]──▶[301 | •]── ... ──▶[402 | •]──▶ None        tamanho = 20
 dado proximo
```

* **Inserção** no fim em O(1) graças à `cauda`; antes, uma busca sequencial recusa ID duplicado.
* **Percurso** pelo gerador `percorrer()`, que segue `proximo` até `None`.
* **Remoção** guarda o nó `anterior` e faz `anterior.proximo = atual.proximo`. Trata a remoção da cabeça, do meio, da cauda e do único nó.
* Em Python, as referências fazem o papel dos ponteiros, e o coletor de lixo libera o nó desligado.

## Complexidade (Big-O)

| Operação | Melhor | Pior | Por quê |
|---|---|---|---|
| Inserção (cadastro) | O(n) | O(n) | verificação de ID duplicado; o encadeamento no fim é O(1) |
| Busca por ID | O(1) | O(n) | sequencial; a lista encadeada não tem acesso por posição, então busca binária não se aplica |
| Pesquisa por atributo | O(n) | O(n) | percorre tudo, pois pode haver vários resultados |
| Remoção / atualização | O(1) | O(n) | custo de localizar o nó; religar ou alterar é O(1) |
| Percurso, listagem, análise | O(n) | O(n) | um percurso |
| **Merge Sort** | O(n log n) | O(n log n) | divide ao meio (ponteiros lento/rápido) e intercala; estável; pilha O(log n) |
| **Insertion Sort** | O(n) | O(n²) | lista já ordenada é anexada no fim; estável; memória O(1) |

Com 4.000 nós aleatórios, o Merge Sort levou ~7 ms e o Insertion Sort ~420 ms (Tabela 2 da documentação técnica).

## Estrutura do repositório

```
├── main.py                       # ponto de entrada (menu interativo)
├── citizen_assist/
│   ├── modelos.py                # classes Servico (registro) e No (nó)
│   ├── lista_encadeada.py        # ListaEncadeada: inserir, percorrer, buscar, atualizar, remover, ordenar
│   ├── busca.py                  # busca sequencial por ID e por atributo
│   ├── ordenacao.py              # Merge Sort e Insertion Sort sobre os nós
│   ├── analise.py                # total e distribuição por categoria e região
│   └── menu.py                   # menu e validação das entradas
├── dados/servicos_exemplo.json   # base de exemplo com 20 serviços
├── tests/                        # 42 testes automatizados (unittest)
├── docs/evidencias_testes.md     # casos de teste: entradas, esperado e observado
└── relatorio/documentacao_tecnica.pdf
```

| Entregável do enunciado | Onde está |
|---|---|
| Código-fonte com instruções de execução | `main.py`, `citizen_assist/` e a seção *Como executar* abaixo |
| Documentação técnica (recorte, registros, lista, menu) | [`relatorio/documentacao_tecnica.pdf`](relatorio/documentacao_tecnica.pdf), seções 2, 3 e 6 |
| Análise dos algoritmos com Big-O | documentação técnica, seções 4 e 5; tabela acima |
| Evidências de testes (entradas, esperado, observado) | [`docs/evidencias_testes.md`](docs/evidencias_testes.md) e documentação técnica, seção 7 |
| Demonstração prática | vídeo/apresentação do grupo usando o menu (`python main.py`); roteiro na documentação técnica, seção 8 |

## Como executar

Requer apenas **Python 3.10+**, sem bibliotecas externas.

```bash
git clone https://github.com/lucasangelo40695-dotcom/gs-dsa-citizen-assist.git
cd gs-dsa-citizen-assist
python main.py
```

* `python main.py --vazio`: começa com a lista vazia (para testar as mensagens de lista vazia).
* `python -m unittest discover -s tests -v`: roda os 42 testes automatizados.

Ao iniciar, o sistema carrega os 20 serviços de `dados/servicos_exemplo.json`. As alterações ficam na memória durante a execução.

### Menu

```
 1 - Cadastrar serviço
 2 - Consultar serviço por ID
 3 - Atualizar serviço
 4 - Excluir serviço
 5 - Pesquisar serviços
 6 - Ordenar e exibir serviços
 7 - Listar todos (percurso da lista)
 8 - Apresentar análise
 0 - Encerrar
```

Entradas tratadas: opção inexistente, texto em campo numérico, número fora do intervalo, ID duplicado, campo obrigatório vazio,
ID inexistente, pesquisa sem resultado, operações com a lista vazia, resposta inválida na confirmação e fim da entrada (Ctrl+Z/Ctrl+D).

## Testes

| Nível | Resultado |
|---|---|
| `unittest` (lista, busca, ordenação e menu) | 42/42 aprovados |
| Casos pelo menu real com entradas simuladas: normais, inexistentes, inválidos e lista vazia | 24/24 aprovados ([tabela](docs/evidencias_testes.md)) |

## Limitações e melhorias

* A busca e a checagem de ID duplicado são O(n). Um índice auxiliar (tabela hash por ID) reduziria isso para O(1) em média.
* A ordenação reorganiza a própria lista, então a ordem de cadastro não é mantida depois de ordenar.
* Os dados são ilustrativos. Uma evolução natural é integrar bases oficiais de serviços e um assistente em linguagem natural.
