from diagrams import Diagram, Cluster, Edge, Node
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.security import SecretsManager
from diagrams.aws.integration import Eventbridge
from diagrams.aws.network import APIGateway, VPC
from diagrams.aws.ml import Polly, Rekognition
from diagrams.onprem.client import User, Users
from diagrams.onprem.compute import Server
from diagrams.programming.framework import React
from diagrams.onprem.network import Nginx
from diagrams.custom import Custom
import os

# Path where the diagram will be saved
output_path = "/Users/skrinak/Development/Noggin/Documents/Images/noggin_architecture_final"
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
    "cluster_bg": "#FFFFFF",
    "cluster_border": "#DDDDDD",
    "aws_orange": "#FF9900",
    "lambda_orange": "#FF9900",
    "edge_color": "#333333",
    "api_gateway_purple": "#A152AD",
    "data_green": "#3F8624",
    "agent_blue": "#2496ED",
    "aws_cloud_bg": "#F8F8F8", 
    "vpc_bg": "#E9F1F6",
    "vpc_border": "#7AA3B5",
    "llm_bg": "#E8F0F7",
}

# Global graph attributes
graph_attrs = {
    "fontsize": "18",
    "fontname": "Arial",
    "bgcolor": "white",
    "rankdir": "TB",
    "pad": "0.5",
    "splines": "ortho",
    "nodesep": "0.9",
    "ranksep": "1.2",
}

# Node attributes
node_attrs = {
    "shape": "box",
    "style": "filled",
    "fillcolor": "white",
    "fontname": "Arial",
    "fontsize": "13",
    "height": "1.3",
    "width": "2.2",
    "penwidth": "1.5",
}

# Bold numbered edge attributes
bold_edge_attrs = {
    "color": COLORS["edge_color"],
    "penwidth": "2.0",
    "fontname": "Arial",
    "fontsize": "13",
    "fontcolor": "#000000",
    "fontweight": "bold",
}

# Normal edge attributes
edge_attrs = {
    "color": COLORS["edge_color"],
    "penwidth": "1.2",
    "fontname": "Arial",
    "fontsize": "11",
}

# AWS Cloud cluster attributes
aws_cloud_attrs = {
    "style": "filled",
    "fillcolor": COLORS["aws_cloud_bg"],
    "color": COLORS["cluster_border"],
    "fontname": "Arial",
    "fontsize": "20",
    "fontweight": "bold",
    "penwidth": "1.5",
    "margin": "30",
}

# VPC cluster attributes
vpc_attrs = {
    "style": "filled",
    "fillcolor": COLORS["vpc_bg"],
    "color": COLORS["vpc_border"],
    "fontname": "Arial",
    "fontsize": "16",
    "penwidth": "1.5",
    "margin": "20",
}

# Regular cluster attributes
cluster_attrs = {
    "style": "rounded,filled",
    "fillcolor": COLORS["cluster_bg"],
    "color": COLORS["cluster_border"],
    "fontname": "Arial",
    "fontsize": "14",
    "penwidth": "1.0",
    "margin": "12",
}

# LLM cluster attributes
llm_attrs = {
    "style": "filled,rounded",
    "fillcolor": COLORS["llm_bg"],
    "color": "#5B9BD5",
    "fontname": "Arial",
    "fontsize": "16",
    "fontweight": "bold",
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
    
    # AWS Cloud boundary
    with Cluster("AWS Cloud", graph_attr=aws_cloud_attrs):
        
        # AWS VPC boundary
        with Cluster("VPC", graph_attr=vpc_attrs):
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
            
            # LLM Layer
            with Cluster("Language Model", graph_attr=llm_attrs):
                claude = Custom("Claude Sonnet 4.5", agent_core_logo)
            
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
    
    # External Users - outside AWS Cloud
    with Cluster("Users", graph_attr=cluster_attrs):
        patients = Users("Patients")
        clinicians = User("Clinicians")
    
    # Add numbered flow connections with bold labels
    # 1. Patient interaction starts
    patients >> Edge(label="1. Initial contact", **bold_edge_attrs) >> messaging
    patients >> Edge(label="1. Alternative channels", **bold_edge_attrs) >> mobile
    
    # 2. Client apps to API Gateway
    messaging >> Edge(label="2. Forward interaction", **bold_edge_attrs) >> api
    mobile >> Edge(label="2. Send data", **bold_edge_attrs) >> api
    
    # 3. API Gateway routes to intake service
    api >> Edge(label="3. Route request", **bold_edge_attrs) >> intake_lambda
    
    # 4. Intake service uses Bedrock agents
    intake_lambda >> Edge(label="4. Process assessment", **bold_edge_attrs) >> bedrock
    bedrock >> Edge(**edge_attrs) >> intake_agent
    
    # Connect agents to LLM
    intake_agent >> Edge(label="Agent-LLM interaction", **edge_attrs) >> claude
    monitoring_agent >> Edge(**edge_attrs) >> claude
    intervention_agent >> Edge(**edge_attrs) >> claude
    escalation_agent >> Edge(**edge_attrs) >> claude
    
    # 5. Voice processing if needed
    intake_lambda >> Edge(label="5a. Speech to text", **bold_edge_attrs) >> transcribe
    transcribe >> Edge(label="5b. Return transcript", **bold_edge_attrs) >> intake_lambda
    
    # 6. Store patient data
    intake_lambda >> Edge(label="6. Store data", **bold_edge_attrs) >> dynamodb
    
    # 7. Event triggered for monitoring
    intake_lambda >> Edge(label="7. Trigger monitoring", **bold_edge_attrs) >> event_bridge
    event_bridge >> Edge(**edge_attrs) >> monitoring_lambda
    
    # 8. Monitoring process
    monitoring_lambda >> Edge(label="8. Analyze symptoms", **bold_edge_attrs) >> bedrock
    bedrock >> Edge(**edge_attrs) >> monitoring_agent
    
    # 9. Intervention recommendation
    monitoring_lambda >> Edge(label="9. Generate plan", **bold_edge_attrs) >> intervention_lambda
    intervention_lambda >> Edge(**edge_attrs) >> bedrock
    bedrock >> Edge(**edge_attrs) >> intervention_agent
    
    # 10. Response generation
    intervention_lambda >> Edge(label="10a. Generate response", **bold_edge_attrs) >> polly
    polly >> Edge(label="10b. Audio response", **bold_edge_attrs) >> messaging
    intervention_lambda >> Edge(label="10c. Update mobile app", **bold_edge_attrs) >> mobile
    
    # 11. Clinical escalation if needed
    monitoring_lambda >> Edge(label="11. Escalate if needed", **bold_edge_attrs) >> escalation_lambda
    escalation_lambda >> Edge(**edge_attrs) >> bedrock
    bedrock >> Edge(**edge_attrs) >> escalation_agent
    
    # 12. Clinician notification
    escalation_lambda >> Edge(label="12. Alert clinician", **bold_edge_attrs) >> notification_lambda
    notification_lambda >> Edge(**edge_attrs) >> clinicians
    
    # 13. Clinician access to dashboard
    clinicians >> Edge(label="13. View patient data", **bold_edge_attrs) >> web
    web >> Edge(label="14. Retrieve data", **bold_edge_attrs) >> api
    api >> Edge(label="15. Access records", **bold_edge_attrs) >> dynamodb