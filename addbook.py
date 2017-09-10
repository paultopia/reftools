from pyzotero import zotero
from freecite import fetch_books
import os
zot = zotero.Zotero(os.environ["ZOTEROACCOUNT"], "user", os.environ["ZOTEROKEY"])
template = zot.item_template('book')

instring = input("enter book cite: ")

bookdict = fetch_books([instring])[0]

for index, item in enumerate(bookdict["authors"]):
    author = item.split()
    # dropping middle initials and such, don't care.
    template['creators'][index]['firstName'] = author[0]
    template['creators'][index]['lastName'] = author[-1]

template["title"] = bookdict["title"]
template["publisher"] = bookdict["publisher"]
template["date"] = bookdict["year"]

zot.create_items([template])
