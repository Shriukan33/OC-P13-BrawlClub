# Requests made in get_new_players command, in order of appearance

* handle
    * fetch_player_tag_list
        * brawlAPI.get_club_batch_player_tags_list
            * (for each club) brawlAPI.get_club_members
                httpx.AsyncClient.get                       // 1. Httpx (club members)
                