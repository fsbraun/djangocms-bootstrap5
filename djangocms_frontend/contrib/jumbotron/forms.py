from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common.background import BackgroundFormMixin
from djangocms_frontend.contrib import jumbotron
from djangocms_frontend.fields import (
    AttributesFormField,
    ColoredButtonGroup,
    TagTypeFormField,
)

mixin_factory = settings.get_forms(jumbotron)


class JumbotronForm(
    mixin_factory("Jumbotron"), BackgroundFormMixin, EntangledModelForm
):
    """
    Components > "Jumbotron" Plugin
    https://getbootstrap.com/docs/5.0/components/jumbotron/
    """

    class Meta:
        entangled_fields = {
            "config": [
                "jumbotron_fluid",
                "template",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    template = forms.ChoiceField(
        label=_("Template"),
        choices=settings.JUMBOTRON_TEMPLATE_CHOICES,
        initial=settings.JUMBOTRON_TEMPLATE_CHOICES[0][0],
        widget=forms.HiddenInput
        if len(settings.JUMBOTRON_TEMPLATE_CHOICES) < 2
        else forms.Select,
    )
    jumbotron_fluid = forms.BooleanField(
        label=_("Fluid"),
        initial=False,
        required=False,
        help_text=_(
            "Makes the jumbotron full the will width of the container or window."
        ),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
