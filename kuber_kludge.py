#!/usr/bin/env python3.11

import argparse
import random
import time
import os
import logging
from kubernetes import client, config

def setup_logging():
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    logging.basicConfig(filename=os.path.join(logs_dir, "kuber_kludge.log"), level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def terminate_eks_pods(kubeconfig_path, namespace, pod_count, delete_sidecar, delete_ingress, delete_service):
    try:
        # Load kubeconfig for EKS cluster
        config.load_kube_config(config_file=kubeconfig_path)

        # Create Kubernetes API client
        api_instance = client.CoreV1Api()

        # Get list of pods in the specified namespace
        pods = api_instance.list_namespaced_pod(namespace=namespace).items

        # Select random pods to terminate
        pods_to_terminate = random.sample(pods, min(pod_count, len(pods)))

        # Delete selected pods
        for pod in pods_to_terminate:
            logging.info(f"Terminating pod: {pod.metadata.name}")
            print(f"Terminating pod: {pod.metadata.name}")
            api_instance.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace, body=client.V1DeleteOptions())

        # Delete random sidecars, ingresses, and services
        if delete_sidecar:
            # Delete random sidecar containers
            logging.info("Deleting a random sidecar container")
            print("Deleting a random sidecar container")
            # Your logic to delete sidecars
        if delete_ingress:
            # Delete random ingresses
            logging.info("Deleting a random ingress")
            print("Deleting a random ingress")
            # Your logic to delete ingresses
        if delete_service:
            # Delete random services
            logging.info("Deleting a random service")
            print("Deleting a random service")
            # Your logic to delete services

        return True
    except Exception as e:
        logging.error("Error terminating EKS pods:", exc_info=True)
        print("Error terminating EKS pods:", e)
        return False

def main():
    parser = argparse.ArgumentParser(description="Kubernetes Pod Kludge - Simulate chaos by terminating Kubernetes pods")
    parser.add_argument("--kubeconfig", type=str, help="Path to kubeconfig file for EKS cluster")
    parser.add_argument("--namespace", type=str, default="default", help="Kubernetes namespace")
    parser.add_argument("--pod-count", type=int, default=1, help="Number of pods to terminate")
    parser.add_argument("--delete-sidecar", action="store_true", help="Randomly delete a sidecar container")
    parser.add_argument("--delete-ingress", action="store_true", help="Randomly delete an ingress")
    parser.add_argument("--delete-service", action="store_true", help="Randomly delete a service")
    args = parser.parse_args()

    setup_logging()

    if args.kubeconfig:
        # Terminate pods in AWS EKS cluster
        if terminate_eks_pods(args.kubeconfig, args.namespace, args.pod_count, args.delete_sidecar, args.delete_ingress, args.delete_service):
            print("Pod termination initiated. Waiting for pods to terminate...")
            logging.info("Pod termination initiated. Waiting for pods to terminate...")
            # Wait for pods to terminate
            time.sleep(5)
            print("Pod termination completed.")
            logging.info("Pod termination completed.")
            exit(0)
        else:
            exit(1)
    else:
        print("Kubeconfig path not provided. Please specify the path to kubeconfig file.")
        logging.error("Kubeconfig path not provided.")
        exit(1)

if __name__ == "__main__":
    main()
