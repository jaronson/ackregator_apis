import httplib
import xml.dom.minidom

class GunbrokerAPI():
  dev_key = "10232355-fe17-46dd-a4d1-c3d106e17e82"
  app_key = "09e1dda2-cf80-43af-aee9-54350d5cb074"
  username = "samizdat"
  password = "lu253i"  

  def __init__(self):
    self.url = "apiv2.gunbroker.com"
    self.port = "80"
    self.api_version = "GunBrokerAPI_V2"
    self.xmlns= "AuctionService.asmx"
    self.responseData = None

  def getSearchResults(self, options={}):
    return self.__makeRequest('GetSearchResults', options)

  # @private 
  def __makeRequest(self, soap_action, options):
    body = self.__buildSoapEnvelope(soap_action, options) 
    headers = self.__buildHTTPHeaders(soap_action, len(body))
    print body, headers

    conn = httplib.HTTPConnection(self.url + ":" + self.port)
    request = conn.request("POST", "/" + self.xmlns, body, headers)
    response = conn.getresponse()
    # log response.status, response.reason
    data = response.read()
    conn.close()
    return data

  def __buildSoapEnvelope(self, soap_action, options):
    return """<?xml version="1.0" encoding="utf-8"?>
  <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    %s
    %s
  </soap:Envelope>""" % ( self.__buildSoapHeader(), self.__buildSoapBody(soap_action, options))

  def __buildSoapHeader(self):
    return """<soap:Header>
      <RequesterCredentials xmlns="%s">
        <DevKey>%s</DevKey>
        <AppKey>%s</AppKey>
        <UserName>%s</UserName>
        <Password>%s</Password>
      </RequesterCredentials>
    </soap:Header>""" % ( self.api_version,
                          GunbrokerAPI.dev_key, 
                          GunbrokerAPI.app_key, 
                          GunbrokerAPI.username, 
                          GunbrokerAPI.password )

  def __buildSoapBody(self, soap_action, options):
    body = "\n\t\t<%sRequest>" % ( soap_action )
    for key, value in options.items():
      body += "\n\t\t\t<%s>%s</%s>" % ( key, value, key )
    body += "\n\t\t</%sRequest>" % ( soap_action )
    return "<soap:Body>\n\t<%s xmlns=\"%s\">%s\n\t</%s>\n</soap:Body>" % ( soap_action, self.api_version, body, soap_action )

  def __buildHTTPHeaders(self, soap_action, content_length):
    return {
      "Host" : "apiv2.gunbroker.com",
      "Content-Type": "text/xml; charset=utf-8",
      "Content-Length": content_length,
      "SOAPAction": "\"%s/%s\"" % (self.api_version, soap_action)
    }
