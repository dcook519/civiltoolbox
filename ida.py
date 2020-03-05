### RUN IDA ANALYSIS VIA MATLAB ###
# Import Modules
import re # regex module
import matlab.engine # MatLab
from my_functions import fn_send_email # email function

# Load in user inputs and write to matlab workspace
ui = open("user_inputs.txt","r")
for x in ui:
    var_name = re.search(".*=", x)
    var_name = re.sub("=", "", var_name.group())
    var_val = re.search("=.*", x)
    var_val = re.sub("=", "", var_val.group())
    #print(var_name)
    globals()[var_name] = var_val

# Send Email acknowleding the start of the process
subject = "IDA Initiated"
body = "Your IDA has been initiated. You will recieve another email with the results from the process."
fn_send_email(user_email, subject, body)

# Send email to me acknowledging that someone started the process
bcc_email = "duco1061@colorado.edu"  # Confirmation to myself
body = "Someone has started an IDA process."
fn_send_email(bcc_email, subject, body)

# Call Matlab and Run IDA
eng = matlab.engine.start_matlab("-r 'cd ../Opensees'")
status = eng.driver_run_IDA(model_name, analysis_name, element, node, primary_nodes, story_ht, period)
#eng = matlab.engine.start_matlab("-desktop -r 'cd ../Opensees; driver_run_IDA(model_name, analysis_name, user_email, element, node, primary_nodes, story_ht)'")#
print(status)
eng.quit()

# Define completion message based on outcome of process
if 'IDA Failed' in status:
    subject = "IDA Failed"
    body = status
    fn_send_email(user_email, subject, body)
elif status == 'IDA Completed Successfully':
    subject = "IDA Finished"
    body = 'IDA Completed Successfully. Please find the summary results in the attached compressed file.'
    filename = "../Opensees/outputs/" + model_name + "/" + analysis_name + "/IDA/summary_data.zip"
    fn_send_email(user_email, subject, body, filename)
else:
    subject = "IDA Failed"
    body = "IDA failed due to an unknown issue."
    fn_send_email(user_email, subject, body)

# Send email to me acknowledging the process has finished
subject = 'Someones IDA has finished'
fn_send_email(bcc_email, subject, body)
    
