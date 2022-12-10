import pubnub.pnconfiguration as pconf
import pubnub.pubnub as pb
import pubnub.callbacks as pcalls


class Connection:
    """
    класс создания соединения с каналами pubnub
    """
    def __init__(self, channel, name, msg_event, conn_event):
        """
        init
        Args:
        channel - канал, к которому идёт подключение
        name - имя пользователя, от имени которого подключаемся
        msg_event - обработчик соьытий призода сообщений
        conn_event - обработчик события присоединения к каналу
        """
        self.channel_name = channel
        self.msg_event = msg_event
        self.conn_event = conn_event
        self.config = pconf.PNConfiguration()
        self.config.\
            subscribe_key = "sub-c-d23026ff-4f53-4301-8078-f382b3af9fa1"
        self.config.\
            publish_key = "pub-c-b69bc4ea-dffe-4a06-8302-1ed1c7aac999"
        self.config.user_id = name
        self.pubnub = pb.PubNub(self.config)

    def write(self, message):
        """
        Пишет сообщения в канал
        Args:
        message - передаваемое сообщение
        """
        self.pubnub.publish().\
            channel(self.channel_name).\
            message(message).sync()

    def connect(self):
        """
        Подписывается на канал
        """
        class MySubscribeCallback(pcalls.SubscribeCallback):
            def __init__(self, msg_ev, conn_ev):
                # инициализация обработчиков
                self.msg = msg_ev
                self.conn = conn_ev

            def message(self, pubnub, message):
                # обработчик прихода сообщений
                self.msg(message)

            def status(self, pubnub, status):
                # обработчик подписки на канал
                if status.is_error():
                    print('error')
                else:
                    self.conn()
        self.listener = MySubscribeCallback(self.msg_event, self.conn_event)
        self.pubnub.add_listener(self.listener)
        self.pubnub.subscribe().\
            channels(self.channel_name).execute()

    def disconnect(self):
        """
        отключение от канала
        """
        self.pubnub.remove_listener(self.listener)
        self.pubnub.unsubscribe().\
            channels(self.channel_name).execute()
        self.pubnub.stop()
        print('done')
