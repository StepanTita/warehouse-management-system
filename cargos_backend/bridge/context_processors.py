from cargos_main.forms import SearchForm
from users.models import Employee


def current_company(request):
    if request.user.is_authenticated:
        company = Employee.objects.filter(pk=int(request.user.pk)).first()
        if company is None:
            return dict()
        return dict(company=company.company, search_form=SearchForm())
    return dict()
