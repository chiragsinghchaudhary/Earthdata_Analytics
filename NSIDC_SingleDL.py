'''
 This script, NSIDC_SingleDL.py, grabs a singular file from a complete HTTPS URL.

 This code was adapted from https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python

 Last edited Jan 26, 2017 G. Deemer 
 
 ===============================================
 Technical Contact
 ===============================================

 NSIDC User Services
 National Snow and Ice Data Center
 CIRES, 449 UCB
 University of Colorado
 Boulder, CO 80309-0449  USA
 phone: +1 303.492.6199
 fax: +1 303.492.2468
 form: Contact NSIDC User Services
 e-mail: nsidc@nsidc.org

'''

#!/usr/bin/python
import urllib2
from cookielib import CookieJar

#===============================================================================
# The following code block is used for authentication for HTTPS server
#===============================================================================

# The user credentials that will be used to authenticate access to the data
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

# The FULL url of the file we wish to retrieve
url = "https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0192_seaice_trends_climo_v2/total-ice-area-extent/nasateam/gsfc.nasateam.daily.extent.1978-2015.s" # Example URL

# Strip the filename from the URL
file_name = url.split('/')[-1]

# Create a password manager to deal with the 401 reponse that is returned from
# Earthdata Login
 
password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
 
# Create a cookie jar for storing cookies. This is used to store and return
# the session cookie given to use by the data server (otherwise it will just
# keep sending us back to Earthdata Login to authenticate).  Ideally, we
# should use a file based cookie jar to preserve cookies between runs. This
# will make it much more efficient.
 
cookie_jar = CookieJar()

# Install all the handlers.
opener = urllib2.build_opener(
    urllib2.HTTPBasicAuthHandler(password_manager),
    #urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
    #urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
    urllib2.HTTPCookieProcessor(cookie_jar))
urllib2.install_opener(opener)
 
# Create and submit the requests. There are a wide range of exceptions that
# can be thrown here, including HTTPError and URLError. These should be
# caught and handled.

#===============================================================================
# Open a request for the data, and download a specific file
#===============================================================================

DataRequest = urllib2.Request(url)
DataRequest.add_header('cookie', cookie_jar) # Pass the saved cookie into a second HTTP request
DataResponse = urllib2.urlopen(DataRequest)

# Get the redirect url and append 'app_type=401'
# to do basic http auth
DataRedirect_url = DataResponse.geturl()
DataRedirect_url += '&app_type=401'

# Request the resource at the modified redirect url
DataRequest = urllib2.Request(DataRedirect_url)
DataResponse = urllib2.urlopen(DataRequest)

# Print out the result (not a good idea with binary data!)
DataBody = DataResponse.read(DataResponse)

# Save file to working directory
file_ = open(file_name, 'wb')
file_.write(DataBody)
file_.close()

print "Your file, ", file_name, " has downloaded to ", os.path.dirname(os.path.realpath(__file__))