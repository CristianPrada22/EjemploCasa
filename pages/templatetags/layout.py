from __future__ import unicode_literals

from django import template
from django.utils.html import format_html

#from djangoplicity.media.models import Image, ImageComparison

register = template.Library()


@register.inclusion_tag('templatetags/image_frame.html')
def image_frame(**kwargs):
    pk = kwargs.get('id', None)

    try:
        obj = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        obj = None

    # If not url is given default to link to image
    url = kwargs.get('url', None)
    if url is None and obj:
        url = obj.get_absolute_url()

    # If no alt is given default to image title
    alt = kwargs.get('alt', None)
    if not alt and obj:
        alt = obj.title

    # If no credit is given default to image credit
    credit = kwargs.get('credit', None)
    if credit is None and obj:
        # We don't use "if not credit" as we may get credit = '' if
        # we don't want to show any credit
        credit = obj.credit

    return {
        'object': obj,
        'alt': alt,
        'legend': kwargs.get('legend', None),
        'credit': credit,
        'url': url,
        'position': kwargs.get('position', None),
        'width': kwargs.get('width', None),
    }


@register.inclusion_tag('templatetags/comparison_frame.html')
def comparison_frame(**kwargs):
    pk = kwargs.get('id', None)

    try:
        obj = ImageComparison.objects.get(pk=pk)
    except ImageComparison.DoesNotExist:
        obj = None

    # If no credit is given default to image credit
    credit = kwargs.get('credit', None)
    if credit is None and obj:
        # We don't use "if not credit" as we may get credit = '' if
        # we don't want to show any credit
        credit = obj.credit

    return {
        'object': obj,
        'legend': kwargs.get('legend', None),
        'credit': credit,
        'position': kwargs.get('position', None),
        'width': kwargs.get('width', None),
    }


@register.inclusion_tag('templatetags/static_image_frame.html')
def static_image_frame(**kwargs):
    return {
        'src': kwargs.get('src', None),
        'alt': kwargs.get('alt', None),
        'url': kwargs.get('url', None),
        'legend': kwargs.get('legend', None),
        'credit': kwargs.get('credit', None),
        'position': kwargs.get('position', None),
        'width': kwargs.get('width', None),
    }


@register.simple_tag
def spacer(height):
    return format_html('<div style="height: {}"></div>', height)


@register.simple_tag
def dropcaps(text, **kwargs):
    width = kwargs.get('width', '50%')
    position = kwargs.get('position', 'left')
    if position not in ('left', 'right', 'center'):
        position = 'left'

    return format_html('<div style="width: {}" class="drop-caps {}">{}</div>',
        width, position, text)


@register.inclusion_tag('templatetags/youtube_frame.html')
def youtube_frame(youtube_id, *args, **kwargs):
    return {
        'youtube_id': youtube_id,
        'legend': kwargs.get('legend', None),
        'credit': kwargs.get('credit', None),
        'autoplay': 'autoplay' in args,
        'mute': 'mute' in args,
    }
