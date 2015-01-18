Feature: other SymbolDict's features

Background:
    Given namespace

    
Scenario: Symboldict creation
    Given list of 3 pairs key value
    When symboldict is created by <method>
    Then symboldict has length 3
    And symboldict has required keys
    And all values are symbol instances
    
    Examples: Vertical
    | method | dict | sequence | kwargs |

    
Scenario: Empty symboldict creation
    Given empty symboldict
    Then sd has length 0
    And sd boolean value is False
    And sd is dict instance

    
Scenario: Symboldict fetches existing values
    Given sd pointing to stdlib symbols
    When these symbols are accessed by <method>
    Then stdlib values are properly fetched
    
    Examples: Vertical
    | method | attribute | getvalue |

    
Scenario: Symboldict reports non existing values
    Given sd pointing to non existing symbols
    Then accessing by <method> raises exception

    Examples: Vertical
    | method | attribute | getvalue |

    
Scenario: Symboldict checks existing values
    Given sd pointing to stdlib symbols
    Then hasvalue returns true for these symbols

    
Scenario: Symboldict checks non existing values
    Given sd pointing to non existing symbols
    Then hasvalue returns false for these symbols

    
Scenario: Setdefault with existing key
    Given non empty sd
    When setdefault is called on existing key
    Then existing value is returned

    
Scenario: Setdefault with non existing key
    Given example sd
    When setdefault is called on non existing key
    Then key is inserted in sd
    And value is default converted to symbol

    
Scenario: Update method works and converts to symbol
    Given non empty sd
    And list of 2 pairs key value
    When sd is updated with <method>
    Then keys are inserted in sd
    And values are converted to symbol
    
    Examples: Vertical
    | method | dict | sequence | kwargs |

    
Scenario: Getvalue w dont load rule does not import module
    Given sd pointing to Telnet
    And telnetlib forced out sys modules
    When getvalue rule dont load fails
    Then telnetlib is not in sys modules
    
    
Scenario: Getvalue w force reload rule refetches value
    Given sd pointing to Telnet with value
    And telnetlib forced out sys modules
    When getvalue rule force reload is called
    Then telnetlib is in sys modules

    
Scenario: Getvalue try load each rule does not reload
    Given sd pointing to Telnet with value
    And telnetlib forced out sys modules
    When getvalue rule try load each is called
    Then telnetlib is not in sys modules

    
Scenario: Getvalue try load each rule does load
    Given sd pointing to Telnet without value
    And telnetlib forced out sys modules
    When getvalue rule try load each is called 2
    Then telnetlib is in sys modules

    
Scenario: Getvalue try load each rule tries after failure
    Given sd pointing to bad eggs symbol in telnetlib
    When getvalue rule try load each fails 
    And telnetlib is removed from sys modules
    And getvalue rule try load each fails
    Then telnetlib is in sys modules

    
Scenario: Getvalue try load once rule does not reload
    Given sd pointing to Telnet with value
    And telnetlib forced out sys modules
    When getvalue rule try load once is called
    Then telnetlib is not in sys modules
    
    
Scenario: Getvalue try load once rule tries only once
    Given sd pointing to bad eggs symbol in telnetlib
    When getvalue rule try load once fails 
    And telnetlib is removed from sys modules
    And getvalue rule try load once fails
    Then telnetlib is not in sys modules

Scenario: Getvalue wo rule does not reload
    Given sd pointing to Telnet with value
    And telnetlib forced out sys modules
    When getvalue wo rule is called
    Then telnetlib is not in sys modules
    
    
Scenario: Getvalue wo rule tries only once
    Given sd pointing to bad eggs symbol in telnetlib
    When getvalue wo rule fails 
    And telnetlib is removed from sys modules
    And getvalue wo rule fails
    Then telnetlib is not in sys modules

# hasvalue

Scenario: Hasvalue w dont load rule does not import module
    Given sd pointing to Telnet
    And telnetlib forced out sys modules
    When hasvalue rule dont load is called
    Then telnetlib is not in sys modules
    
    
Scenario: Hasvalue w force reload rule refetches value
    Given sd pointing to Telnet with value
    And telnetlib forced out sys modules
    When hasvalue rule force reload is called
    Then telnetlib is in sys modules

    
Scenario: Hasvalue try load each rule does not reload
    Given sd pointing to Telnet with value
    And telnetlib forced out sys modules
    When hasvalue rule try load each is called
    Then telnetlib is not in sys modules

    
Scenario: Hasvalue try load each rule does load
    Given sd pointing to Telnet without value
    And telnetlib forced out sys modules
    When hasvalue rule try load each is called 2
    Then telnetlib is in sys modules

    
Scenario: Hasvalue try load each rule tries after failure
    Given sd pointing to bad eggs symbol in telnetlib
    When hasvalue rule try load each is called 3 
    And telnetlib is removed from sys modules
    And hasvalue rule try load each is called 3
    Then telnetlib is in sys modules

    
Scenario: Hasvalue try load once rule does not reload
    Given sd pointing to Telnet with value
    And telnetlib forced out sys modules
    When hasvalue rule try load once is called
    Then telnetlib is not in sys modules
    
    
Scenario: Hasvalue try load once rule tries only once
    Given sd pointing to bad eggs symbol in telnetlib
    When hasvalue rule try load once is called 3 
    And telnetlib is removed from sys modules
    And hasvalue rule try load once is called 3
    Then telnetlib is not in sys modules

    
Scenario: Hasvalue wo rule does not reload
    Given sd pointing to Telnet with value
    And telnetlib forced out sys modules
    When hasvalue wo rule is called
    Then telnetlib is not in sys modules
    
    
Scenario: Hasvalue wo rule tries only once
    Given sd pointing to bad eggs symbol in telnetlib
    When hasvalue wo rule is called 3
    And telnetlib is removed from sys modules
    And hasvalue wo rule is called 3
    Then telnetlib is not in sys modules

