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
    logging.basicConfig(filename=os.path.join(logs_dir, "kuber_kludge.log"), level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def delete_sidecar(api_instance, namespace):
    try:
        # Get list of pods in the specified namespace
        pods = api_instance.list_namespaced_pod(namespace=namespace).items

        # Select a random pod
        pod = random.choice(pods)

        # Check if the pod has sidecar containers
        if pod.spec.containers and len(pod.spec.containers) > 1:
            # Select a random sidecar container to delete
            sidecar_container = random.choice(pod.spec.containers[1:])
            container_name = sidecar_container.name

            # Delete the selected sidecar container
            api_instance.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace, body=client.V1DeleteOptions())

            logging.info(f"Deleted sidecar container '{container_name}' from pod '{pod.metadata.name}'")
            print(f"Deleted sidecar container '{container_name}' from pod '{pod.metadata.name}'")
            return True
        else:
            logging.info("No sidecar containers found in the namespace")
            print("No sidecar containers found in the namespace")
            return False
    except Exception as e:
        logging.error("Error deleting sidecar container:", exc_info=True)
        print("Error deleting sidecar container:", e)
        return False

def delete_ingress(api_instance, namespace):
    try:
        # Get list of ingresses in the specified namespace
        ingresses = api_instance.list_namespaced_ingress(namespace=namespace).items

        # Select a random ingress to delete
        if ingresses:
            ingress = random.choice(ingresses)

            # Delete the selected ingress
            api_instance.delete_namespaced_ingress(name=ingress.metadata.name, namespace=namespace, body=client.V1DeleteOptions())

            logging.info(f"Deleted ingress '{ingress.metadata.name}'")
            print(f"Deleted ingress '{ingress.metadata.name}'")
            return True
        else:
            logging.info("No ingresses found in the namespace")
            print("No ingresses found in the namespace")
            return False
    except Exception as e:
        logging.error("Error deleting ingress:", exc_info=True)
        print("Error deleting ingress:", e)
        return False

def delete_cron_job(api_instance, namespace):
    try:
        # Get list of pods in the specified namespace
        pods = api_instance.list_namespaced_pod(namespace=namespace).items

        # Filter pods with cron jobs
        pods_with_cronjobs = [pod for pod in pods if any(container.name == "cronjob-container" for container in pod.spec.containers)]

        # Select a random pod with cron job
        if pods_with_cronjobs:
            pod = random.choice(pods_with_cronjobs)

            # Delete the cron job container
            cronjob_container = next(container for container in pod.spec.containers if container.name == "cronjob-container")
            api_instance.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace, body=client.V1DeleteOptions())

            logging.info(f"Deleted cron job in pod '{pod.metadata.name}'")
            print(f"Deleted cron job in pod '{pod.metadata.name}'")
            return True
        else:
            logging.info("No pods with cron jobs found in the namespace")
            print("No pods with cron jobs found in the namespace")
            return False
    except Exception as e:
        logging.error("Error deleting cron job:", exc_info=True)
        print("Error deleting cron job:", e)
        return False

def delete_service(api_instance, namespace, pod_specific=False):
    try:
        if pod_specific:
            # Get list of pods in the specified namespace
            pods = api_instance.list_namespaced_pod(namespace=namespace).items

            # Select a random pod
            pod = random.choice(pods)

            # Get services associated with the selected pod
            pod_services = api_instance.list_namespaced_service(namespace=namespace, label_selector=f"pod={pod.metadata.name}").items

            # Select a random service from the pod's services
            if pod_services:
                service = random.choice(pod_services)

                # Delete the selected service
                api_instance.delete_namespaced_service(name=service.metadata.name, namespace=namespace, body=client.V1DeleteOptions())

                logging.info(f"Deleted service '{service.metadata.name}' associated with pod '{pod.metadata.name}'")
                print(f"Deleted service '{service.metadata.name}' associated with pod '{pod.metadata.name}'")
                return True
            else:
                logging.info(f"No services associated with pod '{pod.metadata.name}'")
                print(f"No services associated with pod '{pod.metadata.name}'")
                return False
        else:
            # Get list of all services in the specified namespace
            services = api_instance.list_namespaced_service(namespace=namespace).items

            # Select a random service from all services
            if services:
                service = random.choice(services)

                # Delete the selected service
                api_instance.delete_namespaced_service(name=service.metadata.name, namespace=namespace, body=client.V1DeleteOptions())

                logging.info(f"Deleted service '{service.metadata.name}'")
                print(f"Deleted service '{service.metadata.name}'")
                return True
            else:
                logging.info("No services found in the namespace")
                print("No services found in the namespace")
                return False
    except Exception as e:
        logging.error("Error deleting service:", exc_info=True)
        print("Error deleting service:", e)
        return False

def delete_config_map(api_instance, namespace):
    try:
        # Get list of pods in the specified namespace
        pods = api_instance.list_namespaced_pod(namespace=namespace).items

        # Filter pods with config maps
        pods_with_configmaps = [pod for pod in pods if any(volume.config_map for volume in pod.spec.volumes)]

        # Select a random pod with config map
        if pods_with_configmaps:
            pod = random.choice(pods_with_configmaps)

            # Get config maps associated with the selected pod
            pod_configmaps = [volume.config_map.name for volume in pod.spec.volumes if volume.config_map]

            # Select a random config map from the pod's config maps
            configmap_name = random.choice(pod_configmaps)

            # Delete the selected config map
            api_instance.delete_namespaced_config_map(name=configmap_name, namespace=namespace, body=client.V1DeleteOptions())

            logging.info(f"Deleted config map '{configmap_name}' associated with pod '{pod.metadata.name}'")
            print(f"Deleted config map '{configmap_name}' associated with pod '{pod.metadata.name}'")
            return True
        else:
            logging.info("No pods with config maps found in the namespace")
            print("No pods with config maps found in the namespace")
            return False
    except Exception as e:
        logging.error("Error deleting config map:", exc_info=True)
        print("Error deleting config map:", e)
        return False

def terminate_eks_pods(kubeconfig_path, namespace, pod_count, delete_sidecar, delete_ingress, delete_service, delete_configmap, delete_cronjob):
    try:
        # Load kubeconfig for EKS cluster
        config.load_kube_config(config_file=kubeconfig_path)

        # Create Kubernetes API clients
        api_instance = client.CoreV1Api()
        batch_api_instance = client.BatchV1beta1Api()

        # Get list of pods in the specified namespace
        pods = api_instance.list_namespaced_pod(namespace=namespace).items

        # Select random pods to terminate
        pods_to_terminate = random.sample(pods, min(pod_count, len(pods)))

        # Delete selected pods
        for pod in pods_to_terminate:
            logging.info(f"Terminating pod: {pod.metadata.name}")
            print(f"Terminating pod: {pod.metadata.name}")
            api_instance.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace, body=client.V1DeleteOptions())

        # Delete random sidecars, ingresses, services, config maps, and cron jobs
        if delete_sidecar:
            # Delete random sidecar containers
            delete_sidecar(api_instance, namespace)
        if delete_ingress:
            # Delete random ingresses
            delete_ingress(api_instance, namespace)
        if delete_service:
            # Delete random services
            delete_service(api_instance, namespace, pod_specific=random.choice([True, False]))
        if delete_configmap:
            # Delete random config maps
            delete_config_map(api_instance, namespace)
        if delete_cronjob:
            # Delete random cron jobs
            delete_cron_job(api_instance, namespace)

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
    parser.add_argument("--delete-configmap", action="store_true", help="Randomly delete a config map")
    parser.add_argument("--delete-cronjob", action="store_true", help="Randomly delete a cron job")
    args = parser.parse_args()

    setup_logging()

    if args.kubeconfig:
        # Terminate pods in AWS EKS cluster
        if terminate_eks_pods(args.kubeconfig, args.namespace, args.pod_count, args.delete_sidecar, args.delete_ingress, args.delete_service, args.delete_configmap, args.delete_cronjob):
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
