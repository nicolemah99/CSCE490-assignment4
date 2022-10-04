from django.shortcuts import render
from . import util
import markdown
import random


def index(request):
    links = {}
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {"entries": entries})

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def entry(request,title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {"title": title, "message":"This page does not exist for "})
    else:
        return render(request, "encyclopedia/entry.html",{"content": html_content, "title": title})

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html",{"title":entry_search, "content": html_content})
        else:
            allEntries = util.list_entries()
            search_results =[]
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    search_results.append(entry)
            return render(request, "encyclopedia/search.html",{"results": search_results})

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']

        title_exists = util.get_entry(title)

        if title_exists is not None:
            return render(request, "encyclopedia/error.html", {"message": "Page with that title already exists"})
        else:
            util.save_entry(title,content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {"title":title, "content": html_content})

def edit(request):
    if request.method == "POST":
        title = request.POST['curr_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{"title": title, "content":content})


    return(request)

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        updated_content = request.POST['text']
        util.save_entry(title,updated_content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {"title":title, "content": html_content})

def rand(request):
    all_entries = util.list_entries()
    rand_entry = random.choice(all_entries)
    html_content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {"title": rand_entry, "content": html_content})