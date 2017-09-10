from requests import post
from xml.etree.ElementTree import fromstring
from copy import deepcopy

endpoint = "http://freecite.library.brown.edu/citations/create"

headers = {"Accept": "text/xml"}

def construct_dict_helper(indict, citetree, fieldlist):
    newdict = deepcopy(indict)
    for entry in fieldlist:
        newdict[entry] = citetree.find(entry).text
    return newdict

def article_tree_to_dict(citetree):
    outdict = {}
    authorsnode = citetree.find("authors")
    outdict["authors"] = [au.text for au in authorsnode.findall("author")]
    return construct_dict_helper(outdict, citetree, ["title", "journal", "volume", "pages", "year"])

def fetch_articles(cites):
    data = [("citation[]", x) for x in cites]
    response = post(endpoint, headers=headers, data=data)
    tree = fromstring(response.text)
    citations = tree.findall("citation")
    return [article_tree_to_dict(x) for x in citations]

def book_tree_to_dict(citetree):
    outdict = {}
    authorsnode = citetree.find("authors")
    outdict["authors"] = [au.text for au in authorsnode.findall("author")]
    return construct_dict_helper(outdict, citetree, ["title", "publisher", "year"])

def fetch_books(cites):
    data = [("citation[]", x) for x in cites]
    response = post(endpoint, headers=headers, data=data)
    tree = fromstring(response.text)
    citations = tree.findall("citation")
    return [book_tree_to_dict(x) for x in citations]

