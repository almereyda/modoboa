"""Custom settings."""

from django import forms
from django.utils.translation import ugettext_lazy as _

from modoboa.lib.form_utils import SeparatorField, YesNoField
from modoboa.lib.parameters import AdminParametersForm


class ParametersForm(AdminParametersForm):
    app = "limits"

    defv_sep = SeparatorField(label=_("Default per-admin limits"))

    deflt_user_domain_admins_limit = forms.IntegerField(
        label=_("Domain admins"),
        initial=0,
        help_text=_(
            "Maximum number of allowed domain administrators for a new "
            "administrator. (0 to deny any creation, -1 to allow unlimited "
            "creations)"
        ),
        widget=forms.widgets.TextInput(
            attrs={"class": "col-md-1 form-control"})
    )
    deflt_user_domains_limit = forms.IntegerField(
        label=_("Domains"),
        initial=0,
        help_text=_(
            "Maximum number of allowed domains for a new administrator. "
            "(0 to deny any creation, -1 to allow unlimited creations)"
        ),
        widget=forms.widgets.TextInput(
            attrs={"class": "col-md-1 form-control"})
    )
    deflt_user_domain_aliases_limit = forms.IntegerField(
        label=_("Domain aliases"),
        initial=0,
        help_text=_(
            "Maximum number of allowed domain aliases for a new "
            "administrator. (0 to deny any creation, -1 to allow "
            "unlimited creations)"
        ),
        widget=forms.widgets.TextInput(
            attrs={"class": "col-md-1 form-control"})
    )
    deflt_user_mailboxes_limit = forms.IntegerField(
        label=_("Mailboxes"),
        initial=0,
        help_text=_(
            "Maximum number of allowed mailboxes for a new administrator. "
            "(0 to deny any creation, -1 to allow unlimited creations)"
        ),
        widget=forms.widgets.TextInput(
            attrs={"class": "col-md-1 form-control"})
    )
    deflt_user_mailbox_aliases_limit = forms.IntegerField(
        label=_("Mailbox aliases"),
        initial=0,
        help_text=_(
            "Maximum number of allowed aliases for a new administrator. "
            "(0 to deny any creation, -1 to allow unlimited creations)"
        ),
        widget=forms.widgets.TextInput(
            attrs={"class": "col-md-1 form-control"})
    )

    domain_limits_sep = SeparatorField(label=_("Default per-domain limits"))

    enable_domain_limits = YesNoField(
        label=_("Enable per-domain limits"),
        initial="no",
        help_text=_("Enable or disable per-domain limits")
    )

    # deflt_domain_domain_admins_limit = forms.IntegerField(
    #     label=_("Domain admins"),
    #     initial=0,
    #     help_text=_(
    #         "Maximum number of allowed domain administrators for a new "
    #         "domain. (0 to deny any creation, -1 to allow unlimited "
    #         "creations)"
    #     ),
    #     widget=forms.widgets.TextInput(
    #         attrs={"class": "col-md-1 form-control"})
    # )
    deflt_domain_domain_aliases_limit = forms.IntegerField(
        label=_("Domain aliases"),
        initial=0,
        help_text=_(
            "Maximum number of allowed domain aliases for a new "
            "domain. (0 to deny any creation, -1 to allow "
            "unlimited creations)"
        ),
        widget=forms.widgets.TextInput(
            attrs={"class": "col-md-1 form-control"})
    )
    deflt_domain_mailboxes_limit = forms.IntegerField(
        label=_("Mailboxes"),
        initial=0,
        help_text=_(
            "Maximum number of allowed mailboxes for a new domain. "
            "(0 to deny any creation, -1 to allow unlimited creations)"
        ),
        widget=forms.widgets.TextInput(
            attrs={"class": "col-md-1 form-control"})
    )
    deflt_domain_mailbox_aliases_limit = forms.IntegerField(
        label=_("Mailbox aliases"),
        initial=0,
        help_text=_(
            "Maximum number of allowed aliases for a new domain. "
            "(0 to deny any creation, -1 to allow unlimited creations)"
        ),
        widget=forms.widgets.TextInput(
            attrs={"class": "col-md-1 form-control"})
    )

    visibility_rules = {
        "deflt_domain_mailboxes_limit": "enable_domain_limits=yes",
        "deflt_domain_mailbox_aliases_limit": "enable_domain_limits=yes",
        "deflt_domain_domain_aliases_limit": "enable_domain_limits=yes",
    }

    def __init__(self, *args, **kwargs):
        super(AdminParametersForm, self).__init__(*args, **kwargs)
        self._load_extra_parameters('A')
