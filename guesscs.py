CODES = ['UTF-8', 'UTF-16', 'GB18030', 'BIG5']
# UTF-8 BOM prefix
UTF_8_BOM = b'\xef\xbb\xbf'


def cs(s):
    """
    get file encoding or bytes charset

    :param s: file path or bytes data

    :return: encoding charset
    """

    if type(s) == str:
        with open(s, 'rb') as f:
            data = f.read()
    elif type(s) == bytes:
        data = s
    else:
        raise TypeError('unsupported argument type!')

    # iterator charset
    for code in CODES:
        try:
            data.decode(encoding=code)
            if 'UTF-8' == code and data.startswith(UTF_8_BOM):
                return 'UTF-8-SIG'
            return code
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError('unknown charset!')