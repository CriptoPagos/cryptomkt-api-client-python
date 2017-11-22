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

"""
Clase que representa un mercado genérico de CryptoMKT
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-11-22
"""
class Market :

    _market = None # mercado para el cual se instanció el objeto
    client = None # Objeto que representa el cliente de la conexión a CryptoMKT

    def __init__ (self, market, Client = None) :
        self._market = market
        if Client != None :
            self.client = Client

    def getTicker (self) :
        return self.client.getTicker(self._market)

    def getBuyBook (self, page = 0, limit = None) :
        return self.client.getBook(self._market, 'buy', page, limit)

    def getSellBook (self, page = 0, limit = None) :
        return self.client.getBook(self._market, 'sell', page, limit)

    def getTrades (self, start = None, end = None, page = 0, limit = None) :
        return self.client.getTrades(self._market, start, end, page, limit)

    def getActiveOrders (self, page = 0, limit = None) :
        return self.client.getActiveOrders(self._market, page, limit)

    def getExecutedOrders (self, page = 0, limit = None) :
        return self.client.getExecutedOrders(self._market, page, limit)

    def createBuyOrder (self, amount, price) :
        return self.client.createOrder(self._market, 'buy', amount, price)

    def createSellOrder (self, amount, price) :
        return self.client.createOrder(self._market, 'sell', amount, price)
