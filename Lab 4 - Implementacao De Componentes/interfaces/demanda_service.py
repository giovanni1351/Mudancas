
from abc import ABC, abstractmethod

class DemandaService(ABC):
    @abstractmethod
    def validarInformações(self, demanda):
        raise NotImplementedError("Metodo para validar informações de demanda não implementado.")

    @abstractmethod
    def registrarDemanda(self, demandaValidada):
        raise NotImplementedError("Metodo para registrar demanda não implementado.")

    @abstractmethod
    def buscarTodasDemandas(self):
        raise NotImplementedError("Metodo para buscar todas as demandas não implementado.")

    @abstractmethod
    def mostrarDetalheDemanda(self, demandaId):
        raise NotImplementedError("Metodo para mostrar detalhes da demanda não implementado.")

    @abstractmethod
    def associaCaminhoneiroDemanda(self, caminhoneiro,demanda):
        raise NotImplementedError("Metodo para associar caminhoneiro a demanda não implementado.")