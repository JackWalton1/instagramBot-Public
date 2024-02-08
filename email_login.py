import imaplib
import email

def get_code_from_email(username, password):
    # creata a imap object
    imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    
    # login
    result = imap.login(username, password)
    
    # Use "[Gmail]/Sent Mails" for fetching
    # mails from Sent Mails. 
    imap.select('"[Gmail]/All Mail"', readonly = True) 
    
    response, messages = imap.search(None, 'UnSeen')
    messages = messages[0].split()
    
    # take it from last
    latest = int(messages[-1])
    
    # take it from start
    oldest = int(messages[0])

    codes = []
    
    for i in range(latest, latest-20, -1):
        # fetch
        res, msg = imap.fetch(str(i), "(RFC822)")
        
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                # print required information
                # print(msg["Date"])
                sender = msg["From"]
                # print(msg["From"])

                subject = msg["Subject"]
                # print(msg["Subject"])
        
        for part in msg.walk():
            if part.get_content_type() == "text/html" and sender == '"Instagram" <security@mail.instagram.com>' and subject == "Verify your account":
                # get text or plain data
                body = part.get_payload(decode = True)
                html_soup = body.decode("UTF-8")
                # print(f'Body: {body.decode("UTF-8")}', )
                start_index = html_soup.find('size="6"')
                if (start_index) >= 0:
                    end_index = start_index + len('size="6"')
                    code_size = 6
                    code = html_soup[end_index+1:end_index+code_size+1]
                    codes.append(code)

                    # print("Here is the code: ", code)
    return codes
        

codes = get_code_from_email({username}, {password})
print("\nEmail_login.py returns: ", codes)
