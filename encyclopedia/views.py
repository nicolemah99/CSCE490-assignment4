from django.shortcuts import redirect, render
from . import util
import markdown
import random
from django.contrib import messages


def index(request):
    links = {}
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {"entries": entries})

def convert_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def page(request,title):
    html_content = convert_to_html(title)
    if html_content == None:
        messages.error(request, f"This page does not exist.")
        return redirect("error")
    else:
        return render(request, "encyclopedia/page.html",{"content": html_content, "title": title})

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/page.html",{"title":entry_search, "content": html_content})
        else:
            all_entries = util.list_entries()
            search_results =[]
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    search_results.append(entry)
            return render(request, "encyclopedia/search.html",{"results": search_results, "title":entry_search})

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']

        title_exists = util.get_entry(title)

        if title_exists is not None:
            messages.error(request, f"Page with that title already exists.")
            return redirect("error")
        else:
            util.save_entry(title,content)
            html_content = convert_to_html(title)
            return redirect("entry", {"title":title})

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
        html_content = convert_to_html(title)
        return render(request, "encyclopedia/page.html", {"title":title, "content": html_content})

def random_page(request):
    all_entries = util.list_entries()
    rand_entry = random.choice(all_entries)
    html_content = convert_to_html(rand_entry)
    return render(request, "encyclopedia/page.html", {"title": rand_entry, "content": html_content})

def error(request):
    return render(request, 'encyclopedia/error.html')