def bytes2human(n, format="%(value)i%(symbol)s"):
	symbols = ('B', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb')
	prefix = {}
	for i, s in enumerate(symbols[1:]):
		prefix[s] = 1 << (i+1)*10
	for symbol in reversed(symbols[1:]):
		if n >= prefix[symbol]:
			value = float(n) / prefix[symbol]
			return format % locals()
	return format % dict(symbol=symbols[0], value=n)

def human2bytes(s):
	symbols = ('B', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb')
	letter = s[-1:].strip().upper()
	num = s[:-1]
	assert num.isdigit() and letter in symbols
	num = float(num)
	prefix = {symbols[0]:1}
	for i, s in enumerate(symbols[1:]):
		prefix[s] = 1 << (i+1)*10
	return int(num * prefix[letter])