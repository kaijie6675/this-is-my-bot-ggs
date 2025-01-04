def calculate_profit_factor(gross_profit, gross_loss):
    return gross_profit / gross_loss if gross_loss != 0 else float('inf')

def calculate_win_rate(total_trades, winning_trades):
    return winning_trades / total_trades if total_trades != 0 else 0

def calculate_max_drawdown(net_worths):
    max_drawdown = 0
    peak = net_worths[0]
    for net_worth in net_worths:
        if net_worth > peak:
            peak = net_worth
        drawdown = peak - net_worth
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    return max_drawdown

def calculate_sharpe_ratio(returns, risk_free_rate=0):
    excess_returns = returns - risk_free_rate
    return excess_returns.mean() / excess_returns.std() if returns.std() != 0 else float('inf')