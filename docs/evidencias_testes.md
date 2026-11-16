# Evidências de testes

Cada caso executa o menu real com entradas simuladas;
a coluna *Observado* é a linha impressa pelo sistema.

* Casos pelo menu: **24/24 aprovados**
* Testes automatizados (`python -m unittest discover -s tests`): **42/42 aprovados**

| Código | Tipo | Caso | Entradas | Esperado | Observado | Resultado |
|---|---|---|---|---|---|---|
| CT01 | Normal | Cadastrar serviço com dados válidos | `1 ↵ 601 ↵ Coleta seletiva ↵ 5 ↵ Recolhimento de recicláveis ↵ Separar o material ↵ Central 156 ↵ 3` | Serviço cadastrado e total passa de 20 para 21 | Serviço 601 cadastrado com sucesso. Total de registros: 21. | ✅ OK |
| CT02 | Inválido | Cadastrar com ID já existente (301) | `1 ↵ 301 ↵ (vazio)` | Mensagem de ID duplicado e novo pedido de ID | ID duplicado: já existe um serviço com o ID 301. Informe outro. | ✅ OK |
| CT03 | Inválido | Digitar texto no campo de ID | `1 ↵ abc ↵ (vazio)` | Mensagem de entrada inválida | Entrada inválida: 'abc' não é um número inteiro. | ✅ OK |
| CT04 | Inválido | Digitar ID negativo | `1 ↵ -3 ↵ (vazio)` | Mensagem de valor fora do intervalo | Valor fora do intervalo: informe um número maior ou igual a 1. | ✅ OK |
| CT05 | Inválido | Deixar o título em branco | `1 ↵ 602 ↵ (vazio) ↵ Teste ↵ 1 ↵ d ↵ r ↵ l ↵ 1` | Mensagem de campo obrigatório | Campo obrigatório: digite um valor. | ✅ OK |
| CT06 | Inválido | Escolher categoria inexistente (9) | `1 ↵ 603 ↵ Teste ↵ 9 ↵ 1 ↵ d ↵ r ↵ l ↵ 1` | Mensagem de valor fora do intervalo 1–5 | Valor fora do intervalo: informe um número entre 1 e 5. | ✅ OK |
| CT07 | Inválido | Opção inexistente no menu (12) | `12` | Mensagem de opção inexistente | Opção inexistente: '12'. Escolha um número de 0 a 8. | ✅ OK |
| CT08 | Normal | Consultar ID existente (204) | `2 ↵ 204` | Exibe os detalhes do serviço 204 | Título .....: Benefício de Prestação Continuada (BPC) | ✅ OK |
| CT09 | Inexistente | Consultar ID inexistente (999) | `2 ↵ 999` | Mensagem de serviço não encontrado | Nenhum serviço encontrado com o ID 999. | ✅ OK |
| CT10 | Normal | Pesquisar categoria 'saude' sem acento | `5 ↵ 2 ↵ saude` | Encontra os 4 serviços de Saúde | 4 serviço(s) encontrado(s): | ✅ OK |
| CT11 | Inexistente | Pesquisar título 'passaporte' | `5 ↵ 1 ↵ passaporte` | Mensagem de nenhum resultado | Nenhum serviço encontrado para 'passaporte'. | ✅ OK |
| CT12 | Normal | Atualizar título do serviço 502 | `3 ↵ 502 ↵ Tapa-buraco e recapeamento ↵ (vazio) ↵ (vazio) ↵ (vazio) ↵ (vazio) ↵ (vazio)` | Título alterado; demais campos mantidos | Serviço 502 atualizado: titulo. | ✅ OK |
| CT13 | Inexistente | Atualizar ID inexistente (888) | `3 ↵ 888` | Mensagem de serviço não encontrado | Nenhum serviço encontrado com o ID 888. | ✅ OK |
| CT14 | Normal | Excluir serviço 107 (cabeça da lista) | `4 ↵ 107 ↵ s` | Serviço removido e total passa a 19 | Serviço 107 excluído. Total de registros: 19. | ✅ OK |
| CT15 | Inválido | Responder 'talvez' na confirmação de exclusão | `4 ↵ 107 ↵ talvez ↵ n` | Pede resposta s/n e cancela | Responda com 's' ou 'n'. | ✅ OK |
| CT16 | Inexistente | Excluir ID inexistente (777) | `4 ↵ 777` | Mensagem de serviço não encontrado | Nenhum serviço encontrado com o ID 777. | ✅ OK |
| CT17 | Normal | Ordenar por ID com Merge Sort | `6 ↵ 1 ↵ 1 ↵ 1` | Lista exibida de 101 a 505 | Encadeamento: cabeça → [101] → [103] → [105] → [107] → [201] → [202] → [203] → [204] → [301] → [302] → [303] → [304] → [401] → [402] → [405] → [406] → [502] → [503] → [504] → [505] → None | ✅ OK |
| CT18 | Normal | Ordenar por título com Insertion Sort | `6 ↵ 2 ↵ 1 ↵ 2` | Primeiro título em ordem alfabética: Atendimento a pessoas… | [202] Atendimento a pessoas em situação de rua (Assistência social – Centro) | ✅ OK |
| CT19 | Normal | Apresentar análise | `8` | Total de 20 serviços, 4 por categoria | Total de serviços cadastrados: 20 | ✅ OK |
| CT20 | Lista vazia | Consultar com a lista vazia | `2` | Mensagem de lista vazia | A lista está vazia: nenhum serviço cadastrado. | ✅ OK |
| CT21 | Lista vazia | Excluir com a lista vazia | `4` | Mensagem de lista vazia | A lista está vazia: nenhum serviço cadastrado. | ✅ OK |
| CT22 | Lista vazia | Ordenar com a lista vazia | `6` | Mensagem de lista vazia | A lista está vazia: nenhum serviço cadastrado. | ✅ OK |
| CT23 | Lista vazia | Apresentar análise com a lista vazia | `8` | Mensagem de que não há dados | Nenhum serviço cadastrado: não há dados para analisar. | ✅ OK |
| CT24 | Lista vazia | Cadastrar o primeiro serviço na lista vazia | `1 ↵ 1 ↵ Primeiro serviço ↵ 1 ↵ d ↵ r ↵ l ↵ 1 ↵ 7` | Lista passa a ter 1 nó (cabeça = cauda) | Encadeamento: cabeça → [1] → None | ✅ OK |
