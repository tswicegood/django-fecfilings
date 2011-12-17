from django.core.management.base import NoArgsCommand

from fecfilings.models import Contributor


class Command(NoArgsCommand):
    def handle(self, **options):
        for c in Contributor.objects.all():
            print c.to_csv()
