#!/usr/bin/python
import requests
from xml.dom import minidom

class JasperServerIntegration:
    def __init__(self, jasperUrl, reportPath, type, user, password, parameters):
        self.jasperUrl = jasperUrl
        self.reportPath = reportPath
        self.type = type
        self.user = user
        self.password = password
        self.parameters = parameters

    def _getQueryString(self):
        queryString = ''

        for key in self.parameters:
            if queryString == '':
                queryString += '?'
            else:
                queryString += '&'
            queryString += str(key) + '=' + str(self.parameters[key])
        
        return queryString; 
    
    def execute(self):
        url = self.jasperUrl + '/rest_v2/reports/' + self.reportPath + '.' + self.type + self._getQueryString()
        r = requests.get(url, auth=(self.user, self.password))

        if r.status_code != 200:
            mydoc = minidom.parseString(r.text)
            errorCodeElement = mydoc.getElementsByTagName('errorCode')
            errorCode = errorCodeElement[0].childNodes[0].data
            messageElement = mydoc.getElementsByTagName('message')
            message = messageElement[0].childNodes[0].data

            self.error_code = errorCode
            self.error_message = message

            raise Exception('Status code: ' + str(r.status_code) + ', Error Code: ' + errorCode +  ', Message: ' + message)

        return r.content
        


