# Test call a function
from my_functions import fn_send_email

user_email = "duco1061@colorado.edu"
subject = "IDA Initiated"
body = "Your IDA has been initiated. You will recieve another email with the results from the process."
fn_send_email(user_email, subject, body)
