from collections import defaultdict
from datetime import datetime, timedelta
from support_functions import start_day_of_week, date_validation, Customer, SiteVisit, Image, Order

# Declaration for list of keys or customer, site visit, image, order
key_list_customer = []
key_list_site_visit = []
key_list_image = []
key_list_order = []


# Creating instances of customer, site visit, image, order and load into in-memory Data Structure
def ingest(event, global_dictionary):
    global key_list_customer
    global key_list_site_visit
    global key_list_image
    global key_list_order

# Ingest Customer, Site Visit, Image and Order
# ---------------------------------------------
# Create class instance
# If the new id occurs, then create a dictionary with Corresponding Ids
# Load the instance to global_dictionary

# Customer

    if event['type'] == 'CUSTOMER':
        key = event['key']
        verb = event['verb']
        event_time = event['event_time']
        last_name = event['last_name']
        adr_city = event['adr_city']
        adr_state = event['adr_state']

        if key not in key_list_customer:
            key_list_customer.append(key)
            date_validation(event_time, key, key)
            customer_event = Customer(key, verb, event_time, last_name, adr_city, adr_state)

            if key not in global_dictionary:
                global_dictionary[key] = defaultdict(list)
                global_dictionary[key]['CUSTOMER'].append(customer_event)

# Site Visit
    if event['type'] == 'SITE_VISIT':
        key = event['key']
        verb = event['verb']
        event_time = event['event_time']
        customer_id = event['customer_id']
        tags = event['tags']

        if key not in key_list_site_visit:
            key_list_site_visit.append(key)
            date_validation(event_time, customer_id, key)
            site_visit_event = SiteVisit(key, verb, event_time, customer_id, tags)

            global_dictionary[customer_id]['SITE_VISIT'].append(site_visit_event)

# Image
    if event['type'] == 'IMAGE':
        key = event['key']
        verb = event['verb']
        event_time = event['event_time']
        customer_id = event['customer_id']
        camera_make = event['camera_make']
        camera_model = event['camera_model']

        if key not in key_list_image:
            key_list_image.append(key)
            date_validation(event_time, customer_id, key)
            image_event = Image(key, verb, event_time, customer_id, camera_make, camera_model)

            global_dictionary[customer_id]['IMAGE'].append(image_event)

# Order
    if event['type'] == 'ORDER':
        key = event['key']
        verb = event['verb']
        event_time = event['event_time']
        customer_id = event['customer_id']
        total_amount = event['total_amount']

        if key not in key_list_order:
            key_list_order.append(key)
            date_validation(event_time, customer_id, key)
            order_event = Order(key, verb, event_time, customer_id, total_amount)

            global_dictionary[customer_id]['ORDER'].append(order_event)


def topXSimpleLTVCustomers(x, global_dictionary):
    # Throws an exception if the number of customer mismatch
    try:
        if x > len(global_dictionary):
            raise ValueError
    except ValueError:
        print('Try a smaller value of X')
        exit(1)

    lifespan = 10
    # Dictionary to store LTV vales w.r.t. each customer
    customer_life_time_value = {}
    # Calculate the total order for each customer
    for customer_id in global_dictionary.keys():
        total_customer_exp = 0
        orders_list = global_dictionary[customer_id].get('ORDER', None)

        if orders_list is not None:
            for order in orders_list:
                total_customer_exp += float(order.total_amount.split(' ')[0].strip())

        no_of_site_visits = 0

        # Calculates the total number of weeks for a customer (By subtracting current week to start week)
        customer_start_day = global_dictionary[customer_id]['CUSTOMER'][0].event_time
        customer_start_week = start_day_of_week(customer_start_day)
        current_day = datetime.now().date()
        current_week = current_day - timedelta(days=current_day.weekday())
        no_of_weeks = int(abs((customer_start_week - current_week).days))/7

        # Calculate the number of site visit
        site_visits_list = global_dictionary[customer_id].get('SITE_VISIT', None)

        if site_visits_list is not None:
            no_of_site_visits = len(site_visits_list)

# Calculating LTV by (LTV= = 52 * Avg customer Expenditure * Life Span)
        if no_of_site_visits != 0:
            site_visits_per_week = no_of_site_visits/no_of_weeks
            customer_exp_per_visit = total_customer_exp/no_of_site_visits
            avg_customer_expenditure = customer_exp_per_visit * site_visits_per_week
            lifetime_value = 52 * avg_customer_expenditure * lifespan
        else:
            lifetime_value = 0

        customer_life_time_value[customer_id] = lifetime_value

    # Getting Top X Customers
    top_x_customers = sorted(customer_life_time_value.items(), key=lambda y: y[1], reverse=True)[:x]
    return top_x_customers
