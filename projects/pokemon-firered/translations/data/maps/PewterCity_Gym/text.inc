PewterCity_Gym_Text_BrockIntro::
    .string "Tak jsi tady. Já jsem BROCK.\n"
    .string "Jsem GYM LÍDR PEWTERU.\p"
    .string "Má skálopevná vule se odrází\n"
    .string "i v mych POKéMONech.\p"
    .string "Mí POKéMONi jsou tvrdí jako\n"
    .string "skála, plní pevné vule.\p"
    .string "Presne tak - mí POKéMONi jsou\n"
    .string "vsichni typu ROCK!\p"
    .string "Hahaha! Chces me vyzvat\n"
    .string "i kdyz vís, ze prohrajes?\p"
    .string "To je cest TRÉNÉRA, která te\n"
    .string "nutí mi celit.\p"
    .string "Dobrá tedy!\n"
    .string "Ukaz mi své nejlepsí!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}$"

@ NOTE: This defeat text actually causes a buffer overflow. It's too long for the gDisplayedStringBattle
@ buffer that it's put into, and it stomps all over the gBattleTextBuffs after, as well as the otherwise
@ unused array after that, sFlickerArray. Perhaps that's the reason why said array exists.
PewterCity_Gym_Text_BrockDefeat::
    .string "Podcenil jsem te, a tak\n"
    .string "jsem prohrál.\p"
    .string "Jako dukaz vítezství ti dávám\n"
    .string "tento…oficiální POKéMON\l"
    .string "LIGA BOULDERBADGE.\p"
    .string "{FONT_NORMAL}{PLAYER} obdrzel BOULDERBADGE\n"
    .string "od BROCKA!{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}\p"
    .string "{FONT_MALE}Drzbou BOULDERBADGE budou tví\n"
    .string "POKéMONi silnejsí.\p"
    .string "Také to umozní pouzít útok\n"
    .string "FLASH mimo boj.\p"
    .string "Samozrejme, POKéMON musí útok\n"
    .string "FLASH umet, aby ho mohl pouzít.$"

PewterCity_Gym_Text_TakeThisWithYou::
    .string "Pockej!\n"
    .string "Vezmi si s sebou tohle.$"

PewterCity_Gym_Text_ReceivedTM39FromBrock::
    .string "{PLAYER} obdrzel TM39\n"
    .string "od BROCKA.$"

PewterCity_Gym_Text_ExplainTM39::
    .string "TM, Technical Machine, obsahuje\n"
    .string "techniku pro POKéMONa.\p"
    .string "Pouzitím TM se POKéMON naucí\n"
    .string "útok, ktery je v ní obsazen.\p"
    .string "TM lze pouzít pouze jednou.\p"
    .string "Takze az ji pouzijes, vyber\n"
    .string "POKéMONa peclive.\p"
    .string "Mimochodem…\n"
    .string "TM39 obsahuje ROCK TOMB.\p"
    .string "Hází balvany na neprítele a\n"
    .string "snizuje mu RYCHLOST.$"

PewterCity_Gym_Text_BrockPostBattle::
    .string "V tom nasem velkém svete jsou\n"
    .string "vsemozní TRÉNÉRI.\p"
    .string "Zdá se, ze más velky talent\n"
    .string "jako POKéMON TRÉNÉR.\p"
    .string "Tak ti dám tip.\p"
    .string "Jdi do GYM v CERULEAN a otestuj\n"
    .string "své schopnosti.$"

PewterCity_Gym_Text_DontHaveRoomForThis::
    .string "Nemás na to místo.$"

PewterCity_Gym_Text_LiamIntro::
    .string "Stuj, maly!\p"
    .string "Jsi deset tisíc svetelnych let\n"
    .string "od toho, abys celil BROCKOVI!$"

PewterCity_Gym_Text_LiamDefeat::
    .string "Sakra!\p"
    .string "Svetelné roky nejsou cas…\n"
    .string "Merí vzdálenost!$"

PewterCity_Gym_Text_LiamPostBattle::
    .string "Jsi docela dobry.\n"
    .string "…Ale ne tak dobry jako BROCK!$"

PewterCity_Gym_Text_LetMeTakeYouToTheTop::
    .string "Cau!\n"
    .string "Chces snít ve velkém?\p"
    .string "Mas odvahu snít o tom, ze se\n"
    .string "stanes POKéMON sampiónem?\p"
    .string "Nejsem TRÉNÉR, ale poradím ti,\n"
    .string "jak vyhrát.\p"
    .string "Vezmu te az na vrchol!$"

PewterCity_Gym_Text_LetsGetHappening::
    .string "Tak jo!\n"
    .string "Pojdme do toho!$"

PewterCity_Gym_Text_TryDifferentPartyOrders::
    .string "První POKéMON v zápase je ten\n"
    .string "vlevo v seznamu POKéMONu.\p"
    .string "Zmenou poradí POKéMONu muzes\n"
    .string "získat vyhodu.\p"
    .string "Zkus ruzná poradí, ktera se\n"
    .string "hodí proti soupervu tymu.$"

PewterCity_Gym_Text_ItsFreeLetsGetHappening::
    .string "Je to zdarma!\n"
    .string "Pojdme do toho!$"

PewterCity_Gym_Text_YoureChampMaterial::
    .string "Presne jak jsem si myslel!\n"
    .string "Más na to byt POKéMON sampiónem!$"

PewterCity_Gym_Text_GymStatue::
    .string "PEWTER POKéMON GYM\n"
    .string "LÍDR: BROCK\p"
    .string "VÍTEZNÍ TRÉNÉRI:\n"
    .string "{RIVAL}$"

PewterCity_Gym_Text_GymStatuePlayerWon::
    .string "PEWTER POKéMON GYM\n"
    .string "LÍDR: BROCK\p"
    .string "VÍTEZNÍ TRÉNÉRI:\n"
    .string "{RIVAL}, {PLAYER}$"
