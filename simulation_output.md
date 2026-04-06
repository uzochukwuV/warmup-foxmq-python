Starting SwarmRescue-NG Scenario...
Starting local Python MQTT Broker on port 1883
[2026-04-06 00:12:24,757] :: WARNING :: amqtt.contexts :: sys_interval is deprecated, use 'plugins' to define configuration
[2026-04-06 00:12:24,757] :: WARNING :: amqtt.contexts :: 'auth' and 'topic-check' are deprecated, use 'plugins' to define configuration
/workspace/simple_broker.py:26: DeprecationWarning: Loading plugins from EntryPoints is deprecated and will be removed in a future version. Use `plugins` section of config instead.
  broker = Broker(config)
[2026-04-06 00:12:24,781] :: INFO :: amqtt.broker.plugins.auth_file :: 1 user(s) loaded from passwd
[2026-04-06 00:12:24,794] :: INFO :: transitions.core :: Executed callback '<bound method Broker._log_state_change of <amqtt.broker.Broker object at 0x7f1847abdfd0>>'
[2026-04-06 00:12:24,794] :: INFO :: transitions.core :: Finished processing state new exit callbacks.
[2026-04-06 00:12:24,794] :: INFO :: transitions.core :: Finished processing state starting enter callbacks.
[2026-04-06 00:12:24,794] :: INFO :: amqtt.broker :: Listener 'default' bind to 127.0.0.1:1883 (max_connections=0)
[2026-04-06 00:12:24,794] :: INFO :: transitions.core :: Finished processing state starting exit callbacks.
[2026-04-06 00:12:24,794] :: INFO :: transitions.core :: Finished processing state started enter callbacks.
[2026-04-06 00:12:24,795] :: INFO :: amqtt.broker :: Starting session expiration monitor.
/workspace/hud_server.py:126: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  client = mqtt.Client(
[2026-04-06 00:12:26,749] :: INFO :: amqtt.broker :: Listener 'default': 1/∞ connections acquired
[2026-04-06 00:12:26,750] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:38585 on listener 'default'
All nodes started.
Open index.html in your browser to view the HUD.
Press Ctrl+C to stop all nodes.
/workspace/drone_agent.py:33: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
[2026-04-06 00:12:28,964] :: INFO :: amqtt.broker :: Listener 'default': 2/∞ connections acquired
[2026-04-06 00:12:28,965] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:55593 on listener 'default'
/workspace/drone_agent.py:33: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
[2026-04-06 00:12:28,996] :: INFO :: amqtt.broker :: Listener 'default': 3/∞ connections acquired
[2026-04-06 00:12:28,997] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:54185 on listener 'default'
/workspace/drone_agent.py:33: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
[2026-04-06 00:12:29,007] :: INFO :: amqtt.broker :: Listener 'default': 4/∞ connections acquired
[2026-04-06 00:12:29,007] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:35413 on listener 'default'
/workspace/drone_agent.py:33: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
/workspace/drone_agent.py:33: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  self.client = mqtt.Client(
[2026-04-06 00:12:29,031] :: INFO :: amqtt.broker :: Listener 'default': 5/∞ connections acquired
[2026-04-06 00:12:29,032] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:58633 on listener 'default'
[2026-04-06 00:12:29,032] :: INFO :: amqtt.broker :: Listener 'default': 6/∞ connections acquired
[2026-04-06 00:12:29,032] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:60435 on listener 'default'
127.0.0.1 - - [06/Apr/2026 00:12:44] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [06/Apr/2026 00:12:47] "GET /index.html?webview_request_time=1775434366221 HTTP/1.1" 200 -
[2026-04-06 00:12:59,010] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
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
[2026-04-06 00:13:26,812] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
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
[2026-04-06 00:13:27,812] :: INFO :: amqtt.broker :: Listener 'default': 7/∞ connections acquired
[2026-04-06 00:13:27,813] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:43073 on listener 'default'
[INFO] Connecting DroneAgent drone_05 to FoxMQ at 127.0.0.1:1883
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_05", "task": {"payload": {"sector": "CENTER"}, "requirements": {"max_latency_ms": 5000, "min_agents": 1, "redundancy": 1, "required_role": "any"}, "task_id": "SEARCH_CENTER_drone_05", "type": "RECOVERABLE_TASK"}, "ts": 1775434353963, "type": "TASK_CREATE"}, "sig": "ddd6756d3b848387a9fe78ce2727d4b570d4d023a138220cfe31c0d32bace390"}
Traceback (most recent call last):
[2026-04-06 00:13:29,024] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
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
  File "/workspace/drone_agent.py", line 219, in <module>
    agent.start()
    ~~~~~~~~~~~^^
  File "/workspace/drone_agent.py", line 177, in start
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
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_01", "task": {"payload": {"sector": "NW"}, "requirements": {"max_latency_ms": 5000, "min_agents": 1, "redundancy": 1, "required_role": "any"}, "task_id": "SEARCH_NW_drone_01", "type": "RECOVERABLE_TASK"}, "ts": 1775434353996, "type": "TASK_CREATE"}, "sig": "6a96c63cd7a6a2ad77530112170e2b97ede98473a3d8ef370b392840b8263871"}
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_01", "position": [11, 11], "ts": 1775434368997, "type": "VICTIM_DETECTED"}, "sig": "71c22bb85221841e39f70f3ea3c7c211e650572ef45168f91d3d828887977a6a"}
[drone_01] Published VICTIM_DETECTED!
[2026-04-06 00:13:29,057] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
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
  File "/workspace/drone_agent.py", line 219, in <module>
    agent.start()
    ~~~~~~~~~~~^^
  File "/workspace/drone_agent.py", line 177, in start
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
[INFO] Connecting DroneAgent drone_03 to FoxMQ at 127.0.0.1:1883
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_03", "task": {"payload": {"sector": "SW"}, "requirements": {"max_latency_ms": 5000, "min_agents": 1, "redundancy": 1, "required_role": "any"}, "task_id": "SEARCH_SW_drone_03", "type": "RECOVERABLE_TASK"}, "ts": 1775434354032, "type": "TASK_CREATE"}, "sig": "9423c32b6edb3cd7703be98aad516153595738eb2699448e4a1fd616250078b6"}
[2026-04-06 00:13:29,093] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
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
[INFO] Connecting DroneAgent drone_04 to FoxMQ at 127.0.0.1:1883
[SEND] topic=swarm/state  payload={"payload": {"peer_id": "drone_04", "task": {"payload": {"sector": "SE"}, "requirements": {"max_latency_ms": 5000, "min_agents": 1, "redundancy": 1, "required_role": "any"}, "task_id": "SEARCH_SE_drone_04", "type": "RECOVERABLE_TASK"}, "ts": 1775434354032, "type": "TASK_CREATE"}, "sig": "67a54fe1f9b034163902309e3bf683953927bc7da96c347a13dca3bdaaf006ef"}
Traceback (most recent call last):
  File "/workspace/drone_agent.py", line 219, in <module>
    agent.start()
    ~~~~~~~~~~~^^
  File "/workspace/drone_agent.py", line 177, in start
    self.client.loop_forever()
    ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/root/.pyenv/versions/3.14.3/lib/python3.14/site-packages/paho/mqtt/client.py", line 2297, in loop_forever
    rc = self._loop(timeout)
[2026-04-06 00:13:29,094] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
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
Traceback (most recent call last):
TypeError: on_disconnect() missing 1 required positional argument: 'properties'
  File "/workspace/drone_agent.py", line 219, in <module>
    agent.start()
    ~~~~~~~~~~~^^
  File "/workspace/drone_agent.py", line 177, in start
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
[2026-04-06 00:14:27,876] :: ERROR :: asyncio :: Unhandled exception in client_connected_cb
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
[2026-04-06 00:14:29,876] :: INFO :: amqtt.broker :: Listener 'default': 8/∞ connections acquired
[2026-04-06 00:14:29,877] :: INFO :: amqtt.broker :: Connection from 127.0.0.1:47859 on listener 'default'
./run_scenario.sh: line 1: kill: (3824) - No such process
./run_scenario.sh: line 1: kill: (3909) - No such process
./run_scenario.sh: line 1: kill: (3910) - No such process
./run_scenario.sh: line 1: kill: (4083) - No such process
