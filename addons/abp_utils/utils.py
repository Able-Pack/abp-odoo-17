def format_currency_amount(amount, currency_id):
        pre = currency_id.position == 'before'
        symbol = u'{symbol}'.format(symbol=currency_id.symbol or '')
        # Format amount to two decimal places
        formatted_amount = '{:,.2f}'.format(amount)
        return u'{pre}{0}{post}'.format(formatted_amount, pre=symbol if pre else '', post=symbol if not pre else '')
