#!/bin/bash

# Function to wait for RabbitMQ to start
wait_for_rabbitmq() {
    echo "Waiting for RabbitMQ to start..."
    RETRY_COUNT=0
    MAX_RETRIES=30
    while ! rabbitmqctl wait --timeout 30000 /var/lib/rabbitmq/mnesia/rabbit@$HOSTNAME.pid; do
        echo "Waiting for RabbitMQ to fully start..."
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
            echo "RabbitMQ did not start after $MAX_RETRIES attempts. Exiting..."
            exit 1
        fi
        sleep 1
    done
}

# Ensure the hostname is correctly set
export HOSTNAME=$(hostname)
echo "Current HOSTNAME is $HOSTNAME"

echo "Starting RabbitMQ configuration..."

# Wait for RabbitMQ to fully start before configuring
wait_for_rabbitmq

echo "RabbitMQ is up, setting up initial configuration..."

# Create user and set permissions
if rabbitmqctl add_user myuser mypassword; then
    echo "User myuser created"
else
    echo "User myuser already exists, skipping creation."
fi

rabbitmqctl set_user_tags myuser administrator
rabbitmqctl set_permissions -p / myuser ".*" ".*" ".*"

echo "Declaring durable queues..."

# Download and install rabbitmqadmin if not present
if [ ! -f /usr/local/bin/rabbitmqadmin ]; then
    wget http://localhost:15672/cli/rabbitmqadmin -O /usr/local/bin/rabbitmqadmin
    chmod +x /usr/local/bin/rabbitmqadmin
fi

# Declare queues with rabbitmqadmin
/usr/local/bin/rabbitmqadmin declare queue name=repo durable=true
/usr/local/bin/rabbitmqadmin declare queue name=readme durable=true

# Configure file descriptors limit
echo "Increasing file descriptors limit..."
echo "ulimit -n 65536" >> /etc/default/rabbitmq-server

# Enable detailed logging
echo "Enabling detailed logging..."
rabbitmqctl set_log_level debug

# Set heartbeat interval and disable loopback users for development
echo "Configuring RabbitMQ..."
echo "loopback_users = none" >> /etc/rabbitmq/rabbitmq.conf
echo "heartbeat = 60" >> /etc/rabbitmq/rabbitmq.conf

echo "RabbitMQ configuration completed."

# Keep the script running to avoid container exiting
tail -f /dev/null

