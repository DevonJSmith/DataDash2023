import hmac
import hashlib
class TuyaApi(object):
	BASE_URL = 'https://openapi.tuyaus.com'
	
	def __init__(self):
		self._access_code = None
		self._access_code_expiration = None
	#END __init__
	
	@property
	def access_code(self):
		if self._access_code is None or self._access_code_expiration is None or system.date.now() >= self._access_code_expiration:
			self._authenticate()
		#END if
		return self._access_code
	#END access-code

	def _authenticate(self):
		'''
			Gets an Auth Token from the Tuya API
		'''
		timeStamp = system.date.toMillis(system.date.now())
		queryUrl = '/v1.0/token?grant_type=1'
		headers = {
			'client_id': data_dash.SECRETS.CLIENT_ID,
			't': timeStamp,
			'sign_method': 'HMAC-SHA256',
			'nonce': None,
			'stringToSign': None,
			'sign': None
		}
		signMap = self._generateSignMap(method = 'get', url = queryUrl)
		headers['stringToSign'] = signMap['signUrl'].replace('\n','')
		headers['sign'] = self._generateSignCode(
			clientId = data_dash.SECRETS.CLIENT_ID,
			timestamp = timeStamp,
			nonce = None,
			signStr = signMap['signUrl'],
			secret = data_dash.SECRETS.CLIENT_SECRET
		)
		
		resp = system.net.httpGet(
			url = self.BASE_URL + queryUrl,
			headerValues = headers
		)
		jsonResp = system.util.jsonDecode(resp)
		self._access_code = jsonResp['result']['access_token']
		token_lifetime_seconds = jsonResp['result']['expire_time']
		self._access_code_expiration = system.date.addSeconds(system.date.now(), token_lifetime_seconds - 120)
	#END _authenticate
	
	def _generateSignMap(self, method, url):
		'''
			This algorithm has been taken from the examples available in the Tuya API
			https://developer.tuya.com/en/docs/iot/new-singnature?id=Kbw0q34cs2e5g
		'''
		sha256 = ''
		headersStr = ''
		signMap = {}
		signArr = []
		
		hashObj = hashlib.sha256()
		hashObj.update(sha256)
		sha256 = hashObj.hexdigest()
		
		signMap = {
			'url': url,
			'signUrl': method.upper() + '\n' + sha256 + '\n' + headersStr + '\n' + url 
		}
		return signMap
	#END _generateSignMap

	def _generateSignCode(self, clientId, timestamp, nonce, signStr, secret, access_code = None):
		'''
			generates a sign code for authenticating with Tuya API
			Reference: https://developer.tuya.com/en/docs/iot/new-singnature?id=Kbw0q34cs2e5g
		'''
		strToHash = None
		if access_code is not None:
			strToHash = clientId + str(access_code) + str(timestamp) + str(nonce) + signStr
		else:
			strToHash = clientId + str(timestamp) + str(nonce) + signStr
		#END if
		hashedStr = hmac.new(
		    secret,
		    msg=strToHash,
		    digestmod=hashlib.sha256
		).hexdigest().upper()
		return hashedStr
	#END _generateSignCode
	
	def RetrieveDeviceProperties(self, deviceId):
		'''
			Pull current values of all available properties on device
			API reference: https://developer.tuya.com/en/docs/cloud/116cc8bf6f?id=Kcp2kwfrpe719
			@PARAM deviceId: string - the id of the device to retrieve data for
			@RETURN: list<dict> - the json results from the API
		'''
		timeStamp = system.date.toMillis(system.date.now())
		queryUrl = '/v2.0/cloud/thing/%s/shadow/properties' % deviceId
		headers = {
			'client_id': data_dash.SECRETS.CLIENT_ID,
			'access_token': self.access_code,
			't': timeStamp,
			'sign_method': 'HMAC-SHA256',
			'nonce': None,
			'stringToSign': None,
			'sign': None
		}
		signMap = self._generateSignMap(method = 'get', url = queryUrl)
		headers['stringToSign'] = signMap['signUrl'].replace('\n','')
		headers['sign'] = self._generateSignCode(
			clientId = data_dash.SECRETS.CLIENT_ID,
			timestamp = timeStamp,
			nonce = None,
			signStr = signMap['signUrl'],
			secret = data_dash.SECRETS.CLIENT_SECRET,
			access_code = self.access_code
		)
		
		resp = system.net.httpGet(
			url = self.BASE_URL + queryUrl,
			headerValues = headers
		)
		response = system.util.jsonDecode(resp)
		return response['result']['properties']
	#END RetrieveDeviceProperties
	
	def RetrieveDeviceDetails(self, deviceId):
		'''
			Retrieves base details about device from Tuya API
			API Reference: https://developer.tuya.com/en/docs/cloud/3829469013?id=Kcp2l2v9wma0m
			@PARAM deviceId: string - the id of the device to retrieve info for
		'''
		timeStamp = system.date.toMillis(system.date.now())
		queryUrl = '/v1.0/devices/%s' % deviceId
		headers = {
			'client_id': data_dash.SECRETS.CLIENT_ID,
			'access_token': self.access_code,
			't': timeStamp,
			'sign_method': 'HMAC-SHA256',
			'nonce': None,
			'stringToSign': None,
			'sign': None
		}
		signMap = self._generateSignMap(method = 'get', url = queryUrl)
		headers['stringToSign'] = signMap['signUrl'].replace('\n','')
		headers['sign'] = self._generateSignCode(
			clientId = data_dash.SECRETS.CLIENT_ID,
			timestamp = timeStamp,
			nonce = None,
			signStr = signMap['signUrl'],
			secret = data_dash.SECRETS.CLIENT_SECRET,
			access_code = self.access_code
		)
		
		resp = system.net.httpGet(
			url = self.BASE_URL + queryUrl,
			headerValues = headers
		)
		response = system.util.jsonDecode(resp)
		return response['result']
	#END RetrieveDeviceDetails
#END TuyaApi