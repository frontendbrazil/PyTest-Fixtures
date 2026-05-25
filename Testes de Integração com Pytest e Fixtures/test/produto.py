import sqlite3
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / 'teste.sqlite'
LOGS_DB_FILE = BASE_DIR / 'log.sqlite'


def criar_banco_em_memoria(schema_sql: str):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    return conn


@pytest.fixture(scope='function')
def conn_produtos():
    schema = """
        CREATE TABLE produtos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        );
    """
    conn = criar_banco_em_memoria(schema)
    yield conn
    conn.close()


@pytest.fixture(scope='function')
def conn_logs():
    schema = """
        CREATE TABLE logs (
            id INTEGER PRIMARY KEY,
            mensagem TEXT NOT NULL
        );
    """
    conn = criar_banco_em_memoria(schema)
    yield conn
    conn.close()


def inserir_produto(conn, nome: str, preco: float):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
        (nome, preco),
    )
    conn.commit()
    return cursor.lastrowid


def buscar_produto_por_nome(conn, nome: str):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nome, preco FROM produtos WHERE nome = ?",
        (nome,),
    )
    return cursor.fetchone()


def contar_produtos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    return cursor.fetchone()[0]


def registrar_log(conn, mensagem: str):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (mensagem) VALUES (?)",
        (mensagem,),
    )
    conn.commit()


def listar_logs(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT mensagem FROM logs ORDER BY id")
    return cursor.fetchall()


def test_inserir_produto(conn_produtos):
    inserir_produto(conn_produtos, "Ford GT 40 mk IV", 35000.0)

    produto = buscar_produto_por_nome(conn_produtos, "Ford GT 40 mk IV")

    assert produto == ("Ford GT 40 mk IV", 35000.0)


def test_retorna_produto_inserido(conn_produtos):
    inserir_produto(conn_produtos, "Ford GT 40 mk IV", 35000.0)

    produto = buscar_produto_por_nome(conn_produtos, "Ford GT 40 mk IV")

    assert produto == ("Ford GT 40 mk IV", 35000.0)


def test_banco_produtos_vazio(conn_produtos):
    total = contar_produtos(conn_produtos)

    assert total == 0


def test_registrar_log(conn_logs):
    registrar_log(conn_logs, "Produto criado")

    logs = listar_logs(conn_logs)

    assert logs == [("Produto criado",)]


def test_logs_compartilhados(conn_logs):
    registrar_log(conn_logs, "Log 1")
    registrar_log(conn_logs, "Log 2")

    logs = listar_logs(conn_logs)

    assert logs == [("Log 1",), ("Log 2",)]
