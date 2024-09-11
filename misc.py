from datetime import datetime


# Original date string
date_str = "2024-10-31"
print(type(date_str))

# Convert the string to a datetime object
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
print(date_obj)
print(type(date_obj))

# Convert the datetime object to the desired format
formatted_date_str = date_obj.strftime("%d.%m.%Y")

print(formatted_date_str)  # Output: 31.10.2024

# Get the current date and time
now = datetime.now()

# Format the datetime stamp
timestamp = now.strftime("%Y%m%d-%H%M%S")

print(timestamp)