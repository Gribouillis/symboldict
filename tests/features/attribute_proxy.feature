Feature: Attribute proxy in SymbolDict

Scenario Outline: Successful symbol access in symboldict installs attribute proxy
    Given non empty symboldict having existing symbol path
    When the path is accessed through symboldict <method>
    Then the symboldict instance has given key and value in its dict
    
    Examples: Vertical
    | method | attribute | getvalue | hasvalue |

    
Scenario: Setting item in symboldict deletes attribute proxy
    Given non empty symboldict with existing attribute proxy
    When this key is reset to symbol
    Then attribute proxy is deleted from symboldict

    
Scenario Outline: Updating symboldict deletes corresponding attribute proxies
    Given non empty symboldict with several attribute proxies
    When this symboldict is updated from <what>
    Then corresponding attribute proxies are deleted from symboldict
    
    Examples: Vertical
    | what | dict | sequence | kwargs |

    
Scenario: Deleting item in symboldict deletes attribute proxy
    Given non empty symboldict with existing attribute proxy    
    When this key is deleted from symboldict
    Then attribute proxy is deleted from symboldict

    
Scenario: Clearing symboldict deletes attribute proxies
    Given non empty symboldict with several attribute proxies
    When this symboldict is cleared
    Then all attribute proxies are deleted from symboldict

