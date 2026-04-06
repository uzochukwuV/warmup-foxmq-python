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
