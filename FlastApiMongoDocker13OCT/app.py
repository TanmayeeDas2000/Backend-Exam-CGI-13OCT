from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

customers = []

parser = reqparse.RequestParser()
parser.add_argument('customerName', type=str, required=True, help="Customer name cannot be blank!")
parser.add_argument('customerMobile', type=str, required=True, help="Mobile number must be provided!")
parser.add_argument('customerAddress', type=str, required=True, help="Address must be provided!")


class Customer:
    def _init_(self, customerId, customerName, customerMobile, customerAddress):
        self.customerId = customerId
        self.customerName = customerName
        self.customerMobile = customerMobile
        self.customerAddress = customerAddress


class CustomerServiceImpl:
    @staticmethod
    def add_customer(customer):
        customers.append(customer)
        return customer

    @staticmethod
    def get_all_customers():
        return customers


class CustomerResource(Resource):
    def get(self, customer_id=None):
        if customer_id:
            customer = next((c for c in customers if c.customerId == customer_id), None)
            if customer:
                return {
                    "customerId": customer.customerId,
                    "customerName": customer.customerName,
                    "customerMobile": customer.customerMobile,
                    "customerAddress": customer.customerAddress
                }, 200
            return {"message": "Customer not found"}, 404
        customer_data = []
        for customer in customers:
            customer_data.append({
                "customerId": customer.customerId,
                "customerName": customer.customerName,
                "customerMobile": customer.customerMobile,
                "customerAddress": customer.customerAddress
            })
        return customer_data, 200

    def post(self):
        args = parser.parse_args()

        customer = Customer(
            customerId = len(customers) + 1,
            customerName= args['customerName'],
            customerMobile= args['customerMobile'],
            customerAddress= args['customerAddress']
        )
        CustomerServiceImpl.add_customer(customer)
        return {
            "customerId": customer.customerId,
            "customerName": customer.customerName,
            "customerMobile": customer.customerMobile,
            "customerAddress": customer.customerAddress
        }, 201


api.add_resource(CustomerResource, '/customer', '/customer/<int:customer_id>')

if __name__ == "_main_":
    app.run(host="0.0.0.0", port=5001, debug=True)