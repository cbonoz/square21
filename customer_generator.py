import uuid

class CustomerGenerator:
    
    def __init__(self, client):
        self.client = client
        self.customers_api = client.customers
    
    def create_customer(self, **kwargs):
        print('create_customer', kwargs)
        result = self.customers_api.create_customer(body=kwargs)

        if result.is_success():
            print(result.body)
            return result.body.get('customer', {})
        elif result.is_error():
            print(result.errors)

        return None