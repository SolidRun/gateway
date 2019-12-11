
import logging
import os
from time import time

from wirepas_gateway.utils import LoggerHelper
import wirepas_messaging
from wirepas_messaging.gateway.api.response import Response

from wirepas_messaging.gateway.api import (
    GatewayResultCode,
)


class MaerskGatewayRequestParser():
    """
    
    """    

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.epoch_ms = int(time() * 1000)


    def parse(self, payload):
        """

        """ 

        message = wirepas_messaging.gateway.GenericMessage()
        message.ParseFromString(payload)

        # Check all the optional fields     
        if not message.HasField('customer'):
            raise MaerskParsingException("Cannot parse customer field")
        customer = message.customer
        
        if not customer.HasField('request'):
            raise MaerskParsingException("Cannot parse request field")
        request = customer.request
        
        if not request.HasField('gateway_req'):
            raise MaerskParsingException("Cannot parse gateway_req field")
        gateway_req = request.gateway_req
        
        # Check TTL
        if self.epoch_ms > request.header.time_to_live_epoch_ms:
            raise MaerskParsingException("ttl expired - (gateway {} < request {})".format(self.epoch_ms, request.header.time_to_live_epoch_ms))
            
        # Parse request
        if gateway_req.HasField('gw_status_req'):
            return self.reply_gw_status_req(customer)
        
        else:
            raise MaerskParsingException("request not implemented")



    def reply_gw_status_req(self, customerReq = None):
        """

        """ 
        reply = wirepas_messaging.gateway.GenericMessage()
        req_id = customerReq.request.gateway_req.header.req_id if customerReq is not None else 0
        Response.add_gateway_status(reply, req_id)

        return reply.SerializeToString()
        
        
        
        
class MaerskParsingException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
    