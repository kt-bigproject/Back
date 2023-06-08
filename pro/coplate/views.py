from django.shortcuts import render


def index(req):
    print(req.user)
    return render(req, 'coplate/index.html')