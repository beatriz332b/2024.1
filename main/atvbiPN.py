from concreto import Concreto
from cimento import define_tipo_cimento

def main():
    # Solicita ao usuário para inserir os dados
    resistencia_alvo = float(input("Digite a resistência desejada do concreto (em MPa): "))
    proporcao_cimento = float(input("Digite a proporção de cimento: "))

    # Define o tipo de cimento
    tipo_cimento_escolhido = define_tipo_cimento()
    print(tipo_cimento_escolhido)

    proporcao_areia = float(input("Digite a proporção de areia: "))
    proporcao_pedra = float(input("Digite a proporção de pedra: "))

    # Cria uma instância da classe Concreto
    concreto = Concreto(resistencia_alvo, proporcao_cimento, proporcao_areia, proporcao_pedra)

    # Calcula os ingredientes do concreto com base nos dados fornecidos pelo usuário
    cimento, areia, pedra = concreto.calcular_ingredientes()

    # Exibe os resultados
    print("Quantidade de cimento necessária:", cimento, "kg")
    print("Quantidade de areia necessária:", areia, "kg")
    print("Quantidade de pedra necessária:", pedra, "kg")

    # Exemplo de cálculo de área de aço
    tipo_cimento = 'CP-II'  # Usuário seleciona o tipo de cimento
    propriedades_cimento = Concreto.selecionar_cimento(tipo_cimento)

    Md = 20000  # Momento fletor em N.cm
    fck = propriedades_cimento['fck']  # Resistência característica do concreto em MPa
    fyk = 500  # Resistência característica do aço em MPa
    d = 50  # Altura útil da seção em cm
    bw = 20  # Largura da viga em cm

    # Cálculo da área de aço necessária
    area_aco = Concreto.calcular_area_aco(Md, fck, fyk, d, bw)
    print(f"Tipo de Cimento: {tipo_cimento} - {propriedades_cimento['descricao']}")
    print(f"A área de aço necessária é: {area_aco:.2f} cm²")

if __name__ == "__main__":
    main()
