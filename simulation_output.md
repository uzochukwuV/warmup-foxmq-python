Starting SwarmRescue-NG Scenario...
Starting local Python MQTT Broker on port 1883
[2026-04-05 23:49:54,465] :: WARNING :: amqtt.contexts :: sys_interval is deprecated, use 'plugins' to define configuration
[2026-04-05 23:49:54,466] :: WARNING :: amqtt.contexts :: 'auth' and 'topic-check' are deprecated, use 'plugins' to define configuration
/workspace/simple_broker.py:25: DeprecationWarning: Loading plugins from EntryPoints is deprecated and will be removed in a future version. Use `plugins` section of config instead.
  broker = Broker(config)
[2026-04-05 23:49:54,490] :: WARNING :: amqtt.broker.plugins.auth_file :: Configuration parameter 'password-file' not found
[2026-04-05 23:49:54,502] :: INFO :: transitions.core :: Executed callback '<bound method Broker._log_state_change of <amqtt.broker.Broker object at 0x7f2149621fd0>>'
[2026-04-05 23:49:54,502] :: INFO :: transitions.core :: Finished processing state new exit callbacks.
[2026-04-05 23:49:54,502] :: INFO :: transitions.core :: Finished processing state starting enter callbacks.
[2026-04-05 23:49:54,502] :: INFO :: amqtt.broker :: Listener 'default' bind to 0.0.0.0:1883 (max_connections=0)
[2026-04-05 23:49:54,502] :: INFO :: transitions.core :: Finished processing state starting exit callbacks.
[2026-04-05 23:49:54,503] :: INFO :: transitions.core :: Finished processing state started enter callbacks.
[2026-04-05 23:49:54,503] :: INFO :: amqtt.broker :: Starting session expiration monitor.
/workspace/hud_server.py:106: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  client = mqtt.Client(
[2026-04-05 23:49:56,467] :: INFO :: amqtt.broker :: Listener 'default': 1/∞ connections acquired
[2026-04-05 23:49:56,467] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:55625 on listener 'default'
All nodes started.
Open index.html in your browser to view the HUD.
Press Ctrl+C to stop all nodes.
/workspace/drone_agent.py:32: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
[2026-04-05 23:49:58,684] :: INFO :: amqtt.broker :: Listener 'default': 2/∞ connections acquired
[2026-04-05 23:49:58,687] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:56077 on listener 'default'
/workspace/drone_agent.py:32: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
[2026-04-05 23:49:58,706] :: INFO :: amqtt.broker :: Listener 'default': 3/∞ connections acquired
[2026-04-05 23:49:58,706] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:38043 on listener 'default'
/workspace/drone_agent.py:32: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
[2026-04-05 23:49:58,739] :: INFO :: amqtt.broker :: Listener 'default': 4/∞ connections acquired
[2026-04-05 23:49:58,739] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:51469 on listener 'default'
/workspace/drone_agent.py:32: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
[2026-04-05 23:49:58,747] :: INFO :: amqtt.broker :: Listener 'default': 5/∞ connections acquired
/workspace/drone_agent.py:32: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
[2026-04-05 23:49:58,747] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:41803 on listener 'default'
[2026-04-05 23:49:58,749] :: INFO :: amqtt.broker :: Listener 'default': 6/∞ connections acquired
[2026-04-05 23:49:58,749] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:55859 on listener 'default'
127.0.0.1 - - [05/Apr/2026 23:50:12] "GET / HTTP/1.1" 200 -
connection handler failed
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/websockets/asyncio/server.py", line 376, in conn_handler
    await self.handler(connection)
          ~~~~~~~~~~~~^^^^^^^^^^^^
TypeError: ws_handler() missing 1 required positional argument: 'path'
127.0.0.1 - - [05/Apr/2026 23:50:18] "GET /index.html?webview_request_time=1775433015002 HTTP/1.1" 200 -
[2026-04-05 23:50:56,529] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
[2026-04-05 23:50:57,529] :: INFO :: amqtt.broker :: Listener 'default': 7/∞ connections acquired
[2026-04-05 23:50:57,530] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:57427 on listener 'default'
[INFO] Connecting DroneAgent drone_02 to FoxMQ at 127.0.0.1:1883
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_02", "task": {"payload": {"sector": "NE"}, "requirements": {"max_latency_ms": 5000, "min_agents": 1, "redundancy": 1, "required_role": "any"}, "task_id": "SEARCH_NE_drone_02", "type": "RECOVERABLE_TASK"}, "ts": 1775433003682, "type": "TASK_CREATE"}, "sig": "8c1346d567a3c190c0a3c62ff56801b851e249aeb92e44633314c4db54dab53d"}
[drone_02] CRITICAL FAILURE INJECTED. Drone offline.
Traceback (most recent call last):
[2026-04-05 23:50:58,747] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=8 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
  File "/workspace/drone_agent.py", line 216, in <module>
    agent.start()
    ~~~~~~~~~~~^^
  File "/workspace/drone_agent.py", line 174, in start
    self.client.loop_forever()
    ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2297, in loop_forever
    rc = self._loop(timeout)
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 1707, in _loop
    return self.loop_misc()
           ~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2149, in loop_misc
    self._check_keepalive()
    ~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 3294, in _check_keepalive
    self._do_on_disconnect(
    ~~~~~~~~~~~~~~~~~~~~~~^
        packet_from_broker=False,
        ^^^^^^^^^^^^^^^^^^^^^^^^^
        v1_rc=rc,
        ^^^^^^^^^
    )
    ^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 4365, in _do_on_disconnect
    on_disconnect(self, self._userdata, v1_rc, None)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: on_disconnect() missing 1 required positional argument: 'properties'
[INFO] Connecting DroneAgent drone_01 to FoxMQ at 127.0.0.1:1883
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_01", "task": {"payload": {"sector": "NW"}, "requirements": {"max_latency_ms": 5000, "min_agents": 1, "redundancy": 1, "required_role": "any"}, "task_id": "SEARCH_NW_drone_01", "type": "RECOVERABLE_TASK"}, "ts": 1775433003709, "type": "TASK_CREATE"}, "sig": "6e7a3adf9af031092ac5d1e1531f2a9c9a429036c53edd0ebdbeecfe68b0dd2f"}
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_01", "position": [11, 11], "ts": 1775433018707, "type": "VICTIM_DETECTED"}, "sig": "33aabc07a33a41e7dff9744cb7721b61d72d66ab16b2ec1dcf8b1cb46d946431"}
[drone_01] Published VICTIM_DETECTED!
[2026-04-05 23:50:58,769] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=9 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
Traceback (most recent call last):
  File "/workspace/drone_agent.py", line 216, in <module>
    agent.start()
    ~~~~~~~~~~~^^
  File "/workspace/drone_agent.py", line 174, in start
    self.client.loop_forever()
    ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2297, in loop_forever
    rc = self._loop(timeout)
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 1707, in _loop
    return self.loop_misc()
           ~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2149, in loop_misc
    self._check_keepalive()
    ~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 3294, in _check_keepalive
    self._do_on_disconnect(
    ~~~~~~~~~~~~~~~~~~~~~~^
        packet_from_broker=False,
        ^^^^^^^^^^^^^^^^^^^^^^^^^
        v1_rc=rc,
        ^^^^^^^^^
    )
    ^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 4365, in _do_on_disconnect
    on_disconnect(self, self._userdata, v1_rc, None)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: on_disconnect() missing 1 required positional argument: 'properties'
[INFO] Connecting DroneAgent drone_04 to FoxMQ at 127.0.0.1:1883
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_04", "task": {"payload": {"sector": "SE"}, "requirements": {"max_latency_ms": 5000, "min_agents": 1, "redundancy": 1, "required_role": "any"}, "task_id": "SEARCH_SE_drone_04", "type": "RECOVERABLE_TASK"}, "ts": 1775433003739, "type": "TASK_CREATE"}, "sig": "5ea6cc865c50eb26cddf824118ebdb9885bfc5a5379a8272ca3d885bb9b1723a"}
[2026-04-05 23:50:58,798] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=10 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
Traceback (most recent call last):
  File "/workspace/drone_agent.py", line 216, in <module>
    agent.start()
    ~~~~~~~~~~~^^
  File "/workspace/drone_agent.py", line 174, in start
    self.client.loop_forever()
    ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2297, in loop_forever
    rc = self._loop(timeout)
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 1707, in _loop
    return self.loop_misc()
           ~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2149, in loop_misc
    self._check_keepalive()
    ~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 3294, in _check_keepalive
    self._do_on_disconnect(
    ~~~~~~~~~~~~~~~~~~~~~~^
        packet_from_broker=False,
        ^^^^^^^^^^^^^^^^^^^^^^^^^
        v1_rc=rc,
        ^^^^^^^^^
    )
    ^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 4365, in _do_on_disconnect
    on_disconnect(self, self._userdata, v1_rc, None)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: on_disconnect() missing 1 required positional argument: 'properties'
[INFO] Connecting DroneAgent drone_05 to FoxMQ at 127.0.0.1:1883
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_05", "task": {"payload": {"sector": "CENTER"}, "requirements": {"max_latency_ms": 5000, "min_agents": 1, "redundancy": 1, "required_role": "any"}, "task_id": "SEARCH_CENTER_drone_05", "type": "RECOVERABLE_TASK"}, "ts": 1775433003750, "type": "TASK_CREATE"}, "sig": "17d91b4fb2f762aae44aa77a7b434102ad6b09402a4884bb0e47d28282f3f609"}
[2026-04-05 23:50:58,809] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=12 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
Traceback (most recent call last):
[INFO] Connecting DroneAgent drone_03 to FoxMQ at 127.0.0.1:1883
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_03", "task": {"payload": {"sector": "SW"}, "requirements": {"max_latency_ms": 5000, "min_agents": 1, "redundancy": 1, "required_role": "any"}, "task_id": "SEARCH_SW_drone_03", "type": "RECOVERABLE_TASK"}, "ts": 1775433003747, "type": "TASK_CREATE"}, "sig": "f82febae2a77668b86cd0ca4009efe44cecd92c7e738b91e603c7b53167c0f80"}
  File "/workspace/drone_agent.py", line 216, in <module>
    agent.start()
    ~~~~~~~~~~~^^
Traceback (most recent call last):
[2026-04-05 23:50:58,812] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=11 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
  File "/workspace/drone_agent.py", line 174, in start
    self.client.loop_forever()
    ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2297, in loop_forever
    rc = self._loop(timeout)
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 1707, in _loop
    return self.loop_misc()
           ~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2149, in loop_misc
    self._check_keepalive()
    ~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 3294, in _check_keepalive
    self._do_on_disconnect(
    ~~~~~~~~~~~~~~~~~~~~~~^
        packet_from_broker=False,
        ^^^^^^^^^^^^^^^^^^^^^^^^^
        v1_rc=rc,
        ^^^^^^^^^
    )
    ^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 4365, in _do_on_disconnect
    on_disconnect(self, self._userdata, v1_rc, None)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: on_disconnect() missing 1 required positional argument: 'properties'
  File "/workspace/drone_agent.py", line 216, in <module>
    agent.start()
    ~~~~~~~~~~~^^
  File "/workspace/drone_agent.py", line 174, in start
    self.client.loop_forever()
    ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2297, in loop_forever
    rc = self._loop(timeout)
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 1707, in _loop
    return self.loop_misc()
           ~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2149, in loop_misc
    self._check_keepalive()
    ~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 3294, in _check_keepalive
    self._do_on_disconnect(
    ~~~~~~~~~~~~~~~~~~~~~~^
        packet_from_broker=False,
        ^^^^^^^^^^^^^^^^^^^^^^^^^
        v1_rc=rc,
        ^^^^^^^^^
    )
    ^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 4365, in _do_on_disconnect
    on_disconnect(self, self._userdata, v1_rc, None)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: on_disconnect() missing 1 required positional argument: 'properties'
127.0.0.1 - - [05/Apr/2026 23:51:04] "GET /index.html?webview_request_time=1775433063315 HTTP/1.1" 200 -
[2026-04-05 23:51:57,596] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
[2026-04-05 23:51:59,596] :: INFO :: amqtt.broker :: Listener 'default': 8/∞ connections acquired
[2026-04-05 23:51:59,596] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:46277 on listener 'default'
[2026-04-05 23:52:59,658] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
[2026-04-05 23:53:03,658] :: INFO :: amqtt.broker :: Listener 'default': 9/∞ connections acquired
[2026-04-05 23:53:03,659] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:33407 on listener 'default'
[2026-04-05 23:54:03,719] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
[2026-04-05 23:54:11,719] :: INFO :: amqtt.broker :: Listener 'default': 10/∞ connections acquired
[2026-04-05 23:54:11,719] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:59227 on listener 'default'
[2026-04-05 23:55:11,772] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
[2026-04-05 23:55:27,773] :: INFO :: amqtt.broker :: Listener 'default': 11/∞ connections acquired
[2026-04-05 23:55:27,773] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:56973 on listener 'default'
[2026-04-05 23:56:27,833] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
[2026-04-05 23:56:59,833] :: INFO :: amqtt.broker :: Listener 'default': 12/∞ connections acquired
[2026-04-05 23:56:59,833] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:41537 on listener 'default'
[2026-04-05 23:57:59,894] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
[2026-04-05 23:59:03,894] :: INFO :: amqtt.broker :: Listener 'default': 13/∞ connections acquired
[2026-04-05 23:59:03,895] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:52365 on listener 'default'
[2026-04-06 00:00:03,957] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
[2026-04-06 00:02:03,957] :: INFO :: amqtt.broker :: Listener 'default': 14/∞ connections acquired
[2026-04-06 00:02:03,958] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:57959 on listener 'default'
[2026-04-06 00:03:04,022] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
[2026-04-06 00:05:04,022] :: INFO :: amqtt.broker :: Listener 'default': 15/∞ connections acquired
[2026-04-06 00:05:04,022] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:44107 on listener 'default'
[2026-04-06 00:06:04,088] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
transport: <_SelectorSocketTransport fd=7 read=idle write=<idle, bufsize=0>>
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 430, in stream_connected
    await self._client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer))
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 453, in _client_connected
    handler, client_session = await self._initialize_client_session(reader, writer, remote_address, remote_port)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/broker.py", line 477, in _initialize_client_session
    handler, client_session = await BrokerProtocolHandler.init_from_connect(reader, writer, self.plugins_manager)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/mqtt/protocol/broker_handler.py", line 224, in init_from_connect
    await writer.close()
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/amqtt/adapters.py", line 191, in close
    self._writer.write_eof()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/streams.py", line 346, in write_eof
    return self._transport.write_eof()
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/asyncio/selector_events.py", line 1168, in write_eof
    self._sock.shutdown(socket.SHUT_WR)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
OSError: [Errno 107] Transport endpoint is not connected
