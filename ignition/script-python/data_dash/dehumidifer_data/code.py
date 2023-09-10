Dehumidifer_Tag_Base = '[default]djamessmith03/Basement Dehumidifer'

def RefreshAnalyticData():
	'''
		Calls the Tuya Cloud API to retrieve dehumidifier property values
	'''
	deviceId = data_dash.SECRETS.DEVICE_ID
	tuyaAPI = data_dash.tuya_api.TuyaApi()
	
	tagPaths = []
	tagValues = []
	
	propertyList = tuyaAPI.RetrieveDeviceProperties(deviceId)
	for prop in propertyList:
		propName = prop['code']
		tagName = None
		if propName == 'switch_on':
			tagName = 'Switch On'
		elif propName == 'wind_speed':
			tagName = 'Fan Setting'
		elif propName == 'set_temper':
			tagName = 'Humidity Setting'
		elif propName == 'fault':
			tagName = 'Fault Code'
		elif propName == 'f_temper':
			tagName = 'Current Humidity'
		elif propName == 'filterClean':
			tagName = 'Filter Clean'
		#END if
		tagPaths.append('%(baseTagPath)s/Analytics/%(tagName)s' % {'baseTagPath': Dehumidifer_Tag_Base, 'tagName': tagName})
		tagValues.append(prop['value'])
	#END for
	system.tag.writeAsync(tagPaths = tagPaths, values = tagValues)
#END RefreshAnalyticData