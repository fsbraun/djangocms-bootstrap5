# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from six import with_metaclass
from functools import partial

import django.core.exceptions
import django.db.models
import django.forms

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.encoding import smart_text

from cms.models.pluginmodel import CMSPlugin

from . import fields


# Fieldset setup used specifically for the link
link_fieldset = (
    ('Link', {
        'fields': (
            'link_page',
            'link_file',
            'link_url',
            'link_mailto',
            'link_phone',
        ),
        'description': 'Choose one of the link types below.',
    }),
    ('Link options', {
        'fields': (
            ('link_target', 'link_anchor',),
        ),
    }),
)


# Add an app namespace to related_name to avoid field name clashes
# with any other plugins that have a field with the same name as the
# lowercase of the class name of this model.
# https://github.com/divio/django-cms/issues/5030
CMSPluginField = partial(
    models.OneToOneField,
    to=CMSPlugin,
    related_name='%(app_label)s_%(class)s',
    parent_link=True,
)


"""
Used in:
- Bootstrap3RowPlugin, Bootstrap3ColumnPlugin
"""
class Classes(django.db.models.TextField):
    default_field_class = fields.Classes
    south_field_class = 'django.db.models.fields.TextField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _('Classes')
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = ''
        if 'help_text' not in kwargs:
            kwargs['help_text'] = _('Space separated classes that are added to '
                'the class. See <a href="http://getbootstrap.com/css/" '
                'target="_blank">Bootstrap 3 documentation</a>.')
        super(Classes, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Classes, self).formfield(**defaults)




class SouthMixinBase(object):
    south_field_class = ''

    def south_field_triple(self):
        """Returns a suitable description of this field for South."""
        if not self.south_field_class:
            raise NotImplementedError('please set south_field_class when using the south field mixin')
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = self.south_field_class
        args, kwargs = introspector(self)
        # That's our definition!
        return field_class, args, kwargs


class SouthCharFieldMixin(SouthMixinBase):
    south_field_class = "django.db.models.fields.CharField"


class SouthIntegerFieldMixin(SouthMixinBase):
    south_field_class = "django.db.models.fields.IntegerField"


class Context(django.db.models.fields.CharField, SouthCharFieldMixin):
    default_field_class = fields.Context

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = False
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(Context, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
            'choices_form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Context, self).formfield(**defaults)

    def get_choices(self, **kwargs):
        # if there already is a "blank" choice, don't add another
        # default blank choice
        if '' in dict(self.choices).keys():
            kwargs['include_blank'] = False
        return super(Context, self).get_choices(**kwargs)


class Size(django.db.models.CharField, SouthCharFieldMixin):
    default_field_class = fields.Size

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(Size, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
            'choices_form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Size, self).formfield(**defaults)

    def get_choices(self, **kwargs):
        # if there already is a "blank" choice, don't add another
        # default blank choice
        if '' in dict(self.choices).keys():
            kwargs['include_blank'] = False
        return super(Size, self).get_choices(**kwargs)


class Icon(django.db.models.CharField, SouthCharFieldMixin):
    default_field_class = fields.Icon

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(Icon, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Icon, self).formfield(**defaults)


class IntegerField(django.db.models.IntegerField, SouthIntegerFieldMixin):
    default_field_class = fields.Integer

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        django.db.models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
            'min_value': self.min_value,
            'max_value': self.max_value,
        }
        defaults.update(kwargs)
        return super(IntegerField, self).formfield(**defaults)


class MiniText(django.db.models.TextField):
    default_field_class = fields.MiniText
    south_field_class = "django.db.models.fields.TextField"

    def __init__(self, *args, **kwargs):
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = ''
        super(MiniText, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(MiniText, self).formfield(**defaults)


class LinkOrButton(django.db.models.fields.CharField, SouthCharFieldMixin):
    default_field_class = fields.LinkOrButton

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 10
        if 'blank' not in kwargs:
            kwargs['blank'] = False
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(LinkOrButton, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
            'choices_form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(LinkOrButton, self).formfield(**defaults)

    def get_choices(self, **kwargs):
        # if there already is a "blank" choice, don't add another
        # default blank choice
        if '' in dict(self.choices).keys():
            kwargs['include_blank'] = False
        return super(LinkOrButton, self).get_choices(**kwargs)


class Responsive(MiniText):
    default_field_class = fields.Responsive

    def __init__(self, *args, **kwargs):
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = ''
        super(Responsive, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Responsive, self).formfield(**defaults)


class ResponsivePrint(MiniText):
    default_field_class = fields.ResponsivePrint

    def __init__(self, *args, **kwargs):
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = ''
        super(ResponsivePrint, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(ResponsivePrint, self).formfield(**defaults)


#TODO:
#   * btn-block, disabled
#   * pull-left, pull-right
#   * margins/padding
