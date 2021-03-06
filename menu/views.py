from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import MenuForm
from .models import Menu, Item


def menu_list(request):
    menus = Menu.objects.all().prefetch_related('items').exclude(
        expiration_day__lt=timezone.now()).order_by('expiration_day')
    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': menus})


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.select_related('chef').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            form.save_m2m()
            messages.success(request, 'Menu created successfully.')
            return redirect('menu:menu_detail', pk=menu.pk)
        else:
            messages.error(request, 'Invalid menu. Please correct it and try again.')
            return render(request, 'menu/menu_new.html', {'form': form})
    form = MenuForm()
    return render(request, 'menu/menu_new.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            form.save_m2m()
            messages.success(request, 'Menu edited successfully')
            return redirect('menu:menu_detail', pk=menu.pk)
        else:
            messages.error(request, 'Invalid changes. Please correct them and try again.')
            return render(request, 'menu/change_menu.html', {'form': form})
    form = MenuForm(instance=menu)
    return render(request, 'menu/change_menu.html', {'form': form})
