import requests
import re

def get_response(date):
    url = 'https://gee.bccr.fi.cr/indicadoreseconomicos/Cuadros/frmVerCatCuadro.aspx?CodCuadro=400&Idioma=1&FecInicial={0}&FecFinal={0}&Filtro=0'.format(date)
    response = requests.get(url)
    response = response.content.decode('utf-8')
    return response

def get_exchange_rates(decoded_response):
    regexp = re.compile(' (\d*,\d*)')
    exchange_rates = regexp.findall(decoded_response)
    print('Tipos de cambio:')
    print('Compra: {0}'.format(exchange_rates[0]))
    print('Venta: {0}'.format(exchange_rates[1]))

if __name__ == '__main__':
    get_exchange_rates(get_response('2020/11/29'))
