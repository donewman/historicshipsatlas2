from atlas.forms import BasicSearchForm

def basic_search_form(request):
    return {'basic_search_form' : BasicSearchForm()}
