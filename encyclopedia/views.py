import random
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        raise Http404("Entry not found.")
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": entry_content
    })

def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm()
    })

def edit(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        raise Http404("Entry not found.")
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": NewPageForm(initial={"content": entry_content})
    })

def random_entry(request):
    entries = util.list_entries()
    if not entries:
        raise Http404("No entries found.")
    title = random.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))