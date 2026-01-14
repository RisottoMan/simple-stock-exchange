import pytest
from server import Server

@pytest.fixture
def server():
    return Server()

def test_empty_command(server):
    assert server.handle("") == "EMPTY COMMAND"
    assert server.handle("   ") == "EMPTY COMMAND"

def test_unknown_command(server):
    assert server.handle("SOMETHING") == "UNKNOWN COMMAND"
    assert server.handle("123") == "UNKNOWN COMMAND"
    assert server.handle("VIEW ORDER") == "UNKNOWN COMMAND"

def test_different_case(server):
    assert server.handle("buy snap lmt $30 100") == server.handle("BUY SNAP LMT $30 100")