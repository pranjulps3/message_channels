from channels.routing import route
from chat_messages.consumers import message, add, disconnect

channel_routing = [
    # route("http.request", first_channel),
    route("websocket.connect", add),    				#path="r^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", disconnect), 		#path="r^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.receive", message), 			#path="r^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
]
