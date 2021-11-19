import uuid

class OrderGenerator:
    
    def __init__(self, client):
        self.client = client
        self.orders_api = client.orders
        
    def create_test_order(self, item_name, usd_price, count, location_id, customer_id=None):
        # https://github.com/square/square-python-sdk/blob/master/doc/models/order.md
        body = {}
        
        price_cents = int(usd_price*100)
        
        # Can extend for additional items
        line_items = [{
            "name": item_name,
            "quantity": str(count),
            "base_price_money": {'amount': price_cents, 'currency': 'USD'} # Price expected in cents.
        }]
        
        # Sample data
        body['order'] = {}
        body['location_id'] = location_id
        body['order']['location_id'] = location_id
        body['order']['source'] = {}
        body['order']['line_items'] = []
        if customer_id:
            body['order']['customer_id'] = customer_id

        
        for item in line_items:
            body['order']['line_items'].append(item)

        return body
        

        
    def create_random_orders(self, name, prices, counts, location_id, customer_id=None):
        assert len(prices) == len(counts)
        n = len(prices)
        
        for i in range(n):
            line_items = []
            idem_key = str(uuid.uuid4())
            body = self.create_test_order(name, prices[i], counts[i], location_id, customer_id)
            body['idempotency_key'] = idem_key
            print('creating order', body)
            result = self.orders_api.create_order(body=body, location_id=location_id)

            if result.is_success():
                print(f"Created order {i} with {len(line_items)} items")
                print(result.body)
            elif result.is_error():
                print(result.errors)
