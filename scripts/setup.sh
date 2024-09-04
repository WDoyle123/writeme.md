#!/bin/bash

check_pods_status() {
    echo "Checking if all pods are in 'Running' state..."
    all_running=false

    sleep 5

    while [ "$all_running" = false ]; do
        pod_status=$(kubectl get pods --no-headers | awk '{print $3}' | grep -v "Running")
        
        if [ -z "$pod_status" ]; then
            all_running=true
            echo "All pods are in 'Running' state."
        else
            echo "Waiting for all pods to be in 'Running' state..."
            sleep 5
        fi
    done
}

echo "Have you added '127.0.0.1 writeme.com' to /etc/hosts? & added the google password to the manifest ../manifest/notifications/readme-notifications-secret.yaml ?"
echo "If not, see README.md..."
echo ""
read -p "Press Enter to continue..."

. create_cluster.sh

sleep 3

services=(
    "gateway:./services/gateway:wdoyle123/readme-gateway"
    "mongodb:./services/mongodb:wdoyle123/readme-mongodb"
    "msautogen:./services/msautogen:wdoyle123/readme-msautogen"
    "notifications:./services/notifications:wdoyle123/readme-notifications"
    "rabbitmq:./services/rabbitmq:wdoyle123/readme-rabbitmq"
    "readme_website:./services/readme_website:wdoyle123/readme-website"
    "upload-download:./services/upload-download:wdoyle123/readme-upload-download"
)

for service in "${services[@]}"; do
    IFS=':' read -r name path image <<< "$service"
    
    echo "Pulling image for $name..."
    
    docker pull "$image"
    
    if [ $? -eq 0 ]; then
      echo "Successfully pulled $image for $name"
    else
      echo "Failed to pull $image for $name"
      exit 1
    fi
done

echo "All images have been pulled successfully."

cd ../manifests

kubectl delete -f . --recursive &> /dev/null
kubectl apply -f . --recursive

if [ $? -eq 0 ]; then
  echo "All manifests reapplied successfully."
else
  echo "An error occurred during the application of manifests."
fi

check_pods_status

sleep 3

if open http://writeme.com; then
    echo "Opening browser..."
else
    echo "Failed to open the browser. Please visit https://www.writeme.com manually."
fi

echo "You might need to reload the browser!"

sleep 2

minikube tunnel -p writeme 

