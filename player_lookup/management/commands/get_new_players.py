import logging
from django.core.management.base import BaseCommand
from player_lookup.models import Player, Club
from player_lookup.views import brawl_api
from asgiref.sync import async_to_sync

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = """Create Player records for all clubs in database

    This command will create a Player record for each player in each club in the
    database.
    To the difference of update_all_players, this command will not update existing
    records, but simply create blank Player instance that another command will fill.
    """

    def handle(self, *args, **options):
        logger.info("Starting get_new_players command")
        self.all_club_tags = Club.objects.values_list("club_tag", flat=True)
        club_count = len(self.all_club_tags)
        logger.info(f"Creating Player records for {club_count} clubs")
        batch_size = 999
        number_of_batches = club_count // batch_size * batch_size
        first_loop = True
        for i in range(0, number_of_batches + 1, batch_size):
            if first_loop:
                first_loop = False
                start = i
                continue
            logger.info(f"Creating Player records for clubs {start} to {i}")
            tag_list = self.fetch_player_tag_list(self.all_club_tags[start:i])
            start = i
            self.create_player_records(tag_list)

        # Do the last batch of clubs, it's always smaller than batch_size
        logger.info(f"Creating Player records for clubs {start} to {club_count}")
        tag_list = self.fetch_player_tag_list(self.all_club_tags[start:club_count])
        self.create_player_records(tag_list)

    @async_to_sync
    async def fetch_player_tag_list(self, club_tag_list: list) -> list:
        """Fetch player tag list from API for each club in list

        Keyword arguments:
        club_tag_list -- list of club tags to fetch player tag list from BS API
        """
        return await brawl_api.get_club_batch_player_tags_list(club_tag_list)

    def create_player_records(self, tag_list: list):
        """Create Player records for each tag in tag_list if player doesn't exist

        Keyword arguments:
        tag_list -- list of player tags to create Player records for
        """
        players_to_create = []
        for tag in tag_list:
            if not Player.objects.filter(player_tag=tag).exists():
                players_to_create.append(
                    Player(player_tag=tag, player_name="Not Fetched Yet")
                )

        logger.info(f"Creating {len(players_to_create)} Player records")
        Player.objects.bulk_create(players_to_create)
