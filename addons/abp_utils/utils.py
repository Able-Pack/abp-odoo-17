from itertools import islice

def format_currency_amount(amount, currency_id):
	# Format amount to two decimal places
    formatted_amount = '{:,.2f}'.format(amount)
    if not currency_id:
        return formatted_amount
    
    pre = currency_id.position == 'before'
    symbol = u'{symbol}'.format(symbol=currency_id.symbol or '')
    return u'{pre} {0}{post}'.format(formatted_amount, pre=symbol if pre else '', post=symbol if not pre else '')

def chunks(iterable, size):
        it = iter(iterable)
        return iter(lambda: tuple(islice(it, size)), ())