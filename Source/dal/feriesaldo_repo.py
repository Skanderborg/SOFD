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
            feriesaldo = Feriesaldo(row.cpr,
                                    row.ans_forhold_nr,
                                    row.afloeningsform,
                                    row.ferieoptjeningsaar,
                                    row.dato_for_saldo,
                                    row.ferietimer_med_loen,
                                    row.evt_feriedage_med_loen,
                                    row.ferietimer_uden_loen,
                                    row.evt_feriedage_uden_loen,
                                    row.overfoerte_timer,
                                    row.evt_overfoerte_dage,
                                    row.feriedagstimer_sum)
            result[identifier] = feriesaldo
        return result

    def insert_feriesaldo(self, feriesaldos):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in feriesaldos:
            feriesaldo = feriesaldos[key]
            cursor.execute(
                "INSERT INTO [dbo].[feriesaldo]([cpr], \
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
                                                [feriedagstimer_sum]) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                feriesaldo.cpr,
                feriesaldo.ans_forhold_nr,
                feriesaldo.afloeningsform,
                feriesaldo.ferieoptjeningsaar,
                feriesaldo.dato_for_saldo,
                feriesaldo.ferietimer_med_loen,
                feriesaldo.evt_feriedage_med_loen,
                feriesaldo.ferietimer_uden_loen,
                feriesaldo.evt_feriedage_uden_loen,
                feriesaldo.overfoerte_timer,
                feriesaldo.evt_overfoerte_dage,
                feriesaldo.feriedagstimer_sum
            )
        cnxn.commit()

    def update_feriesaldo(self, feriesaldos):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in feriesaldos:
            feriesaldo = feriesaldos[key]
            cursor.execute("UPDATE [dbo].[feriesaldo] \
                            SET [ans_forhold_nr] = ?, \
                                [afloeningsform] = ?, \
                                [ferieoptjeningsaar] = ?, \
                                [dato_for_saldo] = ?, \
                                [ferietimer_med_loen] = ?, \
                                [evt_feriedage_med_loen] = ?, \
                                [ferietimer_uden_loen] = ?, \
                                [evt_feriedage_uden_loen] = ?, \
                                [overfoerte_timer] = ?, \
                                [evt_overfoerte_dage] = ?, \
                                [feriedagstimer_sum] = ? \
                            WHERE [cpr] = ?",
                            feriesaldo.ans_forhold_nr,
                            feriesaldo.afloeningsform,
                            feriesaldo.ferieoptjeningsaar,
                            feriesaldo.dato_for_saldo,
                            feriesaldo.ferietimer_med_loen,
                            feriesaldo.evt_feriedage_med_loen,
                            feriesaldo.ferietimer_uden_loen,
                            feriesaldo.evt_feriedage_uden_loen,
                            feriesaldo.overfoerte_timer,
                            feriesaldo.evt_overfoerte_dage,
                            feriesaldo.feriedagstimer_sum,
                            feriesaldo.cpr)
        cnxn.commit()