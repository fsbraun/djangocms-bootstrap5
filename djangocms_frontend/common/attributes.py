from copy import copy

from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import insert_fields


class AttributesMixin:
    block_attr = {
        "description": _(
            "Advanced settings lets you add html attributes to render this element. Use them wisely and rarely."
        )
    }

    def get_fieldsets(self, request, obj=None):
        meta = self.form._meta
        fields = (
            ["tag_type"] if "tag_type" in getattr(meta, "untangled_fields", ()) else []
        )
        fields.append("attributes")
        fs = insert_fields(
            super().get_fieldsets(request, obj),
            fields,
            blockname=_("Advanced settings"),
            blockattrs=copy(self.block_attr),
            position=-1,
        )
        return fs
