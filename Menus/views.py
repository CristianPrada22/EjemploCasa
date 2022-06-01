from django.shortcuts import render

def sitemap( request ):
    """ Render a sitemap """
    return render(request, 'menus/sitemap.html')
