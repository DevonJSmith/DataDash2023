class TuyaApi(object):
	def RetrieveDeviceProperties(self,deviceId):
		'''
			Pull current values of all available properties on device
			API reference: https://developer.tuya.com/en/docs/cloud/116cc8bf6f?id=Kcp2kwfrpe719
			@PARAM deviceId: string - the deviceId to retrieve data for
			@RETURN: list<dict> - the json results from the API
		'''
		# TODO: implement fully
		response = {
		  'result': {
		    'properties': [
		      {
		        'code': 'switch_on',
		        'custom_name': '',
		        'dp_id': 1,
		        'time': 1690929978364,
		        'value': True
		      },
		      {
		        'code': 'set_temper',
		        'custom_name': '',
		        'dp_id': 6,
		        'time': 1690929984387,
		        'value': 15
		      },
		      {
		        'code': 'wind_speed',
		        'custom_name': '',
		        'dp_id': 8,
		        'time': 1690930858112,
		        'value': '2'
		      },
		      {
		        'code': 'fault',
		        'custom_name': '',
		        'dp_id': 15,
		        'time': 1690929238118,
		        'value': 0
		      },
		      {
		        'code': 'f_temper',
		        'custom_name': '',
		        'dp_id': 18,
		        'time': 1694309036820,
		        'value': 66
		      },
		      {
		        'code': 'filterClean',
		        'custom_name': '',
		        'dp_id': 25,
		        'time': 1690929165248,
		        'value': True
		      }
		    ]
		  },
		  'success': True,
		  't': 1694309042141,
		  'tid': 'b972af854f7811ee8711ea6e14ba735f'
		}
		return response['result']['properties']
	#END RetrieveDeviceProperties
#END TuyaApi