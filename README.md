# Kuber Kludge

Kuber Kludge is a chaos engineering tool designed to simulate chaos in Kubernetes clusters by terminating pods and performing other disruptive actions.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/davestj/kuber_kludge.git
    ```

2. Navigate to the `kuber_kludge` directory:

    ```bash
    cd kuber_kludge
    ```

3. Ensure you have Python 3.11 installed. If not, install it using your package manager or download it from the [official Python website](https://www.python.org/).

4. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Make sure to have your Kubernetes configuration (`kubeconfig`) file ready. You can then use the script directly from the command line.

```bash
#!/usr/bin/env python3.11

usage: kuber_kludge.py [-h] [--kubeconfig KUBECONFIG] [--namespace NAMESPACE]
                       [--pod-count POD_COUNT] [--delete-sidecar] [--delete-ingress]
                       [--delete-service] [--delete-configmap] [--delete-cronjob]

Kubernetes Pod Kludge - Simulate chaos by terminating Kubernetes pods

optional arguments:
  -h, --help            show this help message and exit
  --kubeconfig KUBECONFIG
                        Path to kubeconfig file for EKS cluster
  --namespace NAMESPACE
                        Kubernetes namespace (default: "default")
  --pod-count POD_COUNT
                        Number of pods to terminate (default: 1)
  --delete-sidecar      Randomly delete a sidecar container
  --delete-ingress      Randomly delete an ingress
  --delete-service      Randomly delete a service
  --delete-configmap    Randomly delete a config map
  --delete-cronjob      Randomly delete a cron job
```

## Examples

Terminate pods and delete a random sidecar container:

```bash
./kuber_kludge.py --kubeconfig /path/to/kubeconfig --delete-sidecar
```

Terminate pods and delete a random service:

```bash
./kuber_kludge.py --kubeconfig /path/to/kubeconfig --delete-service
```

Terminate pods and delete a random config map:

```bash
./kuber_kludge.py --kubeconfig /path/to/kubeconfig --delete-configmap
```

## Contributing

---

Contributions are welcome! Please feel free to open a pull request for any improvements or additional features you'd like to add.

---