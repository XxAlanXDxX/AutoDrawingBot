import json

class DataManager:
    def __init__(self):
        self.loadSetting()

    def loadSetting(self):
        with open(f'setting.json', 'r', encoding='utf-8') as jfile:
            self.jsetting = json.load(jfile)

    def saveSetting(self, setting_data):
        with open(f'setting.json', 'w', encoding='utf-8') as jfile:
            json.dump(setting_data, jfile, ensure_ascii=False, indent=4)

        self.loadSetting()
