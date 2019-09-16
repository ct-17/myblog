import json
import os
from django import template
from django.urls import reverse
from django.forms import CheckboxInput, ModelChoiceField, Select, ModelMultipleChoiceField, SelectMultiple
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from blog_ct import settings
# from blog_ct.models import Bookmark
from ct_admin.utils import get_menu_items
from urllib.parse import parse_qsl

register = template.Library()
assignment_tag = register.assignment_tag if hasattr(register, 'assignment_tag') else register.simple_tag

@assignment_tag(takes_context=True)
def ct_get_menu(context):
    return get_menu_items(context)

