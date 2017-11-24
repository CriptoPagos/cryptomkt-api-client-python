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
Clase que representa una orden de pago
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-11-24
"""
class Order :

    # atributos obligatorios para crear una orden
    to_receive = None # Monto a cobrar de la orden de pago. ARS soporta 2 decimales. CLP no soporta decimales. "." como separador de decimales.
    to_receive_currency = None # string requerido	Tipo de moneda con la cual recibirá el pago.
    payment_receiver = None # string requerido	Email del usuario o comercio que recibirá el pago. Debe estar registrado en CryptoMarket.

    # atributos opcionales para crear una orden
    external_id = None # ID externo. Permite asociar orden interna de comercio con orden de pago. Max. 64 caracteres.
    callback_url = None # Url a la cual se notificarán los cambios de estado de la orden. Max. 256 caracteres.
    error_url = None # Url a la cual se rediccionará en caso de error. Max. 256 caracteres.
    success_url = None # Url a la cual se rediccionará en caso de éxito. Max. 256 caracteres.
    refund_email = None # correo para hacer devolución en caso de problemas

    # atributos que se asignan a través del servicio web de CryptoMKT
    id = None # ID interno de la orden de pago
    status = None # Estado de la orden de pago
    deposit_address = None # Dirección de la orden de pago
    expected_currency = None # Tipo de moneda que espera la orden para ser aceptada
    expected_amount = None # Cantidad que espera la orden para ser aceptada
    created_at = None # Fecha de creación de la orden de pago
    updated_at = None # Fecha de actualización de la orden de pago
    server_at = None # cuando se creo la orden en el servidor
    qr = None # Url de la imagen QR de la orden de pago
    payment_url = None # Url de voucher de orden de pago
    obs = None # Observaciones
    remaining = None # tiempo que queda para hacer el pago
    token = None # token para url de pago en CryptoMKT

    _statuses = {
        -4: 'Pago múltiple',
        -3: 'Monto pagado no concuerda',
        -2: 'Falló conversión',
        -1: 'Expiró orden de pago',
         0: 'Esperando pago',
         1: 'Esperando bloque',
         2: 'Esperando procesamiento',
         3: 'Pago exitoso',
    } # Mensaje asociados al código de estado de la orden

    def getData (self) :
        data = {}
        cols = ['to_receive', 'to_receive_currency', 'payment_receiver', 'external_id', 'callback_url', 'error_url', 'success_url', 'refund_email']
        for col in cols :
            value = getattr(self, col, None)
            if value != None :
                data[col] = value
        return data

    def set (self, data) :
        for col in data :
            setattr(self, col, data[col])

    def getStatusMessage(self) :
        return self._statuses[self.status]
