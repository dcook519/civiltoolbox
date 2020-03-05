def fn_send_email(user_email, subject, body, filename="NA"):
    
    import email, smtplib, ssl # email modules
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "civiltoolbox@gmail.com"
    receiver_email = user_email
    password = "Xw3l44xNjM0l"
    context = ssl.create_default_context() # Create a secure SSL context

    # Send Email acknowleding the start of the process
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain")) # Add body to email

    if filename != "NA":
        with open(filename, "rb") as attachment: # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= summary_results.zip", #potential make filename an optional input
        )
        message.attach(part)

    text = message.as_string() # convert message to string

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    print("email was sent")
