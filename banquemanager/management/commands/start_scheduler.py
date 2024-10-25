import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management import BaseCommand

from banques.models import CompteEnBanque

logger = logging.getLogger(__name__)


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Exemple de tâche planifiée
    scheduler.add_job(
        scheduled_task,
        trigger=IntervalTrigger(seconds=20),
        name='my_job',
        id='my_job',
        replace_existing=True
    )
    scheduler.start()



def scheduled_task():
    logger.info("test")
    try:
        comptes = CompteEnBanque.objects.all()

        for compte in comptes:
            compte.solde+= compte.solde * compte.taux_interet / 100
            compte.save()

        logger.info(f"Comptes mis à jour avec leurs taux d'interet")

    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la récupération des comptes: {e}")




class Command(BaseCommand):
    help = 'Démarre le scheduler APScheduler'

    def handle(self, *args, **kwargs):
        start_scheduler()
        self.stdout.write(self.style.SUCCESS('Scheduler APScheduler démarré'))

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Scheduler stopped manually'))
