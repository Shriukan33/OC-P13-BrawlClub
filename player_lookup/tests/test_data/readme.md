These data are pulled from the actual API at the time I'm writing these tests
P0GVGVRP is the club tag 
2RQRYV0L is a player tag from a member of the club
9090YYGQ is also a player tag from a member of the club
Each player has a battle log composed of its 24 last battles
Each player has a profile

Players have 2 endpoints on the BrawlStars API : 
- /players/{player_tag} -> Provides the player's profile
- /players/{player_tag}/battlelog -> Provides the player's battle log

Clubs have 2 endpoints :
- /clubs/{club_tag} -> Provides the club's profile
- /clubs/{club_tag}/members -> Provides the club's member list

Each of the files in this folder are named after the endpoint they are testing with the associated tag.
For example, the file test_player_2RQRYV0L_battlelog.json is the battle log of the player with the tag 2RQRYV0L
