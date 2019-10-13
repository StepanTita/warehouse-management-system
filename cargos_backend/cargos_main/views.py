from django.shortcuts import render
from .forms import NewCargoForm


# Create your views here.
def index(request):
    return render(request, 'controller/index.html')


def new_cargo(request):
    if request.method == "POST":
        pass
    else:
        form = NewCargoForm()
        return render(request, 'new_cargo/new_cargo.html', {'form': form.as_table()})


def ret_cargo(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'ret_cargo/ret_cargo.html')


def preview_cargos(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'preview_cargos/preview_cargos.html')
