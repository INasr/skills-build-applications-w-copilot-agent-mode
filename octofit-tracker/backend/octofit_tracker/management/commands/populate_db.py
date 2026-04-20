from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        self.stdout.write('Creating teams...')
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        self.stdout.write('Creating users...')
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        self.stdout.write('Creating activities...')
        Activity.objects.create(user=users[0], type='Running', duration=30, date='2026-04-20')
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date='2026-04-19')
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date='2026-04-18')
        Activity.objects.create(user=users[3], type='Yoga', duration=50, date='2026-04-17')

        self.stdout.write('Creating workouts...')
        w1 = Workout.objects.create(name='Hero HIIT', description='High intensity interval training for heroes.')
        w2 = Workout.objects.create(name='Power Yoga', description='Yoga for strength and flexibility.')
        w1.suggested_for.set([users[0], users[1]])
        w2.suggested_for.set([users[2], users[3]])

        self.stdout.write('Creating leaderboards...')
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)


        self.stdout.write('Ensuring unique index on user email...')
        from django.conf import settings
        from pymongo import MongoClient
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        db[User._meta.db_table].create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
