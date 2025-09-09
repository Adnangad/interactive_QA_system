from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from .cron import scrape_aljazeera
from .rag import ingest
import os


class BackendApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_api'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  
            scheduler = BackgroundScheduler()
            scheduler.add_job(
                scrape_aljazeera,
                'interval',
                minutes=10,
                max_instances=2,
                coalesce=True,     
                misfire_grace_time=60
            )
            scheduler.add_job(ingest, 'interval', minutes=10, max_instances=2, coalesce=True, misfire_grace_time=60)
            scheduler.start()