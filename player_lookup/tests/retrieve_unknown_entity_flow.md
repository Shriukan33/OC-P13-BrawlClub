# CASE 1 : We're looking for a player absent from the database

retrieve
    * fetch entity (when player doesn't exist in db)
        * brawlAPI.is_player_or_club
            ---> REQUEST.GET                                       // 1. Request (status code)
        * update_player_profile
            * get_player_data
                ---> httpx.AsyncClient.get                         // 2. Httpx (player profile)
            * get_player_battlelog
                ---> httpx.AsyncClient.get                         // 3. Httpx (player's battlelog)
            * create_or_update_club
                * brawlAPI.get_club_information
                    ---> REQUEST.GET                               // 4. Request (Club profile)
    * (if player has a club) update_club_members 
        * get_club_members_data
            * brawlAPI.get_club_members_tag_list
                * get_club_members
                    ---> httpx.AsyncClient.get                     // 5. Httpx (Club members)
            * (for each member) get_player_data
                ---> httpx.AsyncClient.get                         // 6. Httpx (Players profiles) * number of members
            * (for each member) get_player_battlelog
                ---> httpx.AsyncClient.get                         // 7. Httpx (Players' battlelogs) * number of members
        * create_or_update_club
            * brawlAPI.get_club_information
                ---> REQUEST.GET                                   // 8. Request (Club profile) --> 2nd time !

# CASE 2 : We're looking for a Club absent from the database

retrieve
    * fetch entity (when player doesn't exist in db)
        * brawlAPI.is_player_or_club
            ---> REQUEST.GET                                       // 1. Request (status code) -> 404
            ---> REQUEST.GET                                       // 2. Request (status code) -> 200
        * create_or_update_club
            * brawlAPI.get_club_information
                ---> REQUEST.GET                                   // 3. Request (Club profile)
        * update_club_members 
            * get_club_members_data
                * brawlAPI.get_club_members_tag_list
                    * get_club_members
                        ---> httpx.AsyncClient.get                 // 4. Httpx (Club members)
                * (for each member) get_player_data
                    ---> httpx.AsyncClient.get                     // 5. Httpx (Players profiles) * number of members
                * (for each member) get_player_battlelog
                    ---> httpx.AsyncClient.get                     // 6. Httpx (Players' battlelogs) * number of members
            * create_or_update_club
                * brawlAPI.get_club_information
                    ---> REQUEST.GET                               // 7. Request (Club profile) --> 2nd time !
