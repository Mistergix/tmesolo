from module_teo_nicolas.lib.qsoccer import QSoccer

nb_player_per_team = 4
qsoccer = QSoccer.get_instance(nb_player_per_team)

exit()

qsoccer.Train(show=False)
qsoccer.printBestsAndWorsts()