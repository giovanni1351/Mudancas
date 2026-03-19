from interfaces.candidatura_service  import CandidaturaService
from componentes.demanda import Demanda

class Candidatura(CandidaturaService):
    def __init__(self, demanda: Demanda):
        self.demanda = demanda

    def validarInformaçõesCandidaturas(self, candidatura):
        pass

    def registrarCandidatura(self, candidaturaValidada):
        pass

    def mostrarListaCandidatos(self, demanda):
        pass
