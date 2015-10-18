#!/usr/bin/python
from ansible  import inventory
def get_list(pattern="all"):
    h = inventory.Inventory()   
    return h.list_hosts(pattern = pattern)

