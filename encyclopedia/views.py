from django.shortcuts import render
from . import util
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    md_entry = util.get_entry(name)

    return render(request, "encyclopedia/entry.html", {
        "name": name,
        "entry": markdown(md_entry),
    })

