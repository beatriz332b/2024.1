import numpy as np

class Concreto:
    def __init__(self, resistencia_desejada, proporcao_cimento, proporcao_areia, proporcao_pedra):
        self.resistencia_desejada = resistencia_desejada
        self.proporcao_cimento = proporcao_cimento
        self.proporcao_areia = proporcao_areia
        self.proporcao_pedra = proporcao_pedra

    def calcular_ingredientes(self):
        quantidade_cimento = self.resistencia_desejada * self.proporcao_cimento
        quantidade_areia = self.resistencia_desejada * self.proporcao_areia
        quantidade_pedra = self.resistencia_desejada * self.proporcao_pedra

        return quantidade_cimento, quantidade_areia, quantidade_pedra

    @staticmethod
    def selecionar_cimento(tipo_cimento):
        cimentos = {
            'CP-I': {'fck': 25, 'descricao': 'Cimento Portland Comum'},
            'CP-II': {'fck': 32, 'descricao': 'Cimento Portland Composto'},
            'CP-III': {'fck': 40, 'descricao': 'Cimento Portland de Alto Forno'}
        }
        return cimentos.get(tipo_cimento, {'fck': 25, 'descricao': 'Cimento Padrão'})

    @staticmethod
    def calcular_area_aco(Md, fck, fyk, d, bw):
        fyd = fyk / 1.15  # Tensão de escoamento do aço
        fcd = fck / 1.4   # Tensão de compressão do concreto
        z = 0.9 * d       # Braço de alavanca
        As = Md / (0.87 * fyd * z)  # Área de aço necessária
        return As