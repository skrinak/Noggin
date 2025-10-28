from diagrams import Diagram, Cluster, Edge
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

# Path where the diagram will be saved
output_path = "/Users/skrinak/Development/Noggin/Documents/Images/noggin_architecture_original_with_agentcore"
agent_core_logo = "/Users/skrinak/Development/Noggin/Documents/Images/AgentCoreLogo.png"

# Create a custom class for AWS Transcribe since it's not in the standard library
class Transcribe(Rekognition):
    _icon = "rekognition.png"
    
    def __init__(self, label="Transcribe"):
        super().__init__(label)

# Create a custom class for AWS Bedrock with AgentCore logo
class Bedrock(Custom):
    def __init__(self, label="Bedrock"):
        super().__init__(label, agent_core_logo)

# Create the diagram - exactly as original but with AgentCore icons
with Diagram("Noggin mTBI Management Architecture", filename=output_path, show=False):
    
    # Users and Client interfaces
    with Cluster("Users"):
        patients = Users("Patients")
        clinicians = User("Clinicians")
    
    # Client Applications
    with Cluster("Client Applications"):
        mobile = React("Mobile Apps")
        web = React("Web Dashboard")
        messaging = Nginx("Messaging (WhatsApp/SMS)")
    
    # AWS Services - API Layer
    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        event_bridge = Eventbridge("EventBridge")
    
    # AWS Services - Compute Layer
    with Cluster("Compute Layer"):
        with Cluster("Serverless Functions"):
            intake_lambda = Lambda("Intake Service")
            monitoring_lambda = Lambda("Monitoring Service")
            intervention_lambda = Lambda("Intervention Service")
            escalation_lambda = Lambda("Escalation Service")
            notification_lambda = Lambda("Notification Service")
    
    # LLM Layer
    claude = Custom("Claude Sonnet 4.5", agent_core_logo)
    
    # AWS Services - AI Layer
    with Cluster("AI Layer"):
        with Cluster("AWS Bedrock"):
            bedrock = Bedrock("AWS Bedrock AgentCore")
            
            with Cluster("Agents"):
                # Using Custom class with AgentCore logo for agents
                intake_agent = Custom("Intake Agent", agent_core_logo)
                monitoring_agent = Custom("Monitoring Agent", agent_core_logo)
                intervention_agent = Custom("Intervention Agent", agent_core_logo)
                escalation_agent = Custom("Escalation Agent", agent_core_logo)
        
        # Voice Interface Services
        transcribe = Transcribe("AWS Transcribe Medical")
        polly = Polly("AWS Polly")
    
    # AWS Services - Data Layer
    with Cluster("Data Layer"):
        dynamodb = Dynamodb("Patient Data")
        s3 = S3("Media Storage")
        secrets = SecretsManager("Secrets Manager")
    
    # Add numbered flow connections
    # 1. Patient interaction starts
    patients >> Edge(label="1. Initial contact") >> messaging
    patients >> Edge(label="1. Alternative channels") >> mobile
    
    # 2. Client apps to API Gateway
    messaging >> Edge(label="2. Forward interaction") >> api
    mobile >> Edge(label="2. Send data") >> api
    
    # 3. API Gateway routes to intake service
    api >> Edge(label="3. Route request") >> intake_lambda
    
    # 4. Intake service uses Bedrock agents
    intake_lambda >> Edge(label="4. Process assessment") >> bedrock
    bedrock >> intake_agent
    
    # Connect agents to LLM
    intake_agent >> Edge() >> claude
    monitoring_agent >> Edge() >> claude
    intervention_agent >> Edge() >> claude
    escalation_agent >> Edge() >> claude
    
    # 5. Voice processing if needed
    intake_lambda >> Edge(label="5a. Speech to text") >> transcribe
    transcribe >> Edge(label="5b. Return transcript") >> intake_lambda
    
    # 6. Store patient data
    intake_lambda >> Edge(label="6. Store data") >> dynamodb
    
    # 7. Event triggered for monitoring
    intake_lambda >> Edge(label="7. Trigger monitoring") >> event_bridge
    event_bridge >> monitoring_lambda
    
    # 8. Monitoring process
    monitoring_lambda >> Edge(label="8. Analyze symptoms") >> bedrock
    bedrock >> monitoring_agent
    
    # 9. Intervention recommendation
    monitoring_lambda >> Edge(label="9. Generate plan") >> intervention_lambda
    intervention_lambda >> bedrock
    bedrock >> intervention_agent
    
    # 10. Response generation
    intervention_lambda >> Edge(label="10a. Generate response") >> polly
    polly >> Edge(label="10b. Audio response") >> messaging
    intervention_lambda >> Edge(label="10c. Update mobile app") >> mobile
    
    # 11. Clinical escalation if needed
    monitoring_lambda >> Edge(label="11. Escalate if needed") >> escalation_lambda
    escalation_lambda >> bedrock
    bedrock >> escalation_agent
    
    # 12. Clinician notification
    escalation_lambda >> Edge(label="12. Alert clinician") >> notification_lambda
    notification_lambda >> Edge() >> clinicians
    
    # 13. Clinician access to dashboard
    clinicians >> Edge(label="13. View patient data") >> web
    web >> Edge(label="14. Retrieve data") >> api
    api >> Edge(label="15. Access records") >> dynamodb