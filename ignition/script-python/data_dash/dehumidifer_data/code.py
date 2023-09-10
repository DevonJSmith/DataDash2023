Dehumidifier_Tag_Base = '[default]djamessmith03/Basement Dehumidifer'

def RefreshBasicDeviceDetails():
	'''
		Calls the Tuya Cloud API to retrieve basic info (name, update timestamp, etc) for the dehumidifer
	'''
	deviceId = data_dash.SECRETS.DEVICE_ID
	tuyaAPI = data_dash.tuya_api.TuyaApi()
	
	tagPaths = []
	tagValues = []
	
	details = tuyaAPI.RetrieveDeviceDetails(deviceId)
	# date fields
	# create time
	tagPaths.append('%s/Create Time' % Dehumidifier_Tag_Base)
	tagValues.append(system.date.fromMillis(details['create_time'] * 1000))
	# active time
	tagPaths.append('%s/Active Time' % Dehumidifier_Tag_Base)
	tagValues.append(system.date.fromMillis(details['active_time'] * 1000))
	# update time
	tagPaths.append('%s/Update Time' % Dehumidifier_Tag_Base)
	tagValues.append(system.date.fromMillis(details['update_time'] * 1000))
	# device name
	tagPaths.append('%s/Device Name' % Dehumidifier_Tag_Base)
	tagValues.append(details['name'])
	
	system.tag.writeAsync(tagPaths = tagPaths, values = tagValues)
#END RefreshBasicDeviceDetails

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
		tagPaths.append('%(baseTagPath)s/Analytics/%(tagName)s' % {'baseTagPath': Dehumidifier_Tag_Base, 'tagName': tagName})
		tagValues.append(prop['value'])
	#END for
	system.tag.writeAsync(tagPaths = tagPaths, values = tagValues)
#END RefreshAnalyticData