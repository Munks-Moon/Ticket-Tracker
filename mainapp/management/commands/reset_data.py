from django.core.management.base import BaseCommand
from mainapp.models import Ticket, Message

class Command(BaseCommand):
    help = 'Reset demo data to its original state'

    def handle(self, *args, **options):
        # Preserve original tickets and users
        excluded_ticket_ids = list(range(1, 16))  # IDs 1 to 14

        Ticket.objects.exclude(id__in=excluded_ticket_ids).delete()

        Message.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Demo data has been reset successfully.'))