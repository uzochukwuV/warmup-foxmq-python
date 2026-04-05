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
