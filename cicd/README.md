# Azure DevOps CI/CD Pipeline for AI Agent Deployment

This directory contains Azure DevOps pipelines for deploying and testing AI agents across multiple environments (dev, test, production).

## 🚀 Quick Start

**New to Azure DevOps Pipelines?** Follow these steps:

1. **Prerequisites**: Ensure you have Azure AI Project and OpenAI resources for each environment
2. **Setup**: Complete Steps 1-3 in [Setting Up Pipelines](#3-setting-up-pipelines-in-azure-devops) section
3. **Create Pipeline**: Follow Step 4 to create your first pipeline
4. **Run**: Execute the pipeline and monitor results

**Estimated Setup Time**: 30-45 minutes for first-time setup

---

## Pipeline Files

### 1. `createagentpipeline.yml`
**Purpose**: Agent creation and deployment pipeline across dev, test, and production environments.

**Stages**:
- **Build**: Validates Python syntax, installs dependencies, publishes artifacts
- **Dev**: Creates agent in development environment using `createagent.py`
- **Test**: Creates agent in test environment
- **Prod**: Creates agent in production environment (requires approval)

**Use this when**: You need to create or update agents across all environments.

### 2. `agentconsumptionpipeline.yml`
**Purpose**: Comprehensive testing and evaluation pipeline for existing agents.

**Stages**:
- **Build**: Validates all Python scripts (createagent.py, exagent.py, agenteval.py, redteam.py)
- **Dev**: Tests existing agent with `exagent.py`
- **Test**: Runs agent evaluation (`agenteval.py`) and red team security testing (`redteam.py`)
- **Prod**: Verifies production agent functionality

**Use this when**: You want to test, evaluate, and security-test existing deployed agents without creating new ones.

## Prerequisites

### 1. Azure Resources
Create the following resources for each environment (dev, test, prod):
- Azure AI Project
- Azure OpenAI resource with deployments
- Service Principal for authentication

### 2. Azure DevOps Setup

#### A. Service Connections
Create Azure Resource Manager service connections for each environment:
1. Go to Project Settings → Service Connections
2. Create service connections named:
   - `AZURE_SERVICE_CONNECTION_DEV`
   - `AZURE_SERVICE_CONNECTION_TEST`
   - `AZURE_SERVICE_CONNECTION_PROD`

#### B. Variable Groups
Create three variable groups with the following variables:

**Variable Group: `agent-dev-vars`**
```
AZURE_AI_PROJECT_DEV=<your-dev-ai-project-endpoint>
AZURE_OPENAI_ENDPOINT_DEV=<your-dev-openai-endpoint>
AZURE_OPENAI_KEY_DEV=<your-dev-openai-key>
AZURE_OPENAI_API_VERSION_DEV=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_DEV=gpt-4o
AZURE_AI_PROJECT_ENDPOINT_DEV=<your-dev-project-endpoint>
AZURE_SERVICE_CONNECTION_DEV=<your-dev-service-connection-name>
```

**Variable Group: `agent-test-vars`**
```
AZURE_AI_PROJECT_TEST=<your-test-ai-project-endpoint>
AZURE_OPENAI_ENDPOINT_TEST=<your-test-openai-endpoint>
AZURE_OPENAI_KEY_TEST=<your-test-openai-key>
AZURE_OPENAI_API_VERSION_TEST=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_TEST=gpt-4o
AZURE_AI_PROJECT_ENDPOINT_TEST=<your-test-project-endpoint>
AZURE_SERVICE_CONNECTION_TEST=<your-test-service-connection-name>
```

**Variable Group: `agent-prod-vars`**
```
AZURE_AI_PROJECT_PROD=<your-prod-ai-project-endpoint>
AZURE_OPENAI_ENDPOINT_PROD=<your-prod-openai-endpoint>
AZURE_OPENAI_KEY_PROD=<your-prod-openai-key>
AZURE_OPENAI_API_VERSION_PROD=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_PROD=gpt-4o
AZURE_AI_PROJECT_ENDPOINT_PROD=<your-prod-project-endpoint>
AZURE_SERVICE_CONNECTION_PROD=<your-prod-service-connection-name>
```

**Global Variables** (add to pipeline or variable group):
```
AZURE_CLIENT_ID=<service-principal-client-id>
AZURE_TENANT_ID=<azure-tenant-id>
AZURE_SUBSCRIPTION_ID=<azure-subscription-id>
```

#### C. Environments
Create three environments with approval gates:
1. Go to Pipelines → Environments
2. Create environments:
   - `dev` (no approvals required)
   - `test` (optional: add approvals)
   - `production` (recommended: add approvals and checks)

To add approval gates:
1. Select the environment
2. Click on "Approvals and checks"
3. Add "Approvals" and specify required approvers

### 3. Setting Up Pipelines in Azure DevOps

Follow these detailed steps to create and configure your pipelines in Azure DevOps.

#### Step-by-Step Guide

##### **Step 1: Create Service Connections**

1. Navigate to your Azure DevOps project
2. Click **Project Settings** (bottom-left corner)
3. Under **Pipelines**, select **Service connections**
4. Click **New service connection**
5. Select **Azure Resource Manager**
6. Choose **Service principal (automatic)** or **Service principal (manual)**
7. Configure for each environment:

   **For Dev Connection:**
   - Subscription: Select your Azure subscription
   - Resource group: Select dev resource group (or leave empty for subscription-level)
   - Service connection name: `AZURE_SERVICE_CONNECTION_DEV`
   - Description: "Service connection for Dev environment"
   - Grant access permission to all pipelines: ☑ (check)
   - Click **Save**

   **For Test Connection:**
   - Repeat the above steps
   - Service connection name: `AZURE_SERVICE_CONNECTION_TEST`
   - Description: "Service connection for Test environment"

   **For Prod Connection:**
   - Repeat the above steps
   - Service connection name: `AZURE_SERVICE_CONNECTION_PROD`
   - Description: "Service connection for Production environment"

##### **Step 2: Create Variable Groups**

1. In Project Settings, under **Pipelines**, select **Library**
2. Click **+ Variable group**

   **Create Dev Variable Group:**
   - Variable group name: `agent-dev-vars`
   - Click **+ Add** for each variable:
     ```
     AZURE_AI_PROJECT_DEV = https://<your-project>.api.azureml.ms
     AZURE_OPENAI_ENDPOINT_DEV = https://<your-openai>.openai.azure.com/
     AZURE_OPENAI_KEY_DEV = <your-key> (click the lock icon to make it secret)
     AZURE_OPENAI_API_VERSION_DEV = 2024-02-15-preview
     AZURE_OPENAI_DEPLOYMENT_DEV = gpt-4o
     AZURE_AI_PROJECT_ENDPOINT_DEV = https://<your-project>.api.azureml.ms
     AZURE_SERVICE_CONNECTION_DEV = AZURE_SERVICE_CONNECTION_DEV
     ```
   - Click **Save**

   **Create Test Variable Group:**
   - Variable group name: `agent-test-vars`
   - Add the same variables with `_TEST` suffix
   - Click **Save**

   **Create Prod Variable Group:**
   - Variable group name: `agent-prod-vars`
   - Add the same variables with `_PROD` suffix
   - Click **Save**

3. **Add Global Variables** (optional - can also add to each pipeline):
   - Create a variable group named `agent-global-vars`
   - Add:
     ```
     AZURE_CLIENT_ID = <service-principal-client-id>
     AZURE_TENANT_ID = <azure-tenant-id>
     AZURE_SUBSCRIPTION_ID = <azure-subscription-id>
     ```

##### **Step 3: Create Environments**

1. In **Pipelines**, select **Environments**
2. Click **New environment** or **Create environment**

   **Dev Environment:**
   - Name: `dev`
   - Description: "Development environment for AI agents"
   - Resource: None
   - Click **Create**

   **Test Environment:**
   - Name: `test`
   - Description: "Test environment for AI agents"
   - Click **Create**
   - After creation, click on the environment
   - Click **Approvals and checks** (three dots menu)
   - Add **Approvals** (optional)
     - Approvers: Add team members who should approve test deployments
     - Instructions: "Review test deployment before proceeding"

   **Production Environment:**
   - Name: `production`
   - Description: "Production environment for AI agents"
   - Click **Create**
   - Click **Approvals and checks**
   - Add **Approvals** (recommended)
     - Approvers: Add required approvers (e.g., tech lead, manager)
     - Instructions: "Review production deployment and verify test results"
     - Advanced: Set timeout and approval timeout settings

##### **Step 4: Create Pipelines**

**Create Agent Creation Pipeline:**

1. Go to **Pipelines** → **Pipelines**
2. Click **New pipeline** or **Create pipeline**
3. **Where is your code?**
   - Select **Azure Repos Git** (or GitHub if using GitHub)
4. **Select a repository**
   - Choose your repository (e.g., `foundrycicdbasic`)
5. **Configure your pipeline**
   - Select **Existing Azure Pipelines YAML file**
6. **Select an existing YAML file**
   - Branch: `main`
   - Path: `/cicd/createagentpipeline.yml`
   - Click **Continue**
7. **Review your pipeline YAML**
   - Review the pipeline configuration
   - Click **Save** (dropdown next to Run)
   - Optionally click **Run** to execute immediately
8. **Rename the pipeline** (optional but recommended):
   - Click on the three dots menu (⋮) next to the pipeline
   - Select **Rename/move**
   - Name: `AI Agent - Create Pipeline`
   - Click **Save**

**Create Agent Testing/Evaluation Pipeline:**

1. Repeat steps 1-4 above
2. **Select an existing YAML file**
   - Branch: `main`
   - Path: `/cicd/agentconsumptionpipeline.yml`
   - Click **Continue**
3. Review and save
4. Rename to: `AI Agent - Testing & Evaluation Pipeline`

##### **Step 5: Grant Permissions**

1. For each pipeline created:
   - Go to the pipeline
   - Click **Edit**
   - Click the three dots menu (⋮) in the top-right
   - Select **Triggers**
   - Go to the **YAML** tab
   - Click **Get sources**
   - Ensure "Grant access to all pipelines" is enabled for:
     - Service connections
     - Variable groups
     - Environments

##### **Step 6: Test the Pipeline**

1. Go to **Pipelines** → **Pipelines**
2. Select the pipeline you want to test
3. Click **Run pipeline**
4. Select the branch (e.g., `main`)
5. Click **Run**
6. Monitor the pipeline execution:
   - Click on the running pipeline
   - View logs for each stage
   - Approve deployments when prompted (for test/prod environments)
7. Review results:
   - Check deployment logs
   - Download artifacts if available
   - Verify agent creation/testing in Azure AI Foundry portal

## Pipeline Triggers

The pipeline triggers on:
- Commits to `main` or `develop` branches
- Changes to:
  - `createagent.py`
  - `exagent.py`
  - `agenteval.py`
  - `redteam.py`
  - `requirements.txt`
  - `cicd/*` folder

## Scripts Overview

### `createagent.py`
Creates a new AI agent in Azure AI Foundry.
- Uses `DefaultAzureCredential` for authentication
- Creates agent with name "cicdagenttest"
- Configures agent instructions for CI/CD tasks

### `exagent.py`
Tests an existing agent by running queries and verifying responses.
- Retrieves existing agent by name
- Sends test queries
- Handles MCP approval requests
- Displays responses with citations

### `agenteval.py`
Evaluates agent performance using Azure AI Evaluation metrics:
- **Tool Call Accuracy**: Validates tool calls are correct
- **Intent Resolution**: Checks if agent understands user intent
- **Task Adherence**: Verifies agent follows task requirements
- **Response Completeness**: Ensures responses are comprehensive

### `redteam.py`
Performs security red team testing with attack strategies:
- Violence, HateUnfairness, Sexual, SelfHarm risk categories
- Multiple attack strategies: Easy, Moderate, CharacterSpace, ROT13, UnicodeConfusable, CharSwap, Morse, Leetspeak, URL, Binary, and composed attacks
- Generates detailed security reports

## Monitoring and Results

### Pipeline Artifacts
- **agent-scripts**: Source code artifacts from build stage
- **redteam-results-test**: Red team evaluation results from test stage

### Viewing Results
1. Go to pipeline run details
2. Click on "Published" to view artifacts
3. Download `redteam-results-test` to review security findings

### Logs and Traces
- All stages output detailed logs
- OpenTelemetry traces are generated for observability
- Check pipeline logs for trace IDs and debugging information

## Best Practices

1. **Environment Isolation**: Keep dev, test, and prod resources completely separate
2. **Secret Management**: Store all sensitive values in Azure Key Vault and reference them in variable groups
3. **Approval Gates**: Always require approvals for production deployments
4. **Testing**: Don't skip evaluation and red team testing in test environment
5. **Monitoring**: Set up alerts for pipeline failures and evaluation metric thresholds
6. **Version Control**: Tag releases and maintain changelog for production deployments

## Pipeline Comparison

| Feature | createagentpipeline.yml | agentconsumptionpipeline.yml |
|---------|------------------------|------------------------------|
| **Purpose** | Create/Deploy agents | Test/Evaluate existing agents |
| **Agent Creation** | ✅ Yes (all environments) | ❌ No |
| **Agent Testing** | ❌ No | ✅ Yes (exagent.py) |
| **Evaluation Metrics** | ❌ No | ✅ Yes (agenteval.py) |
| **Red Team Testing** | ❌ No | ✅ Yes (redteam.py) |
| **Artifacts Published** | agent-scripts | agent-scripts, redteam-results |
| **Best Used For** | Initial deployment, updates | Quality assurance, security testing |

## Common Workflow

1. **Create Agent**: Run `createagentpipeline.yml` to deploy agent to dev → test → prod
2. **Test & Validate**: Run `agentconsumptionpipeline.yml` to validate agent behavior and security
3. **Monitor**: Review artifacts and logs
4. **Iterate**: Make changes and repeat

## Troubleshooting

### Authentication Errors

**Problem**: "Unable to authenticate" or "403 Forbidden" errors

**Solutions**:
- Verify service connections are properly configured in Project Settings
- Check that service principal has the following roles:
  - **Cognitive Services Contributor** on Azure OpenAI resource
  - **Azure AI Developer** on Azure AI project
  - **Reader** on resource group
- Ensure variable groups contain correct credentials
- Verify service principal isn't expired
- Check that `DefaultAzureCredential` can authenticate:
  ```bash
  az login
  az account show
  ```

### Pipeline Not Triggering

**Problem**: Pipeline doesn't run on code changes

**Solutions**:
- Check trigger paths in YAML match the files you changed
- Verify branch name matches trigger configuration (`main` or `develop`)
- Check if pipeline is disabled (click pipeline → Edit → ensure it's enabled)
- Review commit history to ensure changes were pushed

### Variable Group Not Found

**Problem**: "Could not find variable group" error

**Solutions**:
- Verify variable group names match exactly (case-sensitive):
  - `agent-dev-vars`
  - `agent-test-vars`
  - `agent-prod-vars`
- Grant pipeline access to variable groups:
  - Go to Library → Select variable group
  - Click Pipeline permissions
  - Add your pipeline

### Environment Not Found

**Problem**: "Could not find environment" error

**Solutions**:
- Create environments in Pipelines → Environments
- Names must match YAML exactly: `dev`, `test`, `production`
- Grant pipeline access to environments

### Agent Creation Failures

**Problem**: createagent.py fails with errors

**Solutions**:
- Verify Azure AI Project endpoint format: `https://<project>.api.azureml.ms`
- Check agent name doesn't conflict with existing agents
- Review Azure AI Foundry quotas and limits
- Check Python dependencies are installed correctly
- View detailed error in pipeline logs

### Evaluation Failures

**Problem**: agenteval.py fails during execution

**Solutions**:
- Ensure OpenAI deployment has sufficient capacity and quota
- Verify evaluation metrics configuration
- Check Azure AI Evaluation service is available in your region
- Ensure agent exists before running evaluation
- Review token limits and rate limiting

### Red Team Testing Failures

**Problem**: redteam.py times out or fails

**Solutions**:
- Red team tests may take 10-30 minutes - this is normal
- Use `continueOnError: true` in pipeline to prevent blocking
- Check rate limits on Azure OpenAI deployment
- Reduce `num_objectives` in redteam.py for faster testing
- Verify sufficient quota for multiple API calls
- Review attack strategy configuration

### Artifact Download Issues

**Problem**: Can't find or download pipeline artifacts

**Solutions**:
- Ensure the stage that publishes artifacts completed successfully
- Check artifact name matches: `agent-scripts`, `redteam-results-test`
- Artifacts are available for 30 days by default
- Click pipeline run → Published tab to view artifacts

### Python Module Import Errors

**Problem**: "ModuleNotFoundError" in pipeline

**Solutions**:
- Verify all dependencies are in `requirements.txt`
- Check Python version matches (3.11 specified in pipeline)
- Ensure pip install step completed successfully
- Review dependency versions for compatibility

## Pipeline Security Best Practices

1. **Secrets Management**
   - ✅ Use Azure Key Vault for storing sensitive credentials
   - ✅ Mark variables as "secret" in variable groups (lock icon)
   - ✅ Avoid logging secrets in pipeline output
   - ✅ Use managed identities when possible

2. **Access Control**
   - ✅ Implement approval gates for production
   - ✅ Use different service principals per environment
   - ✅ Follow principle of least privilege for permissions
   - ✅ Regular review service principal permissions

3. **Code Security**
   - ✅ Enable branch protection on main/production branches
   - ✅ Require pull request reviews before merging
   - ✅ Use red team testing pipeline regularly
   - ✅ Monitor evaluation metrics for degradation

## Additional Resources

### Documentation
- [Azure AI Agent Framework Documentation](https://learn.microsoft.com/azure/ai-services/agents/)
- [Azure DevOps Pipelines Documentation](https://learn.microsoft.com/azure/devops/pipelines/)
- [Azure AI Evaluation Documentation](https://learn.microsoft.com/azure/ai-studio/how-to/evaluate-sdk)
- [Azure OpenTelemetry Setup](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-enable)

### Useful Commands

**Check Azure CLI login:**
```bash
az login
az account show
```

**List Azure DevOps pipelines:**
```bash
az pipelines list --organization https://dev.azure.com/your-org --project your-project
```

**Validate YAML locally:**
```bash
az pipelines validate --yaml-path cicd/createagentpipeline.yml
```

**Download pipeline artifacts:**
```bash
az pipelines runs artifact download --organization https://dev.azure.com/your-org --project your-project --run-id <run-id>
```

## FAQ

**Q: Can I run both pipelines simultaneously?**  
A: Yes, but ensure they target different agents or environments to avoid conflicts.

**Q: How long does each pipeline take?**  
A: 
- createagentpipeline.yml: ~5-10 minutes per environment
- agentconsumptionpipeline.yml: ~15-30 minutes (red team testing takes longer)

**Q: Can I customize the agent name?**  
A: Yes, edit the `myAgent` variable in createagent.py and related scripts.

**Q: What if I only have one environment?**  
A: You can modify the YAML to remove test/prod stages or set the same variables for all environments.

**Q: How do I add more environments?**  
A: Duplicate a stage in the YAML, create new variable group, and update environment references.

**Q: Can I integrate with GitHub instead of Azure Repos?**  
A: Yes, Azure Pipelines supports GitHub repositories. Select GitHub when creating the pipeline.

## Support

For issues or questions:

1. **Pipeline Issues**: Check pipeline logs for detailed error messages
2. **Agent Issues**: Review Azure AI Foundry portal for agent status  
3. **Documentation**: Consult Azure DevOps and Azure AI documentation
4. **Access Issues**: Contact your Azure administrator
5. **Security Questions**: Review the security best practices section above

---

## Appendix: YAML File Structure

### createagentpipeline.yml Structure
```
├── Build Stage
│   └── Validate Python & publish artifacts
├── Dev Stage
│   └── Deploy agent to dev
├── Test Stage
│   └── Deploy agent to test
└── Prod Stage
    └── Deploy agent to production (requires approval)
```

### agentconsumptionpipeline.yml Structure
```
├── Build Stage
│   └── Validate all Python scripts & publish artifacts
├── Dev Stage
│   └── Test existing agent (exagent.py)
├── Test Stage
│   ├── Run agent evaluation (agenteval.py)
│   └── Run red team testing (redteam.py)
└── Prod Stage
    └── Verify production agent (exagent.py)
```

---

**Last Updated**: December 2025  
**Version**: 1.0  
**Maintained by**: DevOps Team
