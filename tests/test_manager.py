import pytest
from server import Server, Manager

@pytest.fixture
def server():
    return Server()

@pytest.fixture
def manager(server):
    return Manager(server)

def test_quote_without_arg(manager):
    assert manager.get_quote(None) == "EMPTY TICKER ARGUMENT"
    assert manager.get_quote("") == "EMPTY TICKER ARGUMENT"

def test_invalid_len_args(manager):
    assert manager.create_order("BUY", "SNAP", "LMT") == "INVALID COMMAND"
    assert manager.create_order("BUY", "SNAP", "LMT", "$30", "50", "10") == "INVALID COMMAND"

def test_invalid_operation(manager):
    assert manager.create_order("BUT", "SNAP", "LMT", "$30") == "INVALID OPERATION"
    assert manager.create_order("SMELL", "SNAP", "LMT", "$30") == "INVALID OPERATION"

def test_invalid_order_type(manager):
    assert manager.create_order("BUY", "SNAP", "GMT", "$30") == "INVALID ORDER TYPE"
    assert manager.create_order("SELL", "SNAP", "MMT", "$30") == "INVALID ORDER TYPE"

def test_invalid_args_for_limit_order(manager):
    assert manager.create_order("BUY", "SNAP", "LMT", "$30") == "INVALID NUMBER ARGUMENTS FOR ORDER TYPE"

def test_convert_price_to_float(manager):
    assert manager.create_order("BUY", "SNAP", "LMT", "$30", "50") == manager.create_order("BUY", "SNAP", "LMT", "$30.00", "50")