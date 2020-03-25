from __future__ import print_function
import pickle
import os.path
import base64
import re # regex module
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from fn_run_ida import fn_run_ida # ida function

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    # Grab all messages new messages (unread) that have attachments with the correct subject line
    results = service.users().messages().list(userId='me',q='has:attachment subject:(run ida) is:unread').execute()
    messages = results.get('messages', [])

    # Go through and extract the subject value of each message
    if not messages:
        print('No messages found.')
    else:
        for message in messages:
            this_message = service.users().messages().get(userId='me', id=message['id']).execute()
            # Find the user email who sent message
            for header in this_message['payload']['headers']:
                if header['name'] == 'From':
                    email_search = re.search("<.*>", header['value'])
                    user_email = re.sub(">","",re.sub("<", "", email_search.group()))
                    print(user_email)

            # Go through the parts of this message and grab user inputs
            for part in this_message['payload']['parts']:
                # Parse Message Body for Analysis Inputs
                if part['mimeType'] == 'multipart/alternative':
                    for subpart in part['parts']:
                        if subpart['mimeType'] == 'text/plain':
                            ui = base64.urlsafe_b64decode(subpart['body']['data'].encode('UTF-8')).decode('ascii')
                            ui_lines = ui.splitlines()
                            for x in ui_lines:
                                var_name = re.search(".*=", x)
                                if var_name != None:
                                    var_name = re.sub("=", "", var_name.group())
                                    print(var_name)
                                    var_val = re.search("=.*", x)
                                    var_val = re.sub("=", "", var_val.group())
                                    print(var_val)
                                    globals()[var_name] = var_val
                                    
                # Get the attachment and save it to the analysis folder
                if part['filename']:
                    attach_id = part['body']['attachmentId']
                    attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attach_id).execute()
                    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                    fsp = os.path.sep
                    store_dir = ".." + fsp + "Opensees" + fsp + "outputs" + fsp + model_name + fsp + analysis_name + fsp + "opensees_data"
                    if not os.path.exists(store_dir):
                        os.makedirs(store_dir)
                    path = ''.join([store_dir, fsp, part['filename']])
                    print(path)
                    f = open(path, 'wb')
                    f.write(file_data)
                    f.close()
                
        
            # Run IDA
            fn_run_ida(user_email, model_name, analysis_name, element, node, primary_nodes, story_ht, period)

            # Mark this Email as read
            print(this_message['labelIds'])
            msg_labels = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
            mod_message = service.users().messages().modify(userId='me', id=message['id'], body=msg_labels).execute()
            print(mod_message['labelIds'])
                    

if __name__ == '__main__':
    main()
