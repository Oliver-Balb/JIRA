from datetime import datetime

def convert_name_format(input_string):
    
    try:            
        # Split the input string by comma and space
        parts = input_string.split(', ')
        
        # Extract lastname and firstname
        lastname = parts[0].strip()
        firstname = parts[1].split(' (')[0].strip()
        department = parts[1].split('(')[1][:-1].strip()

    except:
        lastname = input_string
        firstname = None
        department = None
    
    return firstname, lastname, department

# Example usage
input_string =  "Müller ,   Franz-Walter  Dieter    (FDO3)"
firstname, lastname, department = convert_name_format(input_string)
print(firstname)  # Output: John Doe
print(lastname)
print(department)





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


