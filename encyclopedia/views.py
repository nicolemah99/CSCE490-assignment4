from django.shortcuts import render
from . import util
from markdown2 import Markdown


def index(request):
    links = {}
    entries = util.list_entries()

    for entry in entries:
        links[entry] = "/wiki/"+entry
    return render(request, "encyclopedia/index.html", {"entries": entries, "links":links})

def wiki(request,title):
    contents = util.get_entry(title)
    if contents == None:
        return render(request, "encyclopedia/error.html", {"title": title})
    else:
        return render(request, "encyclopedia/wiki.html",{"contents": contents, "title": title})

def search(request):

    return render(request, "encyclopedia/search.html")
