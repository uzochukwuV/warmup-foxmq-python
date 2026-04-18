#!/bin/bash

# Official FoxMQ Installation for Linux
echo "Downloading FoxMQ v0.3.1 for Linux..."
curl -LO https://github.com/tashigit/foxmq/releases/download/v0.3.1/foxmq_0.3.1_linux-amd64.zip

echo "Unzipping FoxMQ..."
unzip -o foxmq_0.3.1_linux-amd64.zip
chmod +x foxmq

echo "Setting up single node FoxMQ cluster..."
./foxmq address-book from-range 127.0.0.1 19793 19793

# Assuming user add will create the users.toml and we can bypass interactivity
# We will use 'producer' and 'password' as defaults, matching run_scenario.sh
echo "Note: You must manually add a user using: ./foxmq user add"
echo "Recommended: username 'producer', password 'password'"

echo "To start the broker:"
echo "./foxmq run --secret-key-file=foxmq.d/key_0.pem &"
