
from odoo import models
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit='product.product'

    def GtExportSingleProductStock(self):
        for instance_id in self.magento_instance_ids:
            instance_id.generate_token()
            token=instance_id.token
            token=token.replace('"'," ")
            auth_token="Bearer "+token.strip()
            auth_token=auth_token.replace("'",'"')
            headers = {
                'authorization':auth_token,
                'content-type': "application/json",
                'cache-control': "no-cache",
            }
            if self.qty_available >= 0.00:
                vals = { "sourceItems": []}
                for store in self.store_ids:
                    quantity = 0
                    for location in store.stock_location_ids:
                        quantity += self.env['stock.quant']._get_available_quantity(self,location)
                    data = {
                    "sku": self.default_code,
                    "source_code": store.source_code,
                    "quantity": quantity,
                    "status": 1
                    }
                    vals['sourceItems'].append(data)
                payload = str(vals) 
                payload=payload.replace("'",'"')     
                payload=str(payload)
                if self.store_ids and self.store_ids[0].code:
                    store_code = self.store_ids[0].code
                else:
                    store_code = "default2"
                url=instance_id.location+"rest/"+store_code+"/V1/inventory/source-items"
                response = requests.request("POST",url, data=payload, headers=headers)
                if str(response.status_code)=="200":
                    each_response=json.loads(response.text)
                _logger.info(response.text)
        return True