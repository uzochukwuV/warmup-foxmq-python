import asyncio
import logging
from amqtt.broker import Broker

logger = logging.getLogger(__name__)

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '127.0.0.1:1883'
        },
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True,
        'plugins': ['auth_anonymous']
    },
    'topic-check': {
        'enabled': False
    }
}

async def main():
    broker = Broker(config)
    await broker.start()
    
    # Run forever
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass