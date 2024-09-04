#!/bin/bash

# USED FOR BUILDING NOT FOR END USER

cd ~/Documents/code/personal/writeme

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
    
    cd "$path" || { echo "Failed to navigate to $path"; exit 1; }
    
    docker build -t "$image" .

    cd - || exit

done

for service in "${services[@]}"; do
    IFS=':' read -r name path image <<< "$service"
    
    cd "$path" || { echo "Failed to navigate to $path"; exit 1; }

    docker push "$image"
   
    cd - || exit

done

echo "All images have been built and pushed successfully."

cd ~/Documents/code/personal/writeme/manifests

kubectl delete -f . --recursive 

kubectl apply -f . --recursive

if [ $? -eq 0 ]; then
  echo "All manifests reapplied successfully."
else
  echo "An error occurred during reapplication of manifests."
fi

