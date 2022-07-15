
mes = 'a'* 1
bytes_mes = bytes(mes, 'utf-8')

with open('file_to_send.txt', 'wb') as f:
    f.write(bytes_mes)
