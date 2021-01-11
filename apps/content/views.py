from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache


def test(request):
    var = cache.get("test")
    if not var:
        var = 123
        cache.set("test", var)
        print("Setting cache")
    else:
        print("Using cache")
    return HttpResponse("<h1>Hello World</h1>")