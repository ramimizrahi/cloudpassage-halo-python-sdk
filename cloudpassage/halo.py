#!/usr/bin/env python


import sys
import json
import urllib
import urllib2
import sanity
import fn
import base64
import threading
import datetime


# Class with calls to CloudPassage API
class HALO:

    def __init__(self):
        self.auth_url = 'oauth/access_token'
        self.auth_args = {'grant_type': 'client_credentials'}
        self.base_url = 'https://api.cloudpassage.com'
        self.api_ver = 'v1'
        self.port = 443
        self.key_id = None
        self.secret = None
        self.authToken = None
        self.authTokenScope = None
        self.lock = threading.RLock()
        self.api_count = 0
        self.api_time = 0.0

    # Dump debug info
    def dumpToken(self, token, expires):
        if (token):
            print "AuthToken=%s" % token
        if (expires):
            print "Expires in %s minutes" % (expires / 60)

    def getHttpStatus(self, code):
        if (code == 200):
            return "OK" 	# should never be passed in, only errors
        elif (code == 401):
            return "Unauthorized"
        elif (code == 403):
            return "Forbidden"
        elif (code == 404):
            return "Not found"
        elif (code == 422):
            return "Validation failed"
        elif (code == 500):
            return "Internal server error"
        elif (code == 502):
            return "Gateway error"
        else:
            return "Unknown code [%d]" % code

    def addAuth(self, req, kid, sec):
        combined = kid + ":" + sec
        encoded = base64.b64encode(combined)
        req.add_header("Authorization", "Basic " + encoded)

    def getAuthToken(self, url, args, kid, sec):
        req = urllib2.Request(url)
        self.addAuth(req, kid, sec)
        # print >> sys.stderr, "getAuthToken: key=%s secret=%s" % (kid, sec)
        # createPasswordMgr(url, kid, sec)
        if (args):
            args = urllib.urlencode(args)
        try:
            fh = urllib2.urlopen(req, args)
            return fh.read()
        except IOError, e:
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
            elif hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to authorize [%s] at '%s'" % (
                    msg, url)
                data = e.read()
                if data:
                    print >> sys.stderr, "Extra data: %s" % data
                print >> sys.stderr, "Likely cause: incorrect API keys, id=%s" % kid
            else:
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return None

    def getInitialLink(self, fromDate, events_per_page):
        url = "%s:%d/%s/events?per_page=%d" % (self.base_url,
                                               self.port,
                                               self.api_ver,
                                               events_per_page)
        if (fromDate):
            url += "&since=" + fromDate
        return url

    def getEventBatch(self, url):
        return self.doGetRequest(url, self.authToken)

    def logTime(self, start_time, end_time):
        delta = end_time - start_time
        with self.lock:
            self.api_count += 1
            self.api_time += delta.total_seconds()

    def getTimeLog(self):
        tuple = None
        with self.lock:
            tuple = (self.api_count, self.api_time)
        return tuple

    def doGetRequest(self, url, token):
        req = urllib2.Request(url)
        req.add_header("Authorization", "Bearer " + token)
        try:
            start_time = datetime.datetime.now()
            fh = urllib2.urlopen(req)
            data = fh.read()
            contentType = fh.info().getheader('Content-type')
            (mimetype, encoding) = contentType.split("charset=")
            # print >> sys.stderr, "Type=%s  Encoding=%s" % (mimetype, encoding)
            translatedData = data.decode(encoding, 'ignore').encode('utf-8')
            results = (translatedData, False)
            end_time = datetime.datetime.now()
            self.logTime(start_time, end_time)
            return results
        except IOError, e:
            authError = False
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
                if (e.reason == "Unauthorized"):
                    authError = True
            if hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to fetch events [%s] from '%s'" % (
                    msg, url)
                if (e.code == 401) or (e.code == 403):
                    authError = True
                print >> sys.stderr, "Error response: %s" % e.read()
            else:
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return (None, authError)

    def doPutRequest(self, url, token, putData):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        req = urllib2.Request(url, data=putData)
        req.add_header("Authorization", "Bearer " + token)
        req.add_header("Content-Type", "application/json")
        req.get_method = lambda: 'PUT'
        try:
            start_time = datetime.datetime.now()
            fh = opener.open(req)
            results = (fh.read(), False)
            end_time = datetime.datetime.now()
            self.logTime(start_time, end_time)
            return results
        except IOError, e:
            authError = False
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
            if hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to make request: [%s] from '%s'" % (
                    msg, url)
                if (e.code == 401) or (e.code == 403):
                    authError = True
                print >> sys.stderr, "Error response: %s" % e.read()
            if (not hasattr(e, 'reason')) and (not hasattr(e, 'code')):
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return (None, authError)

    def doPostRequest(self, url, token, putData):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        req = urllib2.Request(url, data=putData)
        req.add_header("Authorization", "Bearer " + token)
        req.add_header("Content-Type", "application/json")
        try:
            start_time = datetime.datetime.now()
            fh = opener.open(req)
            results = (fh.read(), False)
            end_time = datetime.datetime.now()
            self.logTime(start_time, end_time)
            return results
        except IOError, e:
            authError = False
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
            if hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to make request: [%s] from '%s'" % (
                    msg, url)
                if (e.code == 401) or (e.code == 403):
                    authError = True
                print >> sys.stderr, "Error response: %s" % e.read()
            if (not hasattr(e, 'reason')) and (not hasattr(e, 'code')):
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return (None, authError)

    def doDeleteRequest(self, url, token):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        req = urllib2.Request(url)
        req.add_header("Authorization", "Bearer " + token)
        req.add_header("Content-Type", "application/json")
        req.get_method = lambda: 'DELETE'
        try:
            fh = opener.open(req)
            return (fh.read(), False)
        except IOError, e:
            authError = False
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
            if hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to make request: [%s] from '%s'" % (
                    msg, url)
                if (e.code == 401):
                    authError = True
            if (not hasattr(e, 'reason')) and (not hasattr(e, 'code')):
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return (None, authError)

    def authenticateClient(self):
        url = "%s:%d/%s" % (self.base_url, self.port, self.auth_url)
        self.token = None
        response = self.getAuthToken(
            url, self.auth_args, self.key_id, self.secret)
        if (response):
            authRespObj = json.loads(response)
            if ('access_token' in authRespObj):
                self.authToken = authRespObj['access_token']
            if ('expires_in' in authRespObj):
                self.expires = authRespObj['expires_in']
            if ('scope' in authRespObj):
                self.authTokenScope = authRespObj['scope']
        # dumpToken(token,expires)
        return self.authToken

    def getServerList(self):
        url = "%s:%d/%s/servers" % (self.base_url, self.port, self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getServerGroupList(self):
        url = "%s:%d/%s/groups" % (self.base_url, self.port, self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getServersInGroup(self, groupID):
        url = "%s:%d/%s/groups/%s/servers" % (self.base_url,
                                              self.port,
                                              self.api_ver,
                                              groupID)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getFirewallPolicyList(self):
        url = "%s:%d/%s/firewall_policies/" % (self.base_url,
                                               self.port,
                                               self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getFirewallPolicyDetails(self, policyID):
        url = "%s:%d/%s/firewall_policies/%s" % (self.base_url,
                                                 self.port,
                                                 self.api_ver,
                                                 policyID)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def moveServerToGroup(self, serverID, groupID):
        url = "%s:%d/%s/servers/%s" % (self.base_url,
                                       self.port,
                                       self.api_ver,
                                       serverID)
        reqData = {"server": {"group_id": groupID}}
        jsonData = json.dumps(reqData)
        # print "move: %s" % jsonData
        (data, authError) = self.doPutRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createServerGroup(self, groupName, **kwargs):
        url = "%s:%d/%s/groups" % (self.base_url, self.port, self.api_ver)
        groupData = {"name": groupName, "policy_ids": [], "tag": None}
        sanity.validate_server_args(kwargs)
        reqData = {"group": fn.merge_dicts(groupData, kwargs)}
        jsonData = json.dumps(reqData)
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteServerGroup(self, group_id, **kwargs):
        if (("force" in kwargs) and (kwargs["force"] == True)):
            url = "%s:%d/%s/groups/%s%s" % (self.base_url,
                                            self.port,
                                            self.api_ver,
                                            group_id,
                                            "?move_to_parent=true")
        else:
            url = "%s:%d/%s/groups/%s" % (self.base_url,
                                          self.port,
                                          self.api_ver,
                                          group_id)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createFirewallPolicy(self, policyData):
        url = "%s:%d/%s/firewall_policies" % (self.base_url,
                                              self.port,
                                              self.api_ver)
        jsonData = json.dumps(policyData)
        # print jsonData # for debugging
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def listFirewallPolicies(self):
        url = "%s:%d/%s/firewall_policies" % (self.base_url,
                                              self.port,
                                              self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteFirewallPolicy(self, policyID):
        url = "%s:%d/%s/firewall_policies/%s" % (self.base_url,
                                                 self.port,
                                                 self.api_ver,
                                                 policyID)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def assignFirewallPolicyToGroup(self, groupID, attrName, policyID):
        url = "%s:%d/%s/groups/%s" % (self.base_url,
                                      self.port,
                                      self.api_ver,
                                      groupID)
        reqData = {"group": {attrName: policyID}}
        jsonData = json.dumps(reqData)
        (data, authError) = self.doPutRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createConfigurationPolicy(self, policyData):
        url = "%s:%d/%s/policies" % (self.base_url, self.port, self.api_ver)
        jsonData = json.dumps(policyData)
        # print jsonData # for debugging
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        # print data
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def listConfigurationPolicies(self):
        url = "%s:%d/%s/policies" % (self.base_url, self.port, self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteConfigurationPolicy(self, policyID):
        url = "%s:%d/%s/policies/%s" % (self.base_url,
                                        self.port,
                                        self.api_ver,
                                        policyID)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createFIMPolicy(self, policyData):
        url = "%s:%d/%s/fim_policies" % (self.base_url,
                                         self.port,
                                         self.api_ver)
        jsonData = json.dumps(policyData)
        # print jsonData # for debugging
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        # print data
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def listFIMPolicies(self):
        url = "%s:%d/%s/fim_policies" % (self.base_url,
                                         self.port,
                                         self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteFIMPolicy(self, policyID):
        url = "%s:%d/%s/fim_policies/%s" % (self.base_url,
                                            self.port,
                                            self.api_ver,
                                            policyID)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createLIDSPolicy(self, policyData):
        url = "%s:%d/%s/lids_policies" % (self.base_url,
                                          self.port, self.api_ver)
        jsonData = json.dumps(policyData)
        # print jsonData # for debugging
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        # print data
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def listLIDSPolicies(self):
        url = "%s:%d/%s/lids_policies" % (self.base_url,
                                          self.port,
                                          self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteLIDSPolicy(self, policyID):
        url = "%s:%d/%s/lids_policies/%s" % (self.base_url,
                                             self.port,
                                             self.api_ver,
                                             policyID)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getAnnouncements(self):
        url = "%s:%d/%s/system_announcements" % (self.base_url,
                                                 self.port,
                                                 self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def initiateScan(self, serverId, scan_type):
        url = "%s:%d/%s/servers/%s/scans" % (self.base_url,
                                             self.port,
                                             self.api_ver,
                                             serverId)
        module_ref = {"sca": "sca",
                      "csm": "sca",
                      "sva": "svm",
                      "svm": "svm",
                      "fim": "fim",
                      "sam": "sam"}
        module = module_ref.get(scan_type)
        if module == None:
            bad_scan_msg = "Invalid scan type: " + str(scan_type)
            return (None, bad_scan_msg)
        jsondata = {"scan": {"module": module}}
        (data, authError) = self.doPostRequest(url,
                                               self.authToken,
                                               json.dumps(jsondata))
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)
