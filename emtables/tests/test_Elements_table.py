from emtables.tables import ElementsTable

def test_iron() : 
    symbol = "Fe"
    atomic_mass = 55.8452
    density = 7.874
    number = 26
    
    t = ElementsTable(elements = [26])
    t.generate_table()
    
    assert t.table[number]["symbol"] == symbol
    assert t.table[number]["atomic_mass"] == atomic_mass
    assert t.table[number]["density"] == density
    
def test_gold () : 
    symbol = "Au"
    atomic_mass = 196.9665695
    density = 19.3
    number = 79
    
    t = ElementsTable(elements = [79])
    t.generate_table(symbols = True)
    
    assert t.table[symbol]["number"] == number
    assert t.table[symbol]["atomic_mass"] == atomic_mass
    assert t.table[symbol]["density"] == density