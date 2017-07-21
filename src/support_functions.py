# This modules  (i) defines the list of Events (Class)- Customer, SiteVisit, Image and Order
#               (ii) Performs Date validation
#               (iii) Prints the final list of top X LTV Customers
from datetime import datetime, timedelta

# The list of Events (Class)- Customer, SiteVisit, Image and Order


class Customer:
    def __init__(self, key, verb, event_time, last_name, adr_city, adr_state):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.last_name = last_name
        self.adr_city = adr_city
        self.adr_state = adr_state


class SiteVisit:
    def __init__(self, key, verb, event_time, customer_id, tags):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.customer_id = customer_id
        self.tags = tags


class Image:
    def __init__(self, key, verb, event_time, customer_id, camera_make, camera_model):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.customer_id = customer_id
        self.camera_make = camera_make
        self.camera_model = camera_model


class Order:
    def __init__(self, key, verb, event_time, customer_id, total_amount):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.customer_id = customer_id
        self.total_amount = total_amount


# get the start day of a customer's start week
def start_day_of_week(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d:%H:%M:%S.%fZ').date()
    start = dt - timedelta(days=dt.weekday())
    return start


# Function definition for date validation
def date_validation(date_str, customer_id, key):
    try:
        datetime.strptime(date_str, '%Y-%m-%d:%H:%M:%S.%fZ')
    except ValueError:
        print("Error: Incorrect date or format for customer:", customer_id, 'in event key:', key)
        exit(1)


# Function definition for printing in tabular format
def display_output(top_X_LTV_customers, global_dictionary):
    x = len(top_X_LTV_customers)
    rank = 0
    for pair in top_X_LTV_customers:
        rank += 1
        customer_id = pair[0]
        life_time_value = format(pair[1], '.2f')
        last_name = global_dictionary[customer_id]['CUSTOMER'][0].last_name
        print(rank, '    ', customer_id, '    ', last_name,  '    ', '$'+life_time_value)
