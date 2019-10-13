from django.shortcuts import render
from .forms import NewCargoForm
from .models import Cargo, Cell


# Create your views here.
def index(request):
    return render(request, 'controller/index.html')


def new_cargo(request):
    if request.method == "POST":
        success = True
        data = request.POST

        # Create Algo to add new Cargo
        print(data)
        new_cargo_obj = Cargo()
        new_cargo_obj.cell = Cell.objects.get(pk=data['cell'])
        new_cargo_obj.date_added = data['date_added']
        new_cargo_obj.date_dated = data['date_dated']
        new_cargo_obj.title = data['title']
        new_cargo_obj.description = data['description']
        new_cargo_obj.height = data['height']
        new_cargo_obj.width = data['width']
        new_cargo_obj.length = data['length']
        new_cargo_obj.save()

        # Create Algo to add new Cargo

        if success:
            form = NewCargoForm()
            return render(request, 'new_cargo/new_cargo.html', {'form': form.as_table()})
        else:
            form = NewCargoForm()
            # Create error message !!!!!
            return render(request, 'new_cargo/new_cargo.html', {'form': form.as_table()})
    else:
        form = NewCargoForm()
        return render(request, 'new_cargo/new_cargo.html', {'form': form.as_table()})


def ret_cargo(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'ret_cargo/ret_cargo.html')


# def preview_cargos(request):
#     print('Hi')
#     if request.method == "GET":
#         success = True
#         data = request.GET
#
#         result = Cargo.objects.get(title__contains=data['title'])
#         print(result)
#         if success:
#             return render(request, 'preview_cargos/preview_cargos.html', {'cargo_list': result})
#         else:
#             return render(request, 'preview_cargos/preview_cargos.html')
#     else:
#         return render(request, 'preview_cargos/preview_cargos.html')
