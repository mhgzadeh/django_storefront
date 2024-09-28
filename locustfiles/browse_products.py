from random import randint

from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(min_wait=1, max_wait=5)

    @task(2)
    def view_products(self):
        print('product list')
        collection_id = randint(2, 6)
        self.client.get(f"/store/products/?collection_id={collection_id}", name='store/products')

    @task(4)
    def view_product(self):
        print('product details')
        product_id = randint(1, 1001)
        self.client.get(f"/store/products/{product_id}", name='store/product/:id')

    @task(1)
    def add_to_cart(self):
        print('add cart')
        product_id = randint(1, 10)
        self.client.get(f"/store/carts/{self.cart_id}/items/", name='store/carts/items',
                        json={'product_id': product_id, 'quantity': 1})

    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['uuid']
