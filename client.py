import urllib.request
import urllib.parse
import hashlib
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#google credentials
#it wont work on your computer due to the lack of my credential informations
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

def generate_screenshot_api_url(customer_key, secret_phrase, options):
  api_url = 'https://api.screenshotmachine.com/?key=' + customer_key
  if secret_phrase:
    api_url = api_url + '&hash=' + hashlib.md5((options.get('url') + secret_phrase).encode('utf-8')).hexdigest()
  api_url = api_url + '&' + urllib.parse.urlencode(options)
  return api_url;

#website array
websites=[1,'iFunded','https://ifunded.de/en/'],[2,'Property Partner','https://www.propertypartner.co'],[3,'Property Moose','https://propertymoose.co.uk'],[4,'Homegrown','https://www.homegrown.co.uk'],[5,'Realty Mogul','https://www.realtymogul.com']


images= []
for x in websites:
    customer_key = '16e8d4'
    secret_phrase = '' # leave secret phrase empty, if not needed
    options = {
      'url': x[2], # mandatory parameter
      # all next parameters are optional, see our website screenshot API guide for more details
      'dimension': '1920x1080', # or "1366xfull" for full length screenshot
      'device': 'desktop',
      'cacheLimit' : '0',
      'delay' : '200',
      'zoom' : '100'
      }

    api_url = generate_screenshot_api_url(customer_key, secret_phrase, options)

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', '-')]
    urllib.request.install_opener(opener)
    output = str(x[0])+" "+str(x[1])+'.jpg'
    images.append(output)
    urllib.request.urlretrieve(api_url, output)
    print('Screenshot saved as ' + output);

for image in images:
    # I am removing the fileID part because it is unique to me
    file = drive.CreateFile({"mimeType": "image/jpeg", "parents": [{"kind": "drive#fileLink", "id": fileID}]})
    file.SetContentFile(image)
    file.Upload()
    print(image+"has been uploaded succesfully")
