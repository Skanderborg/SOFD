class Feriesaldo:
    def __init__(self, cpr, ans_forhold_nr, afloeningsform, ferieoptjeningsaar, dato_for_saldo,
                 ferietimer_med_loen, evt_feriedage_med_loen, ferietimer_uden_loen, evt_feriedage_uden_loen,
                 overfoerte_timer, evt_overfoerte_dage, feriedagstimer_sum):
        self.cpr = cpr
        self.ans_forhold_nr = ans_forhold_nr
        self.afloeningsform = afloeningsform
        self.ferieoptjeningsaar = ferieoptjeningsaar
        self.dato_for_saldo = dato_for_saldo
        self.ferietimer_med_loen = ferietimer_med_loen
        self.evt_feriedage_med_loen = evt_feriedage_med_loen
        self.ferietimer_uden_loen = ferietimer_uden_loen
        self.evt_feriedage_uden_loen = evt_feriedage_uden_loen
        self.overfoerte_timer = overfoerte_timer
        self.evt_overfoerte_dage = evt_overfoerte_dage
        self.feriedagstimer_sum = feriedagstimer_sum

    def __eq__(self, other):
        return self.__dict__ == other.__dict__