
import os

from django.conf import settings

from revproxy.views import ProxyView
from .models import Wiki, Ticket, Revision
from hitcounter.views import HitCounterViewMixin


CWD = os.path.abspath(os.path.dirname(__file__))
DIAZO_RULES_DIR = os.path.join(CWD, 'diazo')

class TracProxyView(HitCounterViewMixin, ProxyView):
    upstream = settings.COLAB_TRAC_URL
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'proxy/trac.html'
    diazo_rules = os.path.join(DIAZO_RULES_DIR, 'trac.xml')
    html5 = True

    def get_object(self):
        obj = None

        if self.request.path_info.startswith('/wiki'):
            wiki_name = self.request.path_info.split('/', 2)[-1]
            if not wiki_name:
                wiki_name = 'WikiStart'
            try:
                obj = Wiki.objects.get(name=wiki_name)
            except Wiki.DoesNotExist:
                return None
        elif self.request.path_info.startswith('/ticket'):
            ticket_id = self.request.path_info.split('/')[2]
            try:
                obj = Ticket.objects.get(id=ticket_id)
            except (Ticket.DoesNotExist, ValueError):
                return None
        elif self.request.path_info.startswith('/changeset'):
            try:
                changeset, repo = self.request.path_info.split('/')[2:4]
            except ValueError:
                return None
            try:
                obj = Revision.objects.get(rev=changeset,
                                           repository_name=repo)
            except Revision.DoesNotExist:
                return None

        return obj


class JenkinsProxyView(ProxyView):
    upstream = settings.COLAB_CI_URL
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'base.html'
    diazo_rules = os.path.join(DIAZO_RULES_DIR, 'jenkins.xml')
    html5 = True
