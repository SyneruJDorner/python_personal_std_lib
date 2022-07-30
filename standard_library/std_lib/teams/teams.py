#pip install pymsteams

def send_feedback(msg):
    webhook_url = "ENTER THE WEB HOOK URL HERE"

    if webhook_url == "ENTER THE WEB HOOK URL HERE":
        print("Please enter the webhook url in the code.")
        return

    import pymsteams
    myTeamsMessage = pymsteams.connectorcard(webhook_url)
    myTeamsMessage.text(msg)
    myTeamsMessage.send()
    pass