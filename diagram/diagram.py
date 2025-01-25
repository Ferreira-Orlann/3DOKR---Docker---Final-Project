from diagrams import Cluster, Diagram
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import NodeJS, Python, Csharp
from diagrams.onprem.inmemory import Redis

with Diagram("Project", show=False):
    with Cluster("Swarm Cluster") as cluster:
        
        with Cluster("Web Network"):
            nodejs = NodeJS("Result App")
            vote = Python("Vote App")
        with Cluster("Internal Network"):
            vote = Csharp("Worker App")
            db = PostgreSQL("Database")
            cache = Redis("Redis")
        vote >> db
        vote >> cache