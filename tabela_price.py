def calculate_schedule(principal, monthly_rate, months):
    """
    Calculate the amortization schedule using the Price Table method.
    
    Parameters:
      principal (float): The loan amount.
      monthly_rate (float): The monthly interest rate as a decimal (e.g., 0.15 for 15%).
      months (int): Number of monthly payments (must be between 1 and 8).
    
    Returns:
      list: A list of dictionaries representing the schedule.
    """
    if months < 1 or months > 8:
        raise ValueError("The number of months must be between 1 and 8.")
    
    # Calculate fixed monthly payment:
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    
    schedule = []
    remaining_balance = principal

    for month in range(1, months + 1):
        interest = remaining_balance * monthly_rate
        amortization = payment - interest
        remaining_balance -= amortization
        
        schedule.append({
            "month": month,
            "payment": round(payment, 2),
            "interest": round(interest, 2),
            "amortization": round(amortization, 2),
            "remaining_balance": round(max(remaining_balance, 0), 2)
        })
    
    return schedule
