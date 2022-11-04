# Case 1 : Update all players while club league is running

* handle
    * update_player_batch
        * get_all_players_profiles_and_battlelog
            * (for each player) get_player_data
                ---> httpx.AsyncClient.get                       // 1. Httpx (player profile)
            * (for each player) get_player_battlelog
                ---> httpx.AsyncClient.get                       // 2. Httpx (player's battlelog)

        * update_player_infos
            * create_club_batch
                * (for each club) get_club_information
                    ---> httpx.AsyncClient.get                   // 3. Httpx (Club profile)