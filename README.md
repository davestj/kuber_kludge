# Kuber Kludge

## Introduction

Kuber Kludge is a chaos engineering tool designed to simulate chaos by terminating Kubernetes pods and other resources. With Kuber Kludge, you can test the resilience of your Kubernetes clusters, identify weaknesses, and improve fault tolerance in your applications.

## Features

- **Random Pod Termination:** Simulate chaos by randomly terminating Kubernetes pods in your cluster.
- **Resource Deletion:** Optionally delete sidecar containers, ingresses, or services to further simulate chaos.

## Getting Started

To get started with Kuber Kludge, follow these steps:

### Prerequisites

- Python 3.x installed on your system, development was done on  MacOS Python 3.11 installed with brew.
- Access to a Kubernetes cluster, either AWS EKS or standalone.

### Installation

1. Clone the Kuber Kludge repository:

   ```bash
   git clone https://github.com/davestj/kuber_kludge.git
   ```

2. Navigate to the cloned directory:

   ```bash
   cd kuber_kludge
   ```

3. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

To run Kuber Kludge, use the following command-line arguments:

```bash
python kuber_kludge.py --kubeconfig <path-to-kubeconfig> --namespace <namespace> --pod-count <number-of-pods> --delete-sidecar --delete-ingress --delete-service
```

Replace `<path-to-kubeconfig>` with the path to your Kubernetes cluster's kubeconfig file, `<namespace>` with the desired Kubernetes namespace, and `<number-of-pods>` with the number of pods to terminate.

Use the `--delete-sidecar`, `--delete-ingress`, and `--delete-service` flags to specify whether to randomly delete a sidecar container, ingress, or service, respectively.

### Example

Terminate 3 pods in the `default` namespace of an AWS EKS cluster, and randomly delete a sidecar container:

```bash
python kuber_kludge.py --kubeconfig ~/.kube/config --namespace default --pod-count 3 --delete-sidecar
```

## Contributing

If you encounter any issues or have ideas for improvements, feel free to open an issue or submit a pull request on [GitHub](https://github.com/davestj/kuber_kludge).

## License

Kuber Kludge is licensed under the [MIT License](LICENSE), allowing for unrestricted use, modification, and distribution.

---