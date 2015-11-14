from django.contrib import admin
from django.apps import apps
from django import template
# from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe as _S
from django.core.urlresolvers import reverse


def _T(src, **ctx):
    return _S(template.Template(src).render(template.Context(ctx)))


def change_link(model):
    return reverse("admin:{0}_{1}_change".format(
        model._meta.app_label,
        model._meta.model_name,
    ), args=[model.id])


def register(app_fullname, admins, ignore_models=[]):
    app_label = app_fullname.split('.')[-2:][0]
    for n, model in apps.get_app_config(app_label).models.items():
        if model.__name__ in ignore_models:
            continue
        name = "%sAdmin" % model.__name__
        admin_class = admins.get(name, None)
        if admin_class is None:
            admin_class = type(
                "%sAdmin" % model.__name__,
                (admin.ModelAdmin,), {},
            )

        if admin_class.list_display == ('__str__',):
            excludes = getattr(admin_class, 'list_excludes', ())
            additionals = getattr(admin_class, 'list_additionals', ())
            admin_class.list_display = tuple(
                [f.name for f in model._meta.fields
                 if f.name not in excludes]) + additionals

        admin.site.register(model, admin_class)


register(__name__, globals())
