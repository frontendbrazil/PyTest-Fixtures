# Relatório de Testes de Integração

## Visão Geral

Este relatório descreve os testes de integração implementados no projeto e sua relação com o código atual em `test/produto.py`.

## Ambiente e Ferramentas

- **Framework de teste:** Pytest
- **Banco de dados:** SQLite em memória
- **Interpretador utilizado:** `.venv\Scripts\python.exe`
- **Arquivo de testes:** `test/produto.py`

## Componentes Cobertos

| Componente | Descrição |
| --- | --- |
| `conn_produtos` | Fixture de escopo `function` que cria um banco em memória para produtos |
| `conn_logs` | Fixture de escopo `function` que cria um banco em memória para logs |
| `criar_banco_em_memoria` | Função utilitária que inicializa o banco SQLite com o esquema fornecido |
| `inserir_produto` | Função auxiliar que insere um produto na tabela `produtos` |
| `buscar_produto_por_nome` | Função auxiliar que recupera um produto pelo nome |
| `contar_produtos` | Função auxiliar que retorna a quantidade de produtos registrados |
| `registrar_log` | Função auxiliar que registra mensagens na tabela `logs` |
| `listar_logs` | Função auxiliar que retorna todos os registros de log ordenados por `id` |

## Casos de Teste

### CT-01 — Inserção de produto

- **Objetivo:** validar que um produto pode ser inserido e recuperado corretamente.
- **Pré-condição:** fixture `conn_produtos` disponível.
- **Passos:**
  1. Inserir um produto usando `inserir_produto`.
  2. Consultar o produto usando `buscar_produto_por_nome`.
- **Resultado esperado:** o registro retornado corresponde ao produto inserido.

```python
def test_inserir_produto(conn_produtos):
    inserir_produto(conn_produtos, "Ford GT 40 mk IV", 35000.0)
    produto = buscar_produto_por_nome(conn_produtos, "Ford GT 40 mk IV")

    assert produto == ("Ford GT 40 mk IV", 35000.0)
```

### CT-02 — Consulta de produto inserido

- **Objetivo:** validar a recuperação de um produto específico a partir do banco.
- **Pré-condição:** fixture `conn_produtos` disponível.
- **Passos:**
  1. Inserir um produto usando `inserir_produto`.
  2. Consultar o produto pelo campo `nome` com `buscar_produto_por_nome`.
- **Resultado esperado:** o produto consultado deve ser exatamente o produto inserido.

```python
def test_retorna_produto_inserido(conn_produtos):
    inserir_produto(conn_produtos, "Ford GT 40 mk IV", 35000.0)
    produto = buscar_produto_por_nome(conn_produtos, "Ford GT 40 mk IV")

    assert produto == ("Ford GT 40 mk IV", 35000.0)
```

### CT-03 — Banco de produtos vazio

- **Objetivo:** garantir que o banco de produtos comece sem registros.
- **Pré-condição:** fixture `conn_produtos` disponível.
- **Passos:**
  1. Consultar a contagem de registros com `contar_produtos`.
- **Resultado esperado:** contagem igual a `0`.

```python
def test_banco_produtos_vazio(conn_produtos):
    total = contar_produtos(conn_produtos)

    assert total == 0
```

### CT-04 — Registro de log

- **Objetivo:** validar que a função de registro insere uma mensagem na tabela `logs`.
- **Pré-condição:** fixture `conn_logs` disponível.
- **Passos:**
  1. Registrar uma mensagem usando `registrar_log`.
  2. Consultar os logs com `listar_logs`.
- **Resultado esperado:** a mensagem registrada deve ser retornada corretamente.

```python
def test_registrar_log(conn_logs):
    registrar_log(conn_logs, "Produto criado")
    logs = listar_logs(conn_logs)

    assert logs == [("Produto criado",)]
```

### CT-05 — Logs compartilhados

- **Objetivo:** validar que múltiplos registros de log são preservados e recuperados na ordem esperada.
- **Pré-condição:** fixture `conn_logs` disponível.
- **Passos:**
  1. Registrar duas mensagens consecutivas usando `registrar_log`.
  2. Consultar todos os registros com `listar_logs`.
- **Resultado esperado:** as mensagens devem ser retornadas na ordem de inserção.

```python
def test_logs_compartilhados(conn_logs):
    registrar_log(conn_logs, "Log 1")
    registrar_log(conn_logs, "Log 2")
    logs = listar_logs(conn_logs)

    assert logs == [("Log 1",), ("Log 2",)]
```

## Resultados de Execução

A suíte foi executada com o comando abaixo:

```powershell
pytest -s -v test/produto.py
```

**Resultado verificado:** 5 testes executados com sucesso.

## Observações

- Os testes utilizam bancos SQLite em memória, garantindo isolamento entre testes.
- O arquivo atual de testes está centralizado em `test/produto.py`.
- O relatório agora reflete a implementação atualizada da suíte, com funções utilitárias e fixtures renomeadas.