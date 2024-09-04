#!/bin/bash

PROFILE_NAME="writeme"

PROFILE_EXISTS=$(minikube profile list --output json | jq -r --arg PROFILE_NAME "$PROFILE_NAME" '.valid | map(select(.Name == $PROFILE_NAME)) | length')

if [ "$PROFILE_EXISTS" -eq 1 ]; then
  minikube stop -p $PROFILE_NAME
  minikube delete -p $PROFILE_NAME
fi

minikube start -p $PROFILE_NAME

echo "Enabling Ingress addon..."
minikube addons enable ingress -p $PROFILE_NAME

echo "Cluster Ready!"
