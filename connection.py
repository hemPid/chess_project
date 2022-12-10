import pubnub.pnconfiguration as pconf
import pubnub.pubnub as pb
import pubnub.callbacks as pcalls


class Connection:
    """docstring for Connection"""
    def __init__(self, channel, name, msg_event, conn_event):
        self.channel_name = channel
        self.msg_event = msg_event
        self.conn_event = conn_event
        self.config = pconf.PNConfiguration()
        self.config.\
            subscribe_key = "sub-c-d23026ff-4f53-4301-8078-f382b3af9fa1"
        self.config.\
            publish_key = "pub-c-b69bc4ea-dffe-4a06-8302-1ed1c7aac999"
        self.config.user_id = name
        # self.config.subscribe_request_timeout = 1
        self.pubnub = pb.PubNub(self.config)

    def write(self, message):
        self.pubnub.publish().\
            channel(self.channel_name).\
            message(message).sync()

    def connect(self):
        class MySubscribeCallback(pcalls.SubscribeCallback):
            def __init__(self, msg_ev, conn_ev):
                self.msg = msg_ev
                self.conn = conn_ev

            def message(self, pubnub, message):
                # Handle new message stored in message.message
                self.msg(message)

            def status(self, pubnub, status):
                if status.is_error():
                    print('error')
                else:
                    print('OK')
                    self.conn()
        self.listener = MySubscribeCallback(self.msg_event, self.conn_event)
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
