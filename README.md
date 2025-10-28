# Noggin: A Multi-Platform mTBI Management Solution

## Executive Summary
Noggin is a comprehensive digital health intervention designed for patients suffering from mild Traumatic Brain Injury (mTBI). This solution bridges the critical gap in healthcare by providing continuous monitoring, triage, and personalized care recommendations through a multi-platform architecture leveraging AWS cloud services and agentic AI.

## Problem Statement
Over one million people suffer an mTBI in the UK annually, yet most receive minimal follow-up care. This results in:
- Patients feeling neglected during recovery
- Delayed interventions that could prevent long-term complications
- Inefficient use of specialist resources

## Solution Architecture

### System Overview

Noggin implements a multi-layered architecture as shown in the [architectural diagram](Documents/Images/noggin_architecture_final_version.png). A detailed [interaction narrative](Documents/patient_interaction_narrative.md) describes how the system components work together in a typical scenario.

1. **User Interface Layer**
   - Native Mobile Applications (iOS/Android)
   - Web Application (Progressive Web App)
   - Conversational Interfaces (WhatsApp/SMS/Voice)

2. **Application Layer**
   - API Gateway (REST)
   - AWS Lambda Functions
   - EventBridge for event-driven processes

3. **Intelligence Layer**
   - AWS Bedrock AgentCore foundation
   - Domain-specific foundation models
   - STRANDS-based agent framework

4. **Data Layer**
   - DynamoDB for patient data and symptom tracking
   - S3 for media storage
   - Secrets Manager for sensitive information

### Agentic Architecture

Noggin employs a specialized multi-agent architecture based on STRANDS framework:

#### Core Agents

1. **Intake Agent**
   - Model: Claude 3 Sonnet
   - Purpose: Initial assessment and triage
   - Tools: Validated mTBI assessment protocols
   - Outputs: Severity score, risk classification

2. **Monitoring Agent**
   - Model: Claude 3 Haiku
   - Purpose: Continuous symptom tracking
   - Tools: Temporal pattern recognition, anomaly detection
   - Outputs: Recovery progress, symptom trends

3. **Intervention Agent**
   - Model: Fine-tuned Titan Text G1
   - Purpose: Personalized care recommendations
   - Tools: NHS guideline integration, intervention effectiveness tracking
   - Outputs: Tailored recovery plans, exercise recommendations

4. **Escalation Agent**
   - Model: Claude 3 Sonnet
   - Purpose: Clinical alert generation
   - Tools: Threshold monitoring, urgency classification
   - Outputs: Provider notifications, emergency alerts

#### Agent Coordination

- **Orchestrator Service**: Manages agent workflows and handoffs
- **Context Manager**: Maintains conversation history and patient context
- **Tool Repository**: Specialized clinical tools for assessment and intervention

### Voice Interface Implementation

Noggin implements a comprehensive voice interface through:

1. **Speech Recognition**
   - AWS Transcribe (with Medical specialization)
   - Real-time speech-to-text for patient interactions
   - Support for multiple languages and accents

2. **Voice Synthesis**
   - AWS Polly with NTTS (Neural Text-to-Speech)
   - Emotionally appropriate voice responses
   - Accessibility considerations for diverse user needs

3. **Conversation Management**
   - Turn-taking protocol
   - Interruption handling
   - Context preservation across voice sessions

### Mobile and Cloud Integration

The system seamlessly integrates mobile capabilities with AWS cloud services:

1. **Mobile Components**
   - Cross-platform React Native application
   - Offline symptom recording
   - Push notification system for reminders
   - Secure data synchronization

2. **Cloud Infrastructure**
   - Serverless architecture (Lambda + API Gateway)
   - Event-driven processing via EventBridge
   - HIPAA-compliant data storage with encryption
   - Multi-region deployment for reliability

## Implementation Plan

### Phase 1: Foundation (Months 1-3)
- Develop core AWS infrastructure using CloudFormation
- Implement base agent framework using STRANDS
- Create initial mobile application prototype
- Set up basic voice interface capabilities

### Phase 2: Intelligence Layer (Months 4-6)
- Train and integrate domain-specific foundation models
- Implement agent coordination system
- Develop clinical dashboard for providers
- Create comprehensive testing framework

### Phase 3: Clinical Validation (Months 7-12)
- Conduct multi-site testing with university athletes
- Analyze engagement and adherence patterns
- Refine triage sensitivity and decision-making
- Prepare for regulatory submissions (MHRA/IRAS)

## Technical Specifications

### AWS Services
- **Compute**: Lambda, ECS
- **Storage**: S3, DynamoDB
- **AI/ML**: Bedrock, Transcribe Medical, Polly
- **Security**: IAM, KMS, Secrets Manager
- **Networking**: API Gateway, CloudFront

### Foundation Models
- **Primary LLM**: Claude 3 Sonnet (general interactions)
- **Lightweight LLM**: Claude 3 Haiku (routine monitoring)
- **Specialized Models**: Fine-tuned Titan models for specific clinical tasks
- **Embedding Model**: Amazon Titan Embeddings (symptom pattern recognition)

### Security and Compliance
- End-to-end encryption for all data
- HIPAA compliance architecture
- Role-based access control
- Comprehensive audit logging
- Regular penetration testing

## Cost Optimization

Noggin implements several strategies to maintain low operational costs:

1. **Serverless Architecture**
   - Pay-per-use Lambda functions
   - Auto-scaling based on demand

2. **Model Selection Strategy**
   - Smaller, specialized models for routine tasks
   - Larger models reserved for complex interactions
   - Caching for common responses

3. **Resource Tiering**
   - Development/testing environments with lower-cost resources
   - Production environment optimized for performance and reliability

## Expected Outcomes

1. **Patient Benefits**
   - Continuous engagement during recovery
   - Personalized guidance and support
   - Timely escalation when needed

2. **Clinical Benefits**
   - Comprehensive symptom documentation
   - Efficient resource allocation
   - Data-driven treatment decisions

3. **Research Benefits**
   - Rich longitudinal data for mTBI research
   - Framework for LLM integration in clinical settings
   - Validation of digital health interventions

## Future Extensions

1. **Expanded Clinical Domains**
   - Adaptation for other neurological conditions
   - Extension to chronic disease management

2. **Enhanced Sensing**
   - Integration with wearable devices
   - Passive symptom monitoring

3. **Advanced Analytics**
   - Population-level insights
   - Predictive recovery modeling