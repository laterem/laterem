ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def int2str(a, base):
    if a == 0:
        return '0'
    digits = ''
    while a:
        digits = ALPHABET[int(a % base)] + digits
        a //= base
    return digits