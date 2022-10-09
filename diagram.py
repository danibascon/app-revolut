from diagrams import Cluster,Diagram
from diagrams.aws.compute import ECR,ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import ALB,Route53

with Diagram("Revolut App", show=False):
    with Cluster("ECS"):
        ECS = [ECS("APP")]

    ECR("ECR") >> ECS << ALB("ALB") << Route53("Route53")
    ECS >> RDS("RDS")
