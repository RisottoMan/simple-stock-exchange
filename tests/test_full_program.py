from server import Server


def test_full_program():
    server = Server()

    #1. Acton: BUY SNAP LMT $30 100
    result = server.handle("BUY SNAP LMT $30 100")
    assert result == "You have placed a limit buy order for 100 SNAP shares at $30.00 each."

    #2. Action: BUY FB MKT 20
    result = server.handle("BUY FB MKT 20")
    assert result == "You have placed a market order for 20 FB shares."

    #3. Action: SELL FB LMT $20.00 20
    result = server.handle("SELL FB LMT $20.00 20")
    assert result == "You have placed a limit sell order for 20 FB shares at $20.00 each."

    #4. Action: SELL SNAP LMT $30.00 20
    result = server.handle("SELL SNAP LMT $30.00 20")
    assert result == "You have placed a limit sell order for 20 SNAP shares at $30.00 each."

    #5. Action: SELL SNAP LMT $31.00 10
    result = server.handle("SELL SNAP LMT $31.00 10")
    assert result == "You have placed a limit sell order for 10 SNAP shares at $31.00 each."

    #6. Action: VIEW ORDERS
    result = server.handle("VIEW ORDERS")
    result = result.split("\n")
    assert result[0] == "1. SNAP LMT BUY $30.00 0/100 PENDING"
    assert result[1] == "2. FB MKT BUY 20/20 FILLED"
    assert result[2] == "3. FB LMT SELL $20.00 20/20 FILLED"
    assert result[3] == "4. SNAP LMT SELL $30.00 10/20 PARTIAL"
    assert result[4] == "5. SNAP LMT SELL $31.00 0/10 PENDING"

    #7. Action: QUOTE SNAP - todo
    result = server.handle("QUOTE SNAP")
    assert result == "SNAP BID: $30.00 ASK: $31.00 LAST: $30.00"