from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates missing user profiles'

    def handle(self, *args, **kwargs):
        from django.contrib.auth.models import User
        from core.models import UserProfile  # Import your UserProfile model here

        # Logic for creating missing user profiles
        users = User.objects.all()
        for user in users:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created profile for user {user.username}'))
        self.stdout.write(self.style.SUCCESS('Successfully created missing user profiles'))
