from diagrams import Cluster, Diagram
from diagrams.onprem.

with Diagram("Project", show=False):
    with Cluster("Swarm Cluster") as cluster:
        Docker("Manager") >> Docker("Worker 1") >> Docker("Worder 2")
