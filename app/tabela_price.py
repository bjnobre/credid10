import math
import numpy_financial as npf

def calcular_tabela_price(principal: float, taxa_mensal: float, meses: int) -> list:
    """
    Calcula a tabela de amortização utilizando o método Price, 
    recalculando os valores de juros e amortização com base no valor da parcela arredondada.
    
    A parcela é inicialmente calculada pela fórmula Price e, em seguida, arredondada para o
    próximo múltiplo de 5. Em cada pagamento, os juros são recalculados com base no saldo devedor,
    e a amortização é definida como (parcela - juros). No último pagamento, a parcela é ajustada para 
    quitar o saldo devedor exatamente, evitando inconsistências na apresentação dos valores.
    
    Parâmetros:
      principal (float): Valor do empréstimo. Deve ser maior que zero.
      taxa_mensal (float): Taxa de juros mensal em decimal (ex: 0.15 para 15%). Deve ser >= 0.
      meses (int): Número de pagamentos mensais (deve estar entre 1 e 8).
      
    Retorna:
      list: Uma lista de dicionários representando a tabela de amortização.
            Cada dicionário contém:
              - "mes": número do mês
              - "parcela": valor da parcela (arredondada para o próximo múltiplo de 5, 
                           exceto possivelmente no último pagamento)
              - "juros": valor dos juros do mês
              - "amortizacao": valor da amortização do mês
              - "saldo_devedor": saldo devedor após o pagamento
    """
    if principal <= 0:
        raise ValueError("O valor do empréstimo deve ser maior que zero.")
    if taxa_mensal < 0:
        raise ValueError("A taxa de juros não pode ser negativa.")
    if meses < 1 or meses > 8:
        raise ValueError("O número de meses deve estar entre 1 e 8.")
    
    tabela = []
    saldo_devedor = principal

    # Calcula a parcela base usando a fórmula Price ou divisão simples se taxa for zero.
    if taxa_mensal == 0:
        parcela_calculada = principal / meses
    else:
        # npf.pmt retorna um valor negativo, então usamos o valor absoluto.
        parcela_calculada = -npf.pmt(taxa_mensal, meses, principal)

    # Arredonda a parcela para o próximo múltiplo de 5
    parcela_arredondada = math.ceil(parcela_calculada / 5) * 5

    # Se a taxa original não era zero, recalcula a taxa mensal (taxa_nova)
    # para que npf.pmt(taxa_nova, meses, principal) = parcela_arredondado.
    if taxa_mensal != 0:
        low, high = 0, 1  # suposição inicial: taxa entre 0% e 100% ao mês
        # Ajusta "high" se necessário
        while -npf.pmt(high, meses, principal) < parcela_arredondada:
            high *= 2
        # Realiza busca binária para encontrar a taxa que produz o pagamento desejado
        for _ in range(100):  # 100 iterações garantem precisão suficiente
            mid = (low + high) / 2
            pagamento = -npf.pmt(mid, meses, principal)
            if pagamento > parcela_arredondada:
                high = mid
            else:
                low = mid
        taxa_mensal = (low + high) / 2
    else:
      taxa_mensal = 0

    for mes in range(1, meses + 1):
        # Recalcula os juros com base no saldo atual
        juros = saldo_devedor * taxa_mensal
        
        if mes == meses:
            # No último mês, ajusta a parcela para quitar exatamente o saldo devedor.
            parcela_utilizada = saldo_devedor + juros
            amortizacao = parcela_utilizada - juros
            saldo_devedor = 0
        else:
            parcela_utilizada = parcela_arredondada
            amortizacao = parcela_utilizada - juros
            saldo_devedor -= amortizacao
            # Se o saldo ficar negativo por conta de arredondamento, ajusta-o para zero.
            if saldo_devedor < 0:
                amortizacao += saldo_devedor
                saldo_devedor = 0
        
        tabela.append({
            "mes": mes,
            "parcela": round(parcela_utilizada, 2),
            "juros": round(juros, 2),
            "amortizacao": round(amortizacao, 2),
            "saldo_devedor": round(saldo_devedor, 2)
        })
    
    return tabela
