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
import os
import graphviz

# Path where the diagram will be saved
output_path = "/Users/skrinak/Development/Noggin/Documents/Images/noggin_architecture_readable"
agent_core_logo = "/Users/skrinak/Development/Noggin/Documents/Images/AgentCoreLogo.png"

# Create a custom class for AWS Transcribe since it's not in the standard library
class Transcribe(Rekognition):
    _icon = "rekognition.png"
    
    def __init__(self, label="Transcribe"):
        super().__init__(label)

# Use Server class with clear labels instead of Custom for better label visibility
class AgentCore(Server):
    def __init__(self, label):
        super().__init__(label)

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
    "rankdir": "LR",  # Left to right layout for better readability
    "pad": "0.5",
    "splines": "ortho",
    "nodesep": "0.9",
    "ranksep": "1.0",
    "concentrate": "true",  # Concentrate edges for better readability
}

# Node attributes
node_attrs = {
    "shape": "box",
    "style": "filled",
    "fillcolor": "white",
    "fontname": "Arial",
    "fontsize": "14",  # Larger font size for better readability
    "fontcolor": "#000000",
    "height": "1.3",
    "width": "2.2",
    "penwidth": "1.5",
}

# HTML-based bold edge label formatting
def bold_edge_label(text):
    return f"<<b>{text}</b>>"

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
    "label": "AWS Cloud",
}

# VPC cluster attributes
vpc_attrs = {
    "style": "filled",
    "fillcolor": COLORS["vpc_bg"],
    "color": COLORS["vpc_border"],
    "fontname": "Arial",
    "fontsize": "16",
    "fontweight": "bold",
    "penwidth": "1.5",
    "margin": "20",
    "label": "VPC",
}

# Regular cluster attributes
cluster_attrs = {
    "style": "rounded,filled",
    "fillcolor": COLORS["cluster_bg"],
    "color": COLORS["cluster_border"],
    "fontname": "Arial",
    "fontsize": "14",
    "fontcolor": "#000000",
    "penwidth": "1.0",
    "margin": "15",
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
    "label": "Language Model"
}

# Create the diagram with custom attributes
with Diagram("Noggin mTBI Management Architecture", 
             filename=output_path,
             show=False,
             direction="LR",  # Left to right for better readability
             graph_attr=graph_attrs,
             node_attr=node_attrs):
    
    # AWS Cloud boundary
    with Cluster("", graph_attr=aws_cloud_attrs):
        
        # AWS VPC boundary
        with Cluster("", graph_attr=vpc_attrs):
            # Client Applications
            with Cluster("Client Applications", graph_attr=cluster_attrs):
                mobile = React("Mobile Apps")
                web = React("Web Dashboard")
                messaging = Nginx("Messaging\\n(WhatsApp/SMS)")
            
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
            with Cluster("", graph_attr=llm_attrs):
                claude = Server("Claude Sonnet 4.5")
            
            # AWS Services - AI Layer
            with Cluster("AI Layer", graph_attr=cluster_attrs):
                with Cluster("AWS Bedrock", graph_attr=cluster_attrs):
                    bedrock = AgentCore("AWS Bedrock AgentCore")
                    
                    with Cluster("Agents", graph_attr=cluster_attrs):
                        intake_agent = AgentCore("Intake Agent")
                        monitoring_agent = AgentCore("Monitoring Agent")
                        intervention_agent = AgentCore("Intervention Agent")
                        escalation_agent = AgentCore("Escalation Agent")
                
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
    
    # Add numbered flow connections with bold labels using HTML formatting
    # 1. Patient interaction starts
    patients >> Edge(label=bold_edge_label("1. Initial contact"), fontsize="14", penwidth="2.0") >> messaging
    patients >> Edge(label=bold_edge_label("1. Alternative channels"), fontsize="14", penwidth="2.0") >> mobile
    
    # 2. Client apps to API Gateway
    messaging >> Edge(label=bold_edge_label("2. Forward interaction"), fontsize="14", penwidth="2.0") >> api
    mobile >> Edge(label=bold_edge_label("2. Send data"), fontsize="14", penwidth="2.0") >> api
    
    # 3. API Gateway routes to intake service
    api >> Edge(label=bold_edge_label("3. Route request"), fontsize="14", penwidth="2.0") >> intake_lambda
    
    # 4. Intake service uses Bedrock agents
    intake_lambda >> Edge(label=bold_edge_label("4. Process assessment"), fontsize="14", penwidth="2.0") >> bedrock
    bedrock >> Edge(penwidth="1.5") >> intake_agent
    
    # Connect agents to LLM
    intake_agent >> Edge(label="Agent-LLM interaction", fontsize="13", penwidth="1.5") >> claude
    monitoring_agent >> Edge(penwidth="1.5") >> claude
    intervention_agent >> Edge(penwidth="1.5") >> claude
    escalation_agent >> Edge(penwidth="1.5") >> claude
    
    # 5. Voice processing if needed
    intake_lambda >> Edge(label=bold_edge_label("5a. Speech to text"), fontsize="14", penwidth="2.0") >> transcribe
    transcribe >> Edge(label=bold_edge_label("5b. Return transcript"), fontsize="14", penwidth="2.0") >> intake_lambda
    
    # 6. Store patient data
    intake_lambda >> Edge(label=bold_edge_label("6. Store data"), fontsize="14", penwidth="2.0") >> dynamodb
    
    # 7. Event triggered for monitoring
    intake_lambda >> Edge(label=bold_edge_label("7. Trigger monitoring"), fontsize="14", penwidth="2.0") >> event_bridge
    event_bridge >> Edge(penwidth="1.5") >> monitoring_lambda
    
    # 8. Monitoring process
    monitoring_lambda >> Edge(label=bold_edge_label("8. Analyze symptoms"), fontsize="14", penwidth="2.0") >> bedrock
    bedrock >> Edge(penwidth="1.5") >> monitoring_agent
    
    # 9. Intervention recommendation
    monitoring_lambda >> Edge(label=bold_edge_label("9. Generate plan"), fontsize="14", penwidth="2.0") >> intervention_lambda
    intervention_lambda >> Edge(penwidth="1.5") >> bedrock
    bedrock >> Edge(penwidth="1.5") >> intervention_agent
    
    # 10. Response generation
    intervention_lambda >> Edge(label=bold_edge_label("10a. Generate response"), fontsize="14", penwidth="2.0") >> polly
    polly >> Edge(label=bold_edge_label("10b. Audio response"), fontsize="14", penwidth="2.0") >> messaging
    intervention_lambda >> Edge(label=bold_edge_label("10c. Update mobile app"), fontsize="14", penwidth="2.0") >> mobile
    
    # 11. Clinical escalation if needed
    monitoring_lambda >> Edge(label=bold_edge_label("11. Escalate if needed"), fontsize="14", penwidth="2.0") >> escalation_lambda
    escalation_lambda >> Edge(penwidth="1.5") >> bedrock
    bedrock >> Edge(penwidth="1.5") >> escalation_agent
    
    # 12. Clinician notification
    escalation_lambda >> Edge(label=bold_edge_label("12. Alert clinician"), fontsize="14", penwidth="2.0") >> notification_lambda
    notification_lambda >> Edge(penwidth="1.5") >> clinicians
    
    # 13. Clinician access to dashboard
    clinicians >> Edge(label=bold_edge_label("13. View patient data"), fontsize="14", penwidth="2.0") >> web
    web >> Edge(label=bold_edge_label("14. Retrieve data"), fontsize="14", penwidth="2.0") >> api
    api >> Edge(label=bold_edge_label("15. Access records"), fontsize="14", penwidth="2.0") >> dynamodb