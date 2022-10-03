from django.shortcuts import render

from . import util


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

