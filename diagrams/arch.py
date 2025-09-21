from diagrams.aws.compute import EC2
from diagrams.aws.network import ALB
from diagrams.onprem.network import ETCD
from diagrams.onprem.queue import RabbitMQ

from diagrams import Cluster, Diagram

if __name__ == "__main__":
    with Diagram("Bob Cluster", show=False, direction="TB"):
        rabbitmq = RabbitMQ("Queue")
        db = ETCD("Database")
        logger = EC2("Logger")
        artifact_store = EC2("Artifact Store")
        resource_provider = EC2("Resource Provider")

        with Cluster("API Servers"):
            api_servers = [EC2("server1"), EC2("server2"), EC2("server3")]

        with Cluster("Runners"):
            runners = [EC2("runner1"), EC2("runner2"), EC2("runner3")]

        ALB("Standard Load Balancer") >> api_servers >> rabbitmq >> runners
        api_servers >> db
        runners >> db
        runners >> logger
        api_servers << logger
        api_servers << artifact_store
        runners << resource_provider
        runners << artifact_store
