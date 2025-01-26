from diagrams import Cluster, Diagram
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import NodeJS, Python, Csharp
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.client import Users

with Diagram("Project", show=False):
    users = Users("Clients")
    with Cluster("Swarm Cluster") as cluster:
        result = NodeJS("Result App")
        vote = Python("Vote App")
        worker = Csharp("Worker App")
        db = PostgreSQL("Database")
        cache = Redis("Redis")
        [result, vote, worker] >> db
        [result, vote, worker] >> cache
        users >> [result, vote]