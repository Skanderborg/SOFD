from model.feriesaldo import Feriesaldo
from dal.feriesaldo_repo import Feriesaldo_repo


class Feriesaldo_service:
    def __init__(self, kfs_filepath, constr_lora):
        self.kfs_filepath = kfs_filepath
        self.constr_lora = constr_lora

    def get_feriesaldos_from_kfsfile(self):
        file = open(self.kfs_filepath)
        file_content = file.readlines()
        result = {}
        for line in file_content[0:]:
            if 'FERIEFORBRUG FRA KMD' in line:
                continue
            else:
                # kfs fil format er mere eller mindre bare en linje, hvor hvert sæt tegn betyder forskellige ting - her er de splittet op efter beskrivelsen
                kommuneinfo = line[0:9] # - vi bruger deti kke pt
                cpr = line[9:19]
                ans_forhold_nr = line[19:20]
                afloeningsform = line[20:21]
                ferieoptjeningsaar = line[21:25]
                dato_for_saldo = line[25:35]
                ferietimer_med_loen = line[35:41]
                evt_feriedage_med_loen = line[41:47]
                ferietimer_uden_loen = line[47:53]
                evt_feriedage_uden_loen = line[53:59]
                overfoerte_timer = line[59:65]
                evt_overfoerte_dage = line[65:71]
                feriedagstimer_sum = line[71:78]
                identifier = cpr + ans_forhold_nr
                feriesaldo = Feriesaldo(cpr,
                                        ans_forhold_nr,
                                        afloeningsform,
                                        ferieoptjeningsaar,
                                        dato_for_saldo,
                                        ferietimer_med_loen,
                                        evt_feriedage_med_loen,
                                        ferietimer_uden_loen,
                                        evt_feriedage_uden_loen,
                                        overfoerte_timer,
                                        evt_overfoerte_dage,
                                        feriedagstimer_sum)
                result[identifier] = feriesaldo
        return result

    def insert_feriesaldos_in_sofd(self):
        repo = Feriesaldo_repo(self.constr_lora)
        sofd_feriesaldos = repo.get_feriesaldos()
        kmd_feriesaldos = Feriesaldo_service.get_feriesaldos_from_kfsfile(self)
        feriesaldos_to_insert = {}
        feriesaldos_to_update = {}
        for cpr in kmd_feriesaldos:
            if cpr not in sofd_feriesaldos:
                feriesaldos_to_insert[cpr] = kmd_feriesaldos[cpr]
            else:
                sofd_saldo = sofd_feriesaldos[cpr]
                kmd_saldo = kmd_feriesaldos[cpr]
                if sofd_saldo == kmd_saldo:
                    continue
                else:
                    feriesaldos_to_update[cpr] = kmd_saldo
        repo.insert_feriesaldo(feriesaldos_to_insert)
        repo.update_feriesaldo(feriesaldos_to_update)
