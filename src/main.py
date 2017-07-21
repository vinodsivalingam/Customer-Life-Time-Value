from main_functions import ingest, topXSimpleLTVCustomers
import sys
import simplejson as json
from support_functions import display_output

# Main Function
# Takes 2 arguments : (i) Top X customer with highest Lifetime Value (ii) Input File- data
x = int(sys.argv[1])
files = sys.argv[2: len(sys.argv)]

global_dictionary = {}

# Input file is in JSON format

for file in files:
    with open(file) as json_file:
        json_object = json.load(json_file)

# Ingest takes two arguments events and update data
    for event in json_object:
        ingest(event, global_dictionary)

# Function returns the Top x customer with highest LVD on the global dictionary
top_X_LTV_customers = topXSimpleLTVCustomers(x, global_dictionary)

# Functions print the top x LTV customers
display_output(top_X_LTV_customers, global_dictionary)
