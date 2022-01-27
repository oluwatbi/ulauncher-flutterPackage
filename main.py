import requests
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

class FlutterExtension(Extension):

    def __init__(self):
        super(FlutterExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument()
        searchSize = extension.preferences['fpub_search_result_size']
        if not searchSize:
          return
        url = 'https:pub.dev/search?q=' + query + '&size=' + searchSize'
        # logger.debug(url)

        response = requests.get(url, headers ={'User-Agent': 'ulauncher-flutterPackage'})
        data = response.json()
        # logger.debug(data)

        items = []
        for i in data['results']:
          package = results['package']
          # logger.debug(package)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=package['name'],
                                             description=package['description'],
                                              on_enter=OpenUrlAction(package['pub_url'])))
                                            #  on_enter=HideWindowAction()))

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data['package']['name'],
                                                           description=data['package']['description'],
                                                           on_enter=OpenUrlAction(data['package']['pub_url']))])

if __name__ == '__main__':
    FlutterExtension().run()