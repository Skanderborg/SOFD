import pyodbc
from model.feriesaldo import Feriesaldo


class Feriesaldo_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_feriesaldos(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT [cpr], \
                    [ans_forhold_nr], \
                    [afloeningsform], \
                    [ferieoptjeningsaar], \
                    [dato_for_saldo], \
                    [ferietimer_med_loen], \
                    [evt_feriedage_med_loen], \
                    [ferietimer_uden_loen], \
                    [evt_feriedage_uden_loen], \
                    [overfoerte_timer], \
                    [evt_overfoerte_dage], \
                    [feriedagstimer_sum] \
            FROM [dbo].[feriesaldo];")
        for row in cursor.fetchall():
            identifier = row.cpr + row.ans_forhold_nr
