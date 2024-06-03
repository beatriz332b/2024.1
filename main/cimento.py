def tipo_cimento_1():
    return "Você escolheu o Cimento Portland Comum (CPI)."

def tipo_cimento_2():
    return "Você escolheu o Cimento Portland Composto (CPII)."

def tipo_cimento_3():
    return "Você escolheu o Cimento Portland de Alto Forno (CPIII)."

def tipo_cimento_4():
    return "Você escolheu o Cimento Portland Pozolânico (CPII-Z)."

def tipo_cimento_5():
    return "Você escolheu o Cimento Portland de Alta Resistência Inicial (CPV-ARI)."

def tipo_invalido():
    return "Tipo de cimento inválido. Por favor, escolha um número de 1 a 5."

def switch_case(tipoCimento):
    switch = {
        1: tipo_cimento_1,
        2: tipo_cimento_2,
        3: tipo_cimento_3,
        4: tipo_cimento_4,
        5: tipo_cimento_5
    }
    return switch.get(tipoCimento, tipo_invalido)()

def define_tipo_cimento():
    print("Escolha um tipo de cimento:")
    print("1. Cimento Portland Comum (CPI)")
    print("2. Cimento Portland Composto (CPII)")
    print("3. Cimento Portland de Alto Forno (CPIII)")
    print("4. Cimento Portland Pozolânico (CPII-Z)")
    print("5. Cimento Portland de Alta Resistência Inicial (CPV-ARI)")

    escolha = int(input("Digite o número correspondente ao tipo de cimento: "))
    resultado = switch_case(escolha)
    print(resultado)
    return escolha
