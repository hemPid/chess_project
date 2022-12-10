import pubnub.pnconfiguration as pconf
import pubnub.pubnub as pb
import pubnub.callbacks as pcalls

class Connection:
    """docstring for Connection"""
    def __init__(self, channel, name, msg_event):
        self.channel_name = channel
        self.msg_event = msg_event
        self.config = pconf.PNConfiguration()
        self.config.subscribe_key = "sub-c-182b6c90-9414-497f-b25c-54129a5236f6"
        self.config.publish_key = "pub-c-5a754c49-a2b9-4cee-ab35-4e840cd37fdc"
        self.config.user_id = name
        #self.config.subscribe_request_timeout = 1
        self.pubnub = pb.PubNub(self.config)

    def write(self, message):
        self.pubnub.publish().\
            channel(self.channel_name).\
            message(message).sync()

    def connect(self):
        class MySubscribeCallback(pcalls.SubscribeCallback):
            def __init__(self, msg):
                self.msg = msg

            def message(self, pubnub, message):
                # Handle new message stored in message.message
                self.msg(message)

            def status(self, pubnub, status):
                if status.is_error():
                    print('error')
                else:
                    print('OK')
        self.listener = MySubscribeCallback(self.msg_event)
        self.pubnub.add_listener(self.listener)
        self.pubnub.subscribe().\
            channels(self.channel_name).execute()
        print('done')

    def disconnect(self):
        self.pubnub.remove_listener(self.listener)
        self.pubnub.unsubscribe().\
            channels(self.channel_name).execute()
        self.pubnub.stop()
        print('done')