from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(req):
    return render(req, 'index.html')

def register(req):
    results = User.objects.register(req.POST)
    if isinstance(results, User):
        req.session['user_id'] = results.id
        messages.add_message(req, messages.SUCCESS, 'Welcome to our site, {}'.format(results.username))
        return redirect('/')
    else:
        for key in results:
            messages.add_message(req, messages.ERROR, results[key])
        return redirect('/')

def login(req):
    results = User.objects.login(req.POST)
    if isinstance(results, User):
        req.session['user_id'] = results.id
        messages.add_message(req, messages.SUCCESS, 'Welcome back, {}'.format(results.username))
        return redirect('/wishlist')
    else:
        for key in results:
            messages.add_message(req, messages.ERROR, results[key])
        return redirect('/')

def wishlist(req):
    context ={
        'items': Item.objects.all(),
    }
    return render(req, 'wishlist.html', context)

def logout(req):
    req.session.clear()
    return redirect('/')

def additem(req):
    return redirect('/createitem')

def items(req):
    add_item = User.objects.get(id = req.session['user_id']).add_item.all()
    items = Item.objects.all()
    for item in add_item:
        items = items.exclude(id = item.id)
    return render(req, 'wishlist.html', {'items': items, 'add_item':add_item})

def removeitem(req, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(id=req.session['user_id'])
    item.additems.remove(user)
    return redirect('/items')

def wishitem(req, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(id=req.session['user_id'])
    item.additems.add(user)
    return redirect('/items')

def produceitem(req):
    results = Item.objects.produceitem(req.POST, req.session['user_id'])
    if isinstance(results, Item):
        messages.add_message(req, messages.SUCCESS, 'You successfully added an item')
        return redirect('/createitem')
    else:
        for key in results:
            messages.add_message(req, messages.ERROR, results[key])
    return redirect ('/createitem')

def createitem(req):
    return render(req, 'createitem.html')

def home(req):
    return redirect('/items')

def wish(req, item_id):
    item = Item.objects.get(id=item_id)
    context = {
        'item': item
    }
    return render(req, 'wish.html', context)

# Create your views here.
