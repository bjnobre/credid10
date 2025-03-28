def calcular_tabela_price(principal, taxa_mensal, meses):
    """
    Calcula a tabela de amortização utilizando o método Price.

    Parâmetros:
      principal (float): Valor do empréstimo.
      taxa_mensal (float): Taxa de juros mensal em decimal (ex: 0.15 para 15%).
      meses (int): Número de pagamentos mensais (deve ser entre 1 e 8).

    Retorna:
      list: Uma lista de dicionários representando a tabela de amortização.
    """
    if meses < 1 or meses > 8:
        raise ValueError("O número de meses deve estar entre 1 e 8.")
    
    # Calcula o valor da parcela fixa
    parcela = principal * (taxa_mensal * (1 + taxa_mensal) ** meses) / ((1 + taxa_mensal) ** meses - 1)
    
    tabela = []
    saldo_devedor = principal

    for mes in range(1, meses + 1):
        juros = saldo_devedor * taxa_mensal
        amortizacao = parcela - juros
        saldo_devedor -= amortizacao
        
        tabela.append({
            "mes": mes,
            "parcela": round(parcela, 2),
            "juros": round(juros, 2),
            "amortizacao": round(amortizacao, 2),
            "saldo_devedor": round(max(saldo_devedor, 0), 2)
        })
    
    return tabela
