import urllib, httplib


'''
This method will send an event to the maker channel in IFTTT to link to any other service
Required Arguments: makerEvent (string) - name given when enabling the service
                    key (string)        - key that is found in the settings of the maker
                                          service https://ifttt.com/services/maker/settings
Optional Arguments: value1 (string)     - variable to pass to the maker service
                    value2 (string)     - variable to pass to the maker service
                    value3 (string)     - variable to pass to the maker service
            Output: success (boolean)
'''
def sendMakerChannel(makerEvent, key, value1='', value2='', value3=''):
    # Form the url for IFTTT maker channel
    url = "https://maker.ifttt.com/trigger/" + makerEvent + "/with/key/" + key
    try:
        # Format the data payload and send POST request
        data = urllib.urlencode({ "value1": value1 , "value2": value2, "value3": value3})
        request = urllib.urlopen(url, data)
        return True
    except:
        return False

'''
This method will send a pushover message, written as a standard function but probably should change
to use keyword arguements and devices to be added as a list
Required Arguments: userKey (string)   - The main user key found on home page
                    apiToken (string)  - This the API key for a particular application
                    message (string)   - The main text for the notification
Optional Arguments: device (string)    - your user's device name to send the message directly to that device
                    title (string)     - your message's title, otherwise your app's name is used
                    url (string)       - a supplementary URL to show with your message
                    url_title (string) - a title for your supplementary URL, otherwise just the URL is shown
                    sound (string)     - the name of one of the sounds supported by device clients to override
                                         the user's default sound choice
'''
def sendPushover(userKey, apiToken, message,
                 device='', title='', url='', url_title='', sound=''):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.urlencode({
                     "token": pushoverApiToken,
                     "user": pushoverUserKey,
                     "message": message,
                     "device": device,
                     "title": title,
                     "url": url,
                     "url_title": url_title,
                     "sound": sound,
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    return conn.getresponse()

