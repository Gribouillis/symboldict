Feature: Strict and non strict symboldict

    Scenario Outline: Check strictness of new symboldict
        Given new <how> symboldict
        Then symboldict is strict
    
        Examples: Vertical
        | how | empty | non empty |
        
    Scenario: Forbidden key setting raise TypeError in strict symboldict
        Given strict symboldict
        Then setting symboldict item with forbidden key raises TypeError
        
    Scenario: Attributes of SymbolDict types are forbidden keys in strict symboldict
        Given strict symboldict
        Then every attribute of SymbolDict type is forbidden key in symboldict   
        
    Scenario: Attributes of SymbolDict types are allowed keys in non strict symboldict
        Given non strict symboldict
        Then all attributes of SymbolDict type are allowed keys in symboldict
        
    Scenario: Setting symboldict strict raises TypeError if there is forbidden key
        Given symboldict containing forbidden key
        Then setting symboldict strict raises TypeError

    Scenario: Creating strict symboldict from dict having forbidden key raises TypeError
        Given dict containing forbidden key
        Then creating strict symboldict from dict raises TypeError
   
    Scenario: Updating strict symboldict with dict having forbidden key raises TypeError
        Given strict symboldict
        And dict containing forbidden key
        Then updating symboldict with dict raises TypeError
        
    Scenario: Creating strict symboldict from sequence having forbidden item raises TypeError
        Given sequence of items containing forbidden key
        Then creating strict symboldict from sequence raises TypeError
        
    Scenario: Updating strict symboldict from sequence having forbidden item raises TypeError
        Given strict symboldict
        And sequence of items containing forbidden key
        Then updating symboldict from sequence raises TypeError
        
