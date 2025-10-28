from diagrams import Diagram, Cluster, Edge, Node
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.security import SecretsManager
from diagrams.aws.integration import Eventbridge
from diagrams.aws.network import APIGateway
from diagrams.aws.ml import Polly, Rekognition
from diagrams.onprem.client import User, Users
from diagrams.onprem.compute import Server
from diagrams.programming.framework import React
from diagrams.onprem.network import Nginx
from diagrams.custom import Custom
from graphviz import Graph
import os

# Path where the diagram will be saved
output_path = "/Users/skrinak/Development/Noggin/Documents/Images/noggin_architecture_updated"
agent_core_logo = "/Users/skrinak/Development/Noggin/Documents/Images/AgentCoreLogo.png"

# Create a custom class for AWS Transcribe since it's not in the standard library
class Transcribe(Rekognition):
    _icon = "rekognition.png"
    
    def __init__(self, label="Transcribe"):
        super().__init__(label)

# Create a custom class for AWS Bedrock since it's not in the standard library
class Bedrock(Custom):
    def __init__(self, label="Bedrock"):
        super().__init__(label, agent_core_logo)

# Create a custom class for Agents
class Agent(Custom):
    def __init__(self, label):
        super().__init__(label, agent_core_logo)

# Custom colors to match the sample diagram
COLORS = {
    "border": "#000000",
    "cluster_bg": "#F8F8F8",
    "cluster_border": "#DDDDDD",
    "aws_orange": "#FF9900",
    "lambda_orange": "#FF9900",
    "edge_color": "#333333",
    "api_gateway_purple": "#A152AD",
    "data_green": "#3F8624",
    "agent_blue": "#2496ED",
}

# Global graph attributes
graph_attrs = {
    "fontsize": "16",
    "fontname": "Arial",
    "bgcolor": "white",
    "rankdir": "LR",
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "1.0",
    "fontcolor": "#2D3436",
    "pad": "0.5",
    "style": "filled",
    "fillcolor": "white",
    "center": "true",
}

# Node attributes
node_attrs = {
    "shape": "box",
    "style": "filled",
    "fillcolor": "white",
    "fontname": "Arial",
    "fontsize": "13",
    "fontcolor": "#2D3436",
    "height": "1.3",
    "width": "2.2",
    "penwidth": "2.0",
}

# Edge attributes
edge_attrs = {
    "color": COLORS["edge_color"],
    "penwidth": "1.5",
    "fontname": "Arial",
    "fontsize": "11",
    "fontcolor": "#444444",
}

# Cluster attributes
cluster_attrs = {
    "style": "filled,rounded",
    "fillcolor": COLORS["cluster_bg"],
    "color": COLORS["cluster_border"],
    "fontname": "Arial",
    "fontsize": "14",
    "fontcolor": "#2D3436",
    "penwidth": "2.0",
    "margin": "15",
}

# Create the diagram with custom attributes
with Diagram("Noggin mTBI Management Architecture", 
             filename=output_path,
             show=False,
             direction="TB",
             graph_attr=graph_attrs,
             node_attr=node_attrs,
             edge_attr=edge_attrs):
    
    # Users and Client interfaces
    with Cluster("Users", graph_attr=cluster_attrs):
        patients = Users("Patients")
        clinicians = User("Clinicians")
    
    # Client Applications
    with Cluster("Client Applications", graph_attr=cluster_attrs):
        mobile = React("Mobile Apps")
        web = React("Web Dashboard")
        messaging = Nginx("Messaging (WhatsApp/SMS)")
    
    # AWS Services - API Layer
    with Cluster("API Layer", graph_attr=cluster_attrs):
        api = APIGateway("API Gateway")
        event_bridge = Eventbridge("EventBridge")
    
    # AWS Services - Compute Layer
    with Cluster("Compute Layer", graph_attr=cluster_attrs):
        with Cluster("Serverless Functions", graph_attr=cluster_attrs):
            intake_lambda = Lambda("Intake Service")
            monitoring_lambda = Lambda("Monitoring Service")
            intervention_lambda = Lambda("Intervention Service")
            escalation_lambda = Lambda("Escalation Service")
            notification_lambda = Lambda("Notification Service")
    
    # AWS Services - AI Layer
    with Cluster("AI Layer", graph_attr=cluster_attrs):
        with Cluster("AWS Bedrock", graph_attr=cluster_attrs):
            bedrock = Bedrock("AWS Bedrock AgentCore")
            
            with Cluster("Agents", graph_attr=cluster_attrs):
                intake_agent = Agent("Intake Agent")
                monitoring_agent = Agent("Monitoring Agent")
                intervention_agent = Agent("Intervention Agent")
                escalation_agent = Agent("Escalation Agent")
        
        # Voice Interface Services
        transcribe = Transcribe("AWS Transcribe Medical")
        polly = Polly("AWS Polly")
    
    # AWS Services - Data Layer
    with Cluster("Data Layer", graph_attr=cluster_attrs):
        dynamodb = Dynamodb("Patient Data")
        s3 = S3("Media Storage")
        secrets = SecretsManager("Secrets Manager")
    
    # Add numbered flow connections
    # 1. Patient interaction starts
    patients >> Edge(label="1. Initial contact", color=COLORS["edge_color"], penwidth="1.5") >> messaging
    patients >> Edge(label="1. Alternative channels", color=COLORS["edge_color"], penwidth="1.5") >> mobile
    
    # 2. Client apps to API Gateway
    messaging >> Edge(label="2. Forward interaction", color=COLORS["edge_color"], penwidth="1.5") >> api
    mobile >> Edge(label="2. Send data", color=COLORS["edge_color"], penwidth="1.5") >> api
    
    # 3. API Gateway routes to intake service
    api >> Edge(label="3. Route request", color=COLORS["edge_color"], penwidth="1.5") >> intake_lambda
    
    # 4. Intake service uses Bedrock agents
    intake_lambda >> Edge(label="4. Process assessment", color=COLORS["edge_color"], penwidth="1.5") >> bedrock
    bedrock >> Edge(color=COLORS["edge_color"], penwidth="1.5") >> intake_agent
    
    # 5. Voice processing if needed
    intake_lambda >> Edge(label="5a. Speech to text", color=COLORS["edge_color"], penwidth="1.5") >> transcribe
    transcribe >> Edge(label="5b. Return transcript", color=COLORS["edge_color"], penwidth="1.5") >> intake_lambda
    
    # 6. Store patient data
    intake_lambda >> Edge(label="6. Store data", color=COLORS["edge_color"], penwidth="1.5") >> dynamodb
    
    # 7. Event triggered for monitoring
    intake_lambda >> Edge(label="7. Trigger monitoring", color=COLORS["edge_color"], penwidth="1.5") >> event_bridge
    event_bridge >> Edge(color=COLORS["edge_color"], penwidth="1.5") >> monitoring_lambda
    
    # 8. Monitoring process
    monitoring_lambda >> Edge(label="8. Analyze symptoms", color=COLORS["edge_color"], penwidth="1.5") >> bedrock
    bedrock >> Edge(color=COLORS["edge_color"], penwidth="1.5") >> monitoring_agent
    
    # 9. Intervention recommendation
    monitoring_lambda >> Edge(label="9. Generate plan", color=COLORS["edge_color"], penwidth="1.5") >> intervention_lambda
    intervention_lambda >> Edge(color=COLORS["edge_color"], penwidth="1.5") >> bedrock
    bedrock >> Edge(color=COLORS["edge_color"], penwidth="1.5") >> intervention_agent
    
    # 10. Response generation
    intervention_lambda >> Edge(label="10a. Generate response", color=COLORS["edge_color"], penwidth="1.5") >> polly
    polly >> Edge(label="10b. Audio response", color=COLORS["edge_color"], penwidth="1.5") >> messaging
    intervention_lambda >> Edge(label="10c. Update mobile app", color=COLORS["edge_color"], penwidth="1.5") >> mobile
    
    # 11. Clinical escalation if needed
    monitoring_lambda >> Edge(label="11. Escalate if needed", color=COLORS["edge_color"], penwidth="1.5") >> escalation_lambda
    escalation_lambda >> Edge(color=COLORS["edge_color"], penwidth="1.5") >> bedrock
    bedrock >> Edge(color=COLORS["edge_color"], penwidth="1.5") >> escalation_agent
    
    # 12. Clinician notification
    escalation_lambda >> Edge(label="12. Alert clinician", color=COLORS["edge_color"], penwidth="1.5") >> notification_lambda
    notification_lambda >> Edge(color=COLORS["edge_color"], penwidth="1.5") >> clinicians
    
    # 13. Clinician access to dashboard
    clinicians >> Edge(label="13. View patient data", color=COLORS["edge_color"], penwidth="1.5") >> web
    web >> Edge(label="14. Retrieve data", color=COLORS["edge_color"], penwidth="1.5") >> api
    api >> Edge(label="15. Access records", color=COLORS["edge_color"], penwidth="1.5") >> dynamodb