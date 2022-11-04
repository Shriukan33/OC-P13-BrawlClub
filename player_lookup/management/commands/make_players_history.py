import logging
from django.core.management.base import BaseCommand
from player_lookup.models import Player, PlayerHistory

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Create players history records"

    def handle(self, *args, **options):
        player_count = Player.objects.count()

        logger.info(f"About to create {player_count} player history records.")
        batch_size = 999
        top_limit = player_count // batch_size * batch_size
        first_loop = True
        for i in range(0, top_limit + batch_size + 1, batch_size):
            if first_loop:
                first_loop = False
                new_start = i
                continue

            logger.info(f"Updating row {new_start} to {i}")
            player_batch = Player.objects.all()[new_start:i]
            self.create_records(player_batch)
            new_start = i

        self.stdout.write(
            self.style.SUCCESS("Successfully created all records"), ending="\n"
        )

    def create_records(self, player_batch):
        records_batch = []
        player: Player
        for player in player_batch:
            records_batch.append(player.create_player_history_instance())

        PlayerHistory.objects.bulk_create(records_batch)
