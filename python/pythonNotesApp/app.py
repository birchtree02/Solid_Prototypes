from solid.auth import Auth
from solid.solid_api import SolidAPI

import io
import json


class NotesApp():
    def __init__(self, folder_name="notes"):

        self.auth = Auth()
        self.login()
        self.folder_url = self.POD_ENDPOINT + folder_name + '/'

        if not self.api.item_exists(self.folder_url):
            self.api.create_folder(self.folder_url)
            if not self.api.item_exists(self.folder_url):
                raise Exception('Error initialising folder.')

    def login(self):
        configs = json.load(open('account.json'))
        self.POD_ENDPOINT = configs['SOLID_ENDPOINT']
        IDP = "https://broker.pod.inrupt.com"
        USERNAME = configs['SOLID_USERNAME']
        PASSWORD = configs['SOLID_PASSWORD']

        self.api = SolidAPI(self.auth)
        self.auth.login(IDP, USERNAME, PASSWORD)

        # self.api = SolidAPI()

    def editNote(self, note_name, content_to_add):
        note_url = self.folder_url + note_name + '.md'
        if not self.api.item_exists(note_url):
            self._createNote(note_url, content_to_add)
        else:
            pass

    def _createNote(self, note_url, content=""):
        self.api.put_file(note_url, io.BytesIO(content.encode('UTF-8')), 'text/markdown')

    def getNote(self, note_name):
        note_url = self.folder_url + note_name + '.md'
        resp = self.api.get(note_url)
        
        return resp.text


if __name__ == '__main__':
    app = NotesApp()
