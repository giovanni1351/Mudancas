from componentes.demanda import Demanda
from componentes.candidatura import Candidatura

if __name__ == "__main__":
    comp_demanda = Demanda()
    comp_candidatura = Candidatura(demanda=comp_demanda)
