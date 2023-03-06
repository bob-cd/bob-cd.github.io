from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.network import ALB
from diagrams.custom import Custom

if __name__ == "__main__":
    with Diagram("Bob Cluster", show=False, direction="TB"):
        rabbitmq = Custom("Queue", "rabbitmq.png")
        db = Custom("Database", "xt.png")

        with Cluster("API Servers"):
            api_servers = [EC2("server1"), EC2("server2"), EC2("server3")]

        with Cluster("Runners"):
            runners = [EC2("runner1"), EC2("runner2"), EC2("runner3")]

        ALB("Standard Load Balancer") >> api_servers >> rabbitmq >> runners
        api_servers >> db
        runners >> db
