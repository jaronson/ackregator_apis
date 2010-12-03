import sys
import httplib
import ConfigParser

from ..persistence import Model

class Gunbroker():
  config = ConfigParser.RawConfigParser()
  config.read("../../config/application.conf")
  
  dev_key   = config.get("Gunbroker API", "dev_key")
  app_key   = config.get("Gunbroker API", "app_key")
  username  = config.get("Gunbroker API", "username")
  password  = config.get("Gunbroker API", "password")

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

    # Insert the whole response into the database
    model = Model()
    model.insertListing("gunbroker", data) 
    return response.status 

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
                          Gunbroker.dev_key, 
                          Gunbroker.app_key, 
                          Gunbroker.username, 
                          Gunbroker.password )

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
