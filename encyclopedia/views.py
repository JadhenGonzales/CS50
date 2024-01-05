from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
from markdown2 import markdown
from random import choice


def index(request):
    entries = util.list_entries()

    if request.method == "POST":
        # If query is in entries, redirect to wiki page
        query = request.POST["q"]
        if query in entries:
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'name': query}))

        else:
            # Show list of all entries where query is a substring of
            results = []
            for entry in entries:
                if query.lower() in entry.lower():
                    results.append(entry)

            return render(request, "encyclopedia/index.html", {
                "entries": results
            })
    else:
        #If method is GET, show list of all entries
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def add(request):
    if request.method == "POST":
        form = util.EntryForm(request.POST)
        #Verify form data
        if form.is_valid():
            new_entry = form.cleaned_data
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
        
        #Add to entries and redirect
        util.save_entry(new_entry["title"], new_entry["description"])
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'name': new_entry["title"]}))

    else:
        return render(request, "encyclopedia/add.html", {
            "form": util.EntryForm()
        })


def edit(request, name):
    if request.method == "POST":
        form = util.EntryForm(request.POST)
        #Verify form data
        if form.is_valid():
            new_entry = form.cleaned_data
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
        
        #Add to entries and redirect
        util.save_entry(new_entry["title"], new_entry["description"])
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'name': new_entry["title"]}))

    else:
        data = {
            "title": name,
            "description": util.get_entry(name)
        }

        return render(request, "encyclopedia/add.html", {
            "form": util.EntryForm(data)
        })


def entry(request, name):
    #Show page of entry
    md_entry = util.get_entry(name)
    return render(request, "encyclopedia/entry.html", {
        "name": name,
        "entry": markdown(md_entry),
    })


def random(request):
    entries = util.list_entries()
    name = choice(entries)

    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'name': name}))

