from django.core.management.base import BaseCommand
from core.models import Tenant

class Command(BaseCommand):
    help = 'Create a tenant'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Tenant name')
        parser.add_argument('domain', type=str, help='Tenant domain (for identification)')

    def handle(self, *args, **options):
        name = options['name']
        domain = options['domain']
        
        tenant, created = Tenant.objects.get_or_create(
            domain=domain,
            defaults={'name': name, 'is_active': True}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created tenant: {tenant.name} (domain: {tenant.domain})'))
            self.stdout.write(f'Tenant ID: {tenant.id}')
        else:
            self.stdout.write(self.style.WARNING(f'Tenant with domain "{domain}" already exists'))
            self.stdout.write(f'Tenant ID: {tenant.id}')

