import json

class JSONConfig(object):
	def __init__(self, settingsPath):
		self.settingsPath = settingsPath
		self.settings = None
	def Load(self):
		try:
			with open(self.settingsPath) as file:
				self.settings = json.load(file)
		except:
			print "Failed to open JSON config {0}".format(self.settingsPath)
			return False
		return True
	def Save(self):
		if self.settings == None:
			print "Failed to write JSON config - settings not loaded"
			return False
		try:
			formattedOptions = json.dumps(self.settings, sort_keys=True, indent=4, separators=(',', ': '))
			with open(self.settingsPath, 'w') as file:
				file.write(formattedOptions)
		except:
			print "Failed to write JSON config {0}".format(self.settingsPath)
			return False
		return True
	def GetSettings(self):
		return self.settings
	def ToJSONString(self):
		return json.dumps(self.settings, sort_keys=True, indent=4, separators=(',', ': '))
	def GetSetting(self, key):
		if self.settings == None:
			return None
		found = self.settings
		keyPath = key.split('.')
		for part in keyPath:
			try:
				found = found[part]
			except:
				return None
		return found
	def SetSetting(self, key, value):
		if self.settings == None:
			return False
		last, lastPart = None, None
		found = self.settings
		keyPath = key.split('.')
		try:
			for part in keyPath:
				if part not in found.keys():
					found[part] = {}
				lastPart = part
				last = found
				found = found[part]
			last[lastPart] = value
		except:
			return False
		return True
	def GetCollapsedConfigDict(self):
		if self.settings == None:
			return {}
		return __GenerateReplacementDict(self.settings)
	def __GenerateReplacementDict(data, prefix=""):
		optionsDict = {}
		for subKey in data:
			key = "{0}{1}{2}".format(prefix, "." if prefix != "" else "", subKey)
			if isinstance(data[subKey], dict):
				subDict = __GenerateReplacementDict(data[subKey], key)
				optionsDict.update(subDict)
			elif isinstance(data[subKey], list):
				pass
			else:
				optionsDict[key] = str(data[subKey])
		return optionsDict

options = JSONConfig('test.json')
options.Load()
options.SetSetting("something.one", "test")
options.SetSetting("something.two", 34)
print options.ToJSONString()