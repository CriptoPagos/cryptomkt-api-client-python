# -*- coding: utf-8 -*-

"""
Cliente para servicios web de CryptoMKT
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""

# módulos que se usan en el cliente
import sys, requests, urllib, time, hashlib, hmac
from .Market import Market
from .Payment import Order

"""
Clase principal con el cliente de CryptoMKT
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-11-22
"""
class Client:

    _url = 'https://api.cryptomkt.com' # URL base para las llamadas a la API
    _version = 'v1' # Versión de la API con la que funciona este SDK
    default_limit = 100 # Límite por defecto a usar en consultas paginadas (se usa el máximo por defecto)
    api_key = None # API key para autenticación
    api_secret = None # API secret para autenticación
    response = None # Objeto con la respuesta del servicio web de CryptoMKT

    def __init__ (self, api_key = None, api_secret = None) :
        if api_key != None and api_secret != None :
            self.api_key = api_key
            self.api_secret = api_secret

    def getMarket(self, market) :
        return Market(market, self)

    def getMarkets (self) :
        url = self.createUrl('/market')
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el listado de mercados: ' + body['message'])
        return body['data']

    def getTicker (self, market = '') :
        url = self.createUrl('/ticker', {'market': market})
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el ticker del mercado ' + market + ': ' + body['message'])
        return body['data']

    def getBook (self, market, type, page = 0, limit = None) :
        if limit == None :
            limit = self.default_limit
        url = self.createUrl('/book', {'market': market, 'type': type, 'page': page, 'limit': limit})
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el libro de ' + type + ' del mercado ' + market + ': ' + body['message'])
        return body['data']

    def getTrades (self, market, start = None, end = None, page = 0, limit = None) :
        if start == None :
            start = time.strftime('%Y-%m-%d')
        if end == None :
            end = start
        if limit == None :
            limit = self.default_limit
        url = self.createUrl('/trades', {'market': market, 'start': start, 'end': end, 'page': page, 'limit': limit})
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener los intercambios del mercado ' + market + ': ' + body['message'])
        return body['data']

    def getActiveOrders (self, market, page = 0, limit = None) :
        if limit == None :
            limit = self.default_limit
        url = self.createUrl('/orders/active', {'market': market, 'page': page, 'limit': limit})
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener las ordenes activas del mercado ' + market + ': ' + body['message'])
        return body['data']

    def getExecutedOrders (self, market, page = 0, limit = None) :
        if limit == None :
            limit = self.default_limit
        url = self.createUrl('/orders/executed', {'market': market, 'page': page, 'limit': limit})
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener las ordenes activas del mercado ' + market + ': ' + body['message'])
        return body['data']

    def createOrder (self, market, type, amount, price) :
        url = self.createUrl('/orders/create')
        self.response = self.consume(url, {'market': market, 'type': type, 'amount': amount, 'price': price})
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible crear la orden en el mercado ' + market + ': ' + body['message'])
        return body['data']

    def getOrder (self, id) :
        url = self.createUrl('/orders/status', {'id': id})
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el balance de las billeteras: ' + body['message'])
        return body['data']

    def cancelOrder (self, id) :
        url = self.createUrl('/orders/cancel')
        self.response = self.consume(url, {'id': id})
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible cancelar la orden ' + id + ' en el mercado: ' + body['message'])
        return body['data']

    def getBalance (self) :
        url = self.createUrl('/balance')
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el balance de las billeteras: ' + body['message'])
        return body['data']

    def createPaymentOrder (self, PaymentOrder) :
        url = self.createUrl('/payment/new_order')
        self.response = self.consume(url, PaymentOrder.getData())
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible realizar consulta a CryptoMKT: ' + body['message'])
        PaymentOrder.set(body['data'])
        return PaymentOrder

    def getPaymentOrder (self, id) :
        url = self.createUrl('/payment/status', {'id': id})
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener la orden de pago ' + id + ' desde CryptoMKT: ' + body['message'])
        PaymentOrder = Order()
        PaymentOrder.set(body['data'])
        return PaymentOrder

    def createUrl (self, recurso, params = None) :
        url = self._url + '/' + self._version + recurso
        if params == None :
            return url
        if sys.version_info[0] == 2 :
            query = urllib.urlencode(params)
        else :
            query = urllib.parse.urlencode(params)
        return '{0}?{1}'.format(url, query)

    def consume (self, url, data = None) :
        # preparar cabeceras
        if self.api_key != None and self.api_secret != None :
            timestamp = int(time.time())
            path = url.replace(self._url, '').split('?')[0]
            msg = str(timestamp) + path
            if data :
                aux = [(k,data[k]) for k in sorted(data.keys())]
                for var, val in aux :
                    msg += str(val)
            if sys.version_info[0] == 2 :
                hashed = hmac.new(self.api_secret, msg, hashlib.sha384)
            else :
                hashed = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(msg, 'utf-8'), hashlib.sha384)
            headers = {
                'X-MKT-APIKEY': self.api_key,
                'X-MKT-SIGNATURE': hashed.hexdigest(),
                'X-MKT-TIMESTAMP': str(timestamp)
            }
        else :
            headers = {}
        # método POST
        if data :
            return requests.post(url, data=data, headers=headers)
        # método GET
        else :
            return requests.get(url, headers=headers)
