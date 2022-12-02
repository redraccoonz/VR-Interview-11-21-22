import csv
from collections import defaultdict
from itertools import combinations

datacenter_to_user_id = defaultdict(set) # Maps datacenter names to list of user ids that satisfy conditions
datacenters = set() # Set of unique datacenters
users = set() # Set of unique user ids

# Creates a map of datacenter to list of users who experience latency below threshold
# Arguments:
#   data_file:              File name of dataset in .csv format
#   latency:                latency threshold
#   datacenter_to_user_id:  map of datacenter to list of user ids
#   datacenter:             set of datacenters
#   users:                  set of user ids
def get_latency_data(data_file, latency, datacenter_to_user_id, datacenters, users):
    with open('BigBox.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=',', quotechar='"')
        for row in reader:
            datacenter = row['action']
            user_id = row['anon_user_id']
            datacenters.add(datacenter)
            users.add(user_id)
            if int(row['value']) < latency:
                datacenter_to_user_id[datacenter].add(user_id)

# Finds the group of datacenters maximizing the number of users 
# Arguments:
#   datacenter_to_user_id:  map of datacenter to list of user ids
#   datacenter_list:        list of datacenters
#   group_size:             size of datacenter group
# Returns:
#   max_user_count:         Count of users in group of datacenters that maximize the number of users
#   best_datacenter_group:  Tuple of datacenters maximizing the number of users
def find_max_coverage(datacenter_to_user_id, datacenter_list, group_size):
    max_user_count = 0
    best_datacenter_group = None
    for datacenter_group in combinations(datacenter_list, group_size):
        user_set = set()
        for datacenter in datacenter_group:
            user_set = user_set.union(datacenter_to_user_id[datacenter])
        user_count = len(user_set)
        if user_count > max_user_count:
            max_user_count = user_count
            best_datacenter_group = datacenter_group
    return max_user_count, best_datacenter_group
             
# Create map of datacenter to list of user ids that experience < 150ms latency             
get_latency_data("BigBox.csv", 150, datacenter_to_user_id, datacenters, users)
datacenter_list = list(datacenters)

# Answers 1)
max_coverage, best_coverage_pair = find_max_coverage(datacenter_to_user_id, datacenter_list, 2)
print(max_coverage, best_coverage_pair)

# Answers 2)
max_coverage, best_coverage_triple = find_max_coverage(datacenter_to_user_id, datacenter_list, 3)
print(max_coverage, best_coverage_triple)

# Create map of datacenter to list of user ids that experience < 250ms latency
# Superset of 150ms map so no need to clear previous map beforehand  
get_latency_data("BigBox.csv", 250, datacenter_to_user_id, datacenters, users)

# Answers 1a)
max_coverage, best_coverage_pair = find_max_coverage(datacenter_to_user_id, datacenter_list, 2)
print(max_coverage, best_coverage_pair)

# Answers 2a)
max_coverage, best_coverage_triple = find_max_coverage(datacenter_to_user_id, datacenter_list, 3)
print(max_coverage, best_coverage_triple)

