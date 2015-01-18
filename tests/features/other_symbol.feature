Feature: other Symbol's features

Background:
    Given namespace

Scenario: Create symbol from arglist
    Given argument list of several words
    When symbol is created from list
    Then result is a symbol instance
    And symbol str is dot join of list
    
Scenario: Create empty symbol
    Given symbol ctor return value
    Then value is symbol instance
    And symbol str is empty string
    
Scenario: Symbol constructor converts args to str
    Given argument list of various types
    When symbol is created from list
    Then symbol str is dot join of args converted to str
    
Scenario: Symbol attribute access returns new symbol
    Given non trivial symbol
    When attribute ham and eggs are taken
    Then result is symbol instance
    And symbol str is appended said attributes
    
Scenario: Attribute setting is forbidden
    Given non trivial symbol
    Then setting attribute ham raises typeerror
    And setting hidden attribute raises typeerror

Scenario: Symbols with same path are equal
    Given 2 symbols with same path
    Then these 2 symbols are equal
    
Scenario: Symbols with different path are different
    Given 2 symbols with different path
    Then these 2 symbols are different
    
Scenario: Symbols are richly ordered
    Given non trivial symbol
    And list of various objects among which symbol
    Then each object has one comparison true among lt eq gt

Scenario: Symbols are hashable
    Given 2 non trivial symbol
    When set is created containing these symbols
    Then both symbols belong to set
    
Scenario: Getvalue method retrieves value
    Given symbol w path to Telnet
    When getvalue method is called
    Then result is stdlib Telnet object
    
Scenario: Getvalue method raises on non existing path
    Given symbol w path to spam in telnetlib
    Then calling getvalue raises exception
    
Scenario: Hasvalue method succeeds if value exists
    Given symbol w path to Telnet
    Then hasvalue method returns True
    
Scenario: Hasvalue method succeeds if value does not exist
    Given symbol w path to spam in telnetlib
    Then hasvalue method returns False

Scenario: Call method returns symbolcontrol instance
    Given example symbol
    When call method is called
    Then return value is a symbolcontrol instance
    And symbolcontrol symbol method returns example symbol
    And symbolcontrol path method returns str of symbol

Scenario: getvalue w rule dont load doesnt load
    Given symbol w path to Telnet
    And telnetlib forced out of sys modules
    When getvalue fails w rule dont load
    Then telnetlib is not in sys modules
    
Scenario: hasvalue w rule dont load doesnt load
    Given symbol w path to Telnet
    And telnetlib forced out of sys modules
    When hasvalue called w rule dont load returns false
    Then telnetlib is not in sys modules

Scenario: getvalue w rule force reload does reload
    Given symbol w path to Telnet and value
    And telnetlib forced out of sys modules
    When getvalue is called with rule force reload
    Then telnetlib is in sys modules

Scenario: hasvalue w rule force reload does reload
    Given symbol w path to Telnet and value
    And telnetlib forced out of sys modules
    When hasvalue called with rule force reload returns true
    Then telnetlib is in sys modules
    
Scenario: getvalue w rule each does try twice
    Given symbol w path to spam in telnetlib
    When calling getvalue w rule try load each fails
    And telnetlib is removed from sys modules
    And calling getvalue w rule try load each fails
    Then telnetlib is in sys modules

Scenario: hasvalue w rule each does try twice
    Given symbol w path to spam in telnetlib
    When calling hasvalue w rule try load each returns false
    And telnetlib is removed from sys modules
    And calling hasvalue w rule try load each returns false
    Then telnetlib is in sys modules

Scenario: getvalue with rule each doesnt reload
    Given symbol w path to Telnet and value
    And telnetlib forced out of sys modules
    When getvalue is called with rule try load each
    Then telnetlib is not in sys modules
    
Scenario: hasvalue with rule each doesnt reload
    Given symbol w path to Telnet and value
    And telnetlib forced out of sys modules
    When hasvalue called with rule try load each returns true
    Then telnetlib is not in sys modules

Scenario: getvalue w rule once doesnt try twice
    Given symbol w path to spam in telnetlib
    When calling getvalue w rule once fails
    And telnetlib is removed from sys modules
    And calling getvalue w rule once fails
    Then telnetlib is not in sys modules
    
Scenario: hasvalue w rule once doesnt try twice
    Given symbol w path to spam in telnetlib
    When calling hasvalue w rule once returns false
    And telnetlib is removed from sys modules
    And calling hasvalue w rule once returns false
    Then telnetlib is not in sys modules
    
Scenario: getvalue with rule once doesnt reload
    Given symbol w path to Telnet and value
    And telnetlib forced out of sys modules
    When getvalue is called with rule once
    Then telnetlib is not in sys modules
    
Scenario: hasvalue with rule once doesnt reload
    Given symbol w path to Telnet and value
    And telnetlib forced out of sys modules
    When hasvalue called with rule once returns true
    Then telnetlib is not in sys modules

Scenario: getvalue wo rule doesnt try twice
    Given symbol w path to spam in telnetlib
    When calling getvalue wo rule fails
    And telnetlib is removed from sys modules
    And calling getvalue wo rule fails
    Then telnetlib is not in sys modules
    
Scenario: hasvalue wo rule doesnt try twice
    Given symbol w path to spam in telnetlib
    When calling hasvalue wo rule returns false
    And telnetlib is removed from sys modules
    And calling hasvalue wo rule returns false
    Then telnetlib is not in sys modules
    
Scenario: getvalue wo rule doesnt reload
    Given symbol w path to Telnet and value
    And telnetlib forced out of sys modules
    When getvalue is called wo rule
    Then telnetlib is not in sys modules
    
Scenario: hasvalue wo rule doesnt reload
    Given symbol w path to Telnet and value
    And telnetlib forced out of sys modules
    When hasvalue called wo rule returns true
    Then telnetlib is not in sys modules
