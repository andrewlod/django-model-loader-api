from django.core.management.base import BaseCommand
import random
from ...models import ModelOutputType, StorageType

# python manage.py seed --mode=refresh

""" Clear all data and inserts data """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "Seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    ModelOutputType.objects.all().delete()
    StorageType.objects.all().delete()


def create_model_output_type(type):
    """Creates a Model Output Type object"""
    model_output_type = ModelOutputType(
        type=type
    )
    model_output_type.save()
    return model_output_type

def create_storage_type(type):
    """Creates a Model Output Type object"""
    storage_type = StorageType(
        type=type
    )
    storage_type.save()
    return storage_type

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    model_output_types = ["String", "Image"]
    storage_types = ["AWS", "Local"]
    
    for type in model_output_types:
        create_model_output_type(type)
    
    for type in storage_types:
        create_storage_type(type)