
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login

from .views import (UserProfileDetailView, UserProfileUpdateView,
                    ManageUserSubscriptionsView, ChangeXMPPPasswordView,
                    password_reset_done_custom, password_reset_complete_custom)


urlpatterns = patterns('',
    url(r'^register/$', 'accounts.views.signup', name='signup'),

    url(r'^novo-login/$',
        login,
        {'template_name': 'novo_login.html',
         'redirect_field_name': 'previous_path'},
        name='novo_login'),

    url(r'^password-reset/$', auth_views.password_reset,
        {'template_name': 'registration/password_reset_form_custom.html',
         'email_template_name':'registration/password_reset_email_custom.html'},
        name="password_reset"),

    url(r'^password-reset-done/?$', password_reset_done_custom,
        name="password_reset_done"),

    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm_custom.html'},
        name="password_reset_confirm"),

    url(r'^password-reset-complete/$', 'accounts.views.password_reset_complete_custom',
        name="password_reset_complete"),

    url(r'^change-password/?$', auth_views.password_change,
        {'template_name': 'registration/password_change_form_custom.html'},
        name='password_change'),

    url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='novo_logout'),

    url(r'^(?P<username>[\w@+.-]+)/?$',
        UserProfileDetailView.as_view(), name='user_profile'),

    url(r'^(?P<username>[\w@+.-]+)/edit/?$',
        UserProfileUpdateView.as_view(), name='user_profile_update'),

    url(r'^(?P<username>[\w@+.-]+)/subscriptions/?$',
        ManageUserSubscriptionsView.as_view(), name='user_list_subscriptions'),
)
