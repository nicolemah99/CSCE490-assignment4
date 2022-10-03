from django.shortcuts import render
from . import util
import markdown


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
    content = convert_md_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {"title": title, "message":"This page does not exist for "})
    else:
        return render(request, "encyclopedia/entry.html",{"content": content, "title": title})

def search(request):
    if request.method == "POST":
        search_entry = request.POST['q']
        content = convert_md_to_html(search_entry)
        entries = util.list_entries()
        for entry in entries:
            if search_entry.lower() == entry.lower():
                return render(request, "encyclopedia/entry.html",{"content": content, "title": search_entry})
        else:
            search_results = []
            for entry in entries:
                if search_entry.lower() in entry.lower():
                    search_results.append(entry)

            return render(request, "encyclopedia/search.html", {"results": search_results})

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        title = request.POST['title']
        content = request.POST['title']

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
    return