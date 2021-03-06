# civiltoolbox
This is an email based tool that runs Opensees models through an Incremental Dynamic Analysis

## Run Tool
To run an IDA, send an email to civiltoolbox@gmail.com with the following information:

### Subject
'run ida'

### Body
Fill out the following information in the body of the email

model_name: name of the model (e.g. my_great_model, no spaces or special characters)<br />
analysis_name: sub name of the model (e.g run_1, no spaces or special characters)<br />
element: list of element ids to record (comma separated, no spaces)<br />
node: list of node ids to record (comma separated, no spaces)<br />
primary_nodes: list of node ids to measure drifts (one node per story, does not include ground floor, ie 5 story building should have 5 items, comma separated, no spaces)<br />
story_ht: list of story hts in whatever length units the model uses (one height per story, ie 5 story building should have 5 items, comma separated, no spaces)<br />
period: period of the building

Example:<br />
model_name=tayo<br />
analysis_name=analysis_3<br />
element=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,201,202,203,301,302,303,401,402,403,501,502,503,601,602,603,701,702,703,801,802,803<br />
node=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32<br />
primary_nodes=8,12,16,20,24,28,32<br />
story_ht=3750,3000,3000,3000,3000,3000,3000<br />
period=1.7<br />

### Attachment
Attach you model tcl file to the email and make sure to name it 'model.tcl'
