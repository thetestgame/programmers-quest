
from panda3d import core as p3d

from quest.engine import core, prc, runtime
from quest.framework import singleton, runnable

import traceback
import urllib
import json

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class HttpRequest(core.QuestObject):
    """
    """

    def __init__(self, channel: object, ram_file: object, callback: object = None):
        super().__init__()

        self._channel = channel
        self._ram_file = ram_file
        self._callback = callback

    async def update(self) -> bool:
        """
        """

        if self._channel is None:
            return

        done = not self._channel.run()
        if done and self._callback != None:
            try:
                assert callable(self._callback), 'Callback is not a valid callable object'
                self._callback(self._ram_file.get_data())
            except Exception as e:
                self.notify.warning('Exception occured processing HTTP callback')
                print(traceback.format_exc())

        return done

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class HttpManager(singleton.Singleton, runnable.Runnable, core.QuestObject):
    """
    """

    def __init__(self):
        runnable.Runnable.__init__(self, collector='App:HttpUpdates')
        core.QuestObject.__init__(self)
        runtime.http_mgr = self

        max_http_requests = prc.get_prc_int('http-max-requests', 900)
        self._http_client = p3d.HTTPClient()
        self._request_allocator = p3d.UniqueIdAllocator(0, max_http_requests)

        self._requests = {}
        self.activate()

    def destroy(self) -> None:
        """
        """

        self.deactivate()
        for request_id in list(self._requests.keys()):
            self.remove_request(request_id)

    async def tick(self, dt: float) -> None:
        """
        Performs the tick operation for the runnable object
        """

        for request_id in list(self._requests.keys()):
            if not request_id in self._requests:
                continue
                
            request = self._requests[request_id]
            if await request.update():
                self.remove_request(request_id)

    def remove_request(self, request_id: int) -> None:
        """
        """

        if not request_id in self._requests:
            return

        self._request_allocator.free(request_id)
        del self._requests[request_id]

    def get_request_status(self, request_id: int) -> bool:
        """
        Returns the requests current status. 
        """

        return not request_id in self._requests

    def get_request(self, request_id: int) -> HttpRequest:
        """
        Returns the requested request if its present
        """

        return self._requests.get(request_id, None)    

    def perform_get_request(self, url: str, headers: dict = {}, body: dict = {}, content_type: str = None, callback: object = None) -> int:
        """
        Performs an HTTP restful GET call and returns the request's unique identifier
        """

        self.notify.debug('Sending GET request: %s' % url)
        request_channel = self._http_client.make_channel(True)

        if content_type != None:
            request_channel.set_content_type(content_type)

        for header_key in headers:
            header_value = headers[header_key]
            request_channel.send_extra_header(header_key, header_value)

        if len(body) > 0:
            request_params = urllib.urlencode(body, doseq=True)
            url = '%s/?%s' % (url, request_params)
        request_channel.begin_get_document(p3d.DocumentSpec(url))

        ram_file = p3d.Ramfile()
        request_channel.download_to_ram(ram_file, False)

        request_id = self._request_allocator.allocate()
        http_request = HttpRequest(request_channel, ram_file, callback)
        self._requests[request_id] = http_request

        return request_id

    def perform_json_get_request(self, url: str, headers: dict = {}, body: dict = {}, callback: object = None) -> int:
        """
        """

        def json_wrapper(data):
            """
            Wraps the callback to automatically perform json.load
            on the resulting data
            """

            try:
                data = json.loads(data)
            except:
                self.notify.warning('Received invalid JSON results: %s' % data)
                
            callback(data)

        return self.perform_get_request(
            url=url, 
            content_type='application/json',
            headers=headers,
            body=body,
            callback=json_wrapper)

    def perform_post_request(self, url: str, headers: dict = {}, body: dict = {}, content_type: str = None, callback: object = None) -> int:
        """
        """

        self.notify.debug('Sending POST request: %s' % url)
        request_channel = self._http_client.make_channel(True)

        if content_type != None:
            request_channel.set_content_type(content_type)

        for header_key in headers:
            header_value = headers[header_key]
            request_channel.send_extra_header(header_key, header_value)

        body = json.dumps(body)
        request_channel.begin_post_form(p3d.DocumentSpec(url), body)

        ram_file = p3d.Ramfile()
        request_channel.download_to_ram(ram_file, False)

        request_id = self._request_allocator.allocate()
        http_request = HttpRequest(request_channel, ram_file, callback)
        self._requests[request_id] = http_request

        return request_id

    def perform_json_post_request(self, url: str, headers: dict = {}, body: dict = {}, callback: object = None) -> int:
        """
        """

        def json_wrapper(data):
            """
            Wraps the callback to automatically perform json.load
            on the resulting data
            """

            try:
                data = json.loads(data)
            except:
                self.notify.warning('Received invalid JSON results: %s' % data)

            callback(data)

        return self.perform_post_request(
            url=url, 
            content_type='application/json',
            headers=headers,
            body=body, 
            callback=json_wrapper)

#----------------------------------------------------------------------------------------------------