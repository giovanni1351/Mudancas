from abc import ABC, abstractmethod

class CandidaturaService(ABC):

    @abstractmethod
    def validarInformaçõesCandidaturas(self, candidatura):
        raise NotImplementedError("Metodo para validar informações de candidatura não implementado.")

    @abstractmethod
    def registrarCandidatura(self, candidaturaValidada):
        raise NotImplementedError("Metodo para registrar candidatura não implementado.")

    @abstractmethod
    def mostrarListaCandidatos(self, demanda):
        raise NotImplementedError("Metodo para mostrar lista de candidatos.")