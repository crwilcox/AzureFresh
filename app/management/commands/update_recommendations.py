from django.core.management.base import BaseCommand
from app.models import Product
import csv
import requests
import base64
from recommendationservice import RecommendationService, Uris, BuildStatus
import config
import os
from datetime import datetime

class Command(BaseCommand):
    args = ''
    help = ''
    
    def _update_recommendations(self):
        print('Updating Recommendation Model using datamarket.azure.com')

        email = config.azure_datamarket_email
        key = config.azure_datamarket_access_key
        model_id = config.model_id

        rs = RecommendationService(email, key)

        # if model_id is set we are updating.  otherwise we need to make a new model
        if not model_id:
            print('creating model')
            model_id = rs.create_model('groceries' + datetime.now().strftime('%Y%m%d%H%M%S'))
            print('model id: ', model_id)

        print('importing catalog and usage file')
        catalog_path = os.path.join('app', 'management', 'commands', 'catalog.csv')
        transactions_path = os.path.join('app', 'management', 'commands', 'transactions.csv')

        rs.import_file(model_id, catalog_path, Uris.import_catalog)
        rs.import_file(model_id, transactions_path, Uris.import_usage)

        print('building model')
        build_id = rs.build_fbt_model(model_id)
        status = rs.wait_for_build(model_id, build_id)

        if status != BuildStatus.success:
            print('Unsuccessful in building the model, failing now.')
            return

        # update model active build
        rs.update_model(model_id, None, build_id)
        
        print('Built a model. Model ID:{} Build ID:{}'.format(model_id, build_id))
        print('Add this model id to config.py if you wish to use this model')

    def handle(self, *args, **options):
        self._update_recommendations()
