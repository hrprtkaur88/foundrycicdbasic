# GitHub Actions CI/CD for AI Agent Deployment

This directory contains GitHub Actions workflows for deploying AI agents across multiple environments.

## 🚀 Quick Start

1. **Fork/Clone** this repository to your GitHub account
2. **Set up Azure resources** for each environment (dev, test, prod)
3. **Configure GitHub Secrets** (see below)
4. **Create GitHub Environments** with protection rules
5. **Push to main branch** to trigger the workflow

**Estimated Setup Time**: 20-30 minutes

---

## Workflow Files

### 1. `create-agent-multi-env.yml`
**Purpose**: Creates and deploys AI agents across dev, test, and production environments.

**Jobs**:
- **Build**: Validates Python code and creates artifacts
- **Deploy-Dev**: Deploys agent to development environment
- **Deploy-Test**: Deploys agent to test environment (after dev succeeds)
- **Deploy-Prod**: Deploys agent to production (after test succeeds, requires approval)

**Triggers**:
- Push to `main` or `develop` branches
- Changes to `createagent.py`, `requirements.txt`, or workflow file
- Manual trigger via GitHub UI

**Use this when**: You need to create or update agents across all environments.

---

### 2. `agent-consumption-multi-env.yml`
**Purpose**: Tests, evaluates, and security-tests existing AI agents without creating new ones.

**Jobs**:
- **Build**: Validates all test scripts (exagent.py, agenteval.py, redteam.py)
- **Test-Dev**: Tests existing agent with `exagent.py` in dev
- **Evaluate-Test**: Runs comprehensive agent evaluation with metrics
- **Red-Team-Test**: Performs security testing with multiple attack strategies
- **Verify-Prod**: Verifies production agent functionality

**Triggers**:
- Push to `main` or `develop` branches
- Changes to test scripts or workflow file
- Manual trigger via GitHub UI
- Weekly schedule (Monday 2 AM UTC) for automated security testing

**Use this when**: You want to validate agent behavior, evaluate performance metrics, and perform security testing on existing deployed agents.

**Key Features**:
- 📊 Evaluation metrics (tool call accuracy, intent resolution, task adherence, response completeness)
- 🔒 Red team security testing (11+ attack strategies)
- 📁 Publishes security results as artifacts
- ⏰ Scheduled weekly security scans
- 45-minute timeout for red team testing

---

## Setting Up GitHub Actions

### Step 1: Create Azure Service Principals

For each environment (dev, test, prod), create a service principal:

```bash
# For Dev Environment
az ad sp create-for-rbac \
  --name "github-actions-dev" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{dev-resource-group} \
  --sdk-auth

# For Test Environment
az ad sp create-for-rbac \
  --name "github-actions-test" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{test-resource-group} \
  --sdk-auth

# For Production Environment
az ad sp create-for-rbac \
  --name "github-actions-prod" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{prod-resource-group} \
  --sdk-auth
```

**Save the output JSON** - you'll need it for GitHub Secrets.

Expected output format:
```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  ...
}
```

### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each of the following:

#### Global Secrets (used across all environments)
```
AZURE_SUBSCRIPTION_ID = your-subscription-id
AZURE_TENANT_ID = your-tenant-id
```

#### Dev Environment Secrets
```
AZURE_CREDENTIALS_DEV = {entire JSON output from dev service principal}
AZURE_AI_PROJECT_DEV = https://your-dev-project.api.azureml.ms
AZURE_CLIENT_ID_DEV = dev-service-principal-client-id
```

#### Test Environment Secrets
```
AZURE_CREDENTIALS_TEST = {entire JSON output from test service principal}
AZURE_AI_PROJECT_TEST = https://your-test-project.api.azureml.ms
AZURE_AI_PROJECT_ENDPOINT_TEST = https://your-test-project.api.azureml.ms
AZURE_OPENAI_ENDPOINT_TEST = https://your-test-openai.openai.azure.com/
AZURE_OPENAI_KEY_TEST = your-test-openai-api-key
AZURE_OPENAI_API_VERSION_TEST = 2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_TEST = gpt-4o
AZURE_CLIENT_ID_TEST = test-service-principal-client-id
```

**Note**: Additional OpenAI secrets are required for the evaluation and red team testing workflows.

#### Production Environment Secrets
```
AZURE_CREDENTIALS_PROD = {entire JSON output from prod service principal}
AZURE_AI_PROJECT_PROD = https://your-prod-project.api.azureml.ms
AZURE_CLIENT_ID_PROD = prod-service-principal-client-id
```

**Note**: The `AZURE_CREDENTIALS_*` secrets should contain the **entire JSON** output from the `az ad sp create-for-rbac` command.

### Step 3: Create GitHub Environments

1. Go to **Settings** → **Environments**
2. Click **New environment**

#### Create Dev Environment
- Name: `dev`
- Protection rules: None (for faster development)
- Click **Configure environment**

#### Create Test Environment
- Name: `test`
- Protection rules (optional):
  - ☑️ **Required reviewers**: Add team members who should approve test deployments
  - Set **Wait timer**: 0 minutes (or add delay if needed)
- Click **Configure environment**

#### Create Production Environment
- Name: `production`
- Protection rules (recommended):
  - ☑️ **Required reviewers**: Add required approvers (e.g., tech lead, manager)
  - ☑️ **Wait timer**: 5 minutes (gives time to review)
  - ☑️ **Deployment branches**: Only `main` branch
- Click **Configure environment**

### Step 4: Grant Service Principal Permissions

For each service principal, grant the necessary Azure permissions:

```bash
# Assign Cognitive Services Contributor role
az role assignment create \
  --assignee {service-principal-client-id} \
  --role "Cognitive Services Contributor" \
  --scope /subscriptions/{subscription-id}/resourceGroups/{resource-group}

# Assign Azure AI Developer role
az role assignment create \
  --assignee {service-principal-client-id} \
  --role "Azure AI Developer" \
  --scope /subscriptions/{subscription-id}/resourceGroups/{resource-group}
```

### Step 5: Test the Workflow

1. Make a small change to `createagent.py` or `requirements.txt`
2. Commit and push to the `main` branch:
   ```bash
   git add .
   git commit -m "Test workflow deployment"
   git push origin main
   ```
3. Go to **Actions** tab in GitHub
4. Click on the running workflow
5. Monitor each job's progress
6. Approve deployments when prompted (for test/prod)

---

## Workflow Features

### ✅ Automatic Triggers
- Runs on push to `main` or `develop` branches
- Only triggers when relevant files change
- Supports manual trigger via GitHub UI

### ✅ Environment Isolation
- Separate credentials for each environment
- Sequential deployment: dev → test → prod
- Prevents production deployment if test fails

### ✅ Approval Gates
- Production deployments require manual approval
- Optional approval for test environment
- Configurable wait timers

### ✅ Artifact Management
- Build artifacts once, use across environments
- 30-day retention for troubleshooting
- Includes all necessary files

### ✅ Security
- Credentials stored as encrypted secrets
- Service principals with least-privilege access
- Azure login per job for security isolation

---

## Manual Workflow Trigger

To manually trigger the workflow:

1. Go to **Actions** tab
2. Select **AI Agent - Create & Deploy** workflow
3. Click **Run workflow**
4. Select branch (usually `main`)
5. Click **Run workflow** button

---

## Monitoring and Logs

### View Workflow Runs
1. Go to **Actions** tab
2. Click on a workflow run
3. View logs for each job
4. Download artifacts if needed

### View Deployment Status
- **Dev**: Check status badge (optional, can add to main README)
- **Test**: Review test job logs
- **Prod**: Verify in Azure AI Foundry portal

### Download Artifacts
1. Click on completed workflow run
2. Scroll to **Artifacts** section at bottom
3. Click **agent-scripts** to download

---

## Troubleshooting

### Authentication Failures

**Problem**: Azure login fails with "Invalid credentials"

**Solutions**:
- Verify `AZURE_CREDENTIALS_*` secrets contain complete JSON from service principal creation
- Ensure service principal hasn't expired
- Check that JSON is properly formatted (no extra spaces/newlines)
- Verify subscription ID matches in secrets and service principal

### Workflow Not Triggering

**Problem**: Workflow doesn't run on push

**Solutions**:
- Check that changed files match the `paths` filter in workflow
- Verify branch name matches `branches` filter (`main` or `develop`)
- Check if Actions are enabled: Settings → Actions → General → Allow all actions

### Environment Not Found

**Problem**: "Environment `dev` not found" error

**Solutions**:
- Create environments in Settings → Environments
- Ensure names match exactly: `dev`, `test`, `production`
- Check that repository settings allow environment usage

### Secret Not Available

**Problem**: "Secret AZURE_AI_PROJECT_DEV not found"

**Solutions**:
- Verify secret name matches exactly (case-sensitive)
- Check secret is created at repository level (not organization level)
- Ensure environment-specific secrets are configured

### Permission Denied on Azure Resources

**Problem**: "Authorization failed" when deploying agent

**Solutions**:
- Verify service principal has required roles:
  - Cognitive Services Contributor
  - Azure AI Developer
- Check resource group/subscription scope is correct
- Wait 5-10 minutes for role assignments to propagate

### Python Module Not Found

**Problem**: "ModuleNotFoundError" in deployment step

**Solutions**:
- Verify `requirements.txt` includes all dependencies
- Check pip install step completed successfully
- Review dependency versions for compatibility
- Ensure Python version matches (3.11)

---

## Workflow Comparison

| Feature | create-agent-multi-env.yml | agent-consumption-multi-env.yml |
|---------|---------------------------|--------------------------------|
| **Purpose** | Create/Deploy agents | Test/Evaluate existing agents |
| **Agent Creation** | ✅ Yes (all environments) | ❌ No |
| **Agent Testing** | ❌ No | ✅ Yes (exagent.py) |
| **Evaluation Metrics** | ❌ No | ✅ Yes (agenteval.py) |
| **Red Team Testing** | ❌ No | ✅ Yes (redteam.py) |
| **Scheduled Runs** | ❌ No | ✅ Weekly security scans |
| **Artifacts Published** | agent-scripts | agent-test-scripts, redteam-results |
| **Typical Duration** | 5-10 minutes | 15-45 minutes |
| **Best Used For** | Initial deployment, updates | Quality assurance, security testing |

### Recommended Workflow

1. **Create Agents**: Run `create-agent-multi-env.yml` to deploy agents to dev → test → prod
2. **Test & Validate**: Run `agent-consumption-multi-env.yml` to validate behavior and security
3. **Monitor**: Review artifacts, logs, and evaluation metrics
4. **Iterate**: Make improvements based on findings and repeat

---

## Comparing with Azure DevOps

| Feature | GitHub Actions | Azure DevOps |
|---------|---------------|--------------|
| **Setup Complexity** | Simple | Moderate |
| **Cost** | Free for public repos | Free tier available |
| **Integration** | Native GitHub | Separate platform |
| **Approval Process** | Environment protection rules | Environment approvals |
| **Secrets Management** | GitHub Secrets | Variable Groups |
| **Artifact Storage** | GitHub Artifacts | Azure Artifacts |
| **Scheduled Runs** | CRON expressions | Scheduled triggers |
| **Best For** | GitHub-based projects | Enterprise Azure projects |

---

## Best Practices

### 🔒 Security
- ✅ Rotate service principal credentials regularly (every 90 days)
- ✅ Use separate service principals per environment
- ✅ Enable secret scanning in repository settings
- ✅ Review audit logs regularly

### 🚀 Deployment
- ✅ Always test in dev before promoting to test/prod
- ✅ Use semantic versioning for releases
- ✅ Tag production deployments with git tags
- ✅ Maintain deployment logs and change history

### 📊 Monitoring
- ✅ Set up notifications for workflow failures
- ✅ Monitor Azure AI Foundry for agent health
- ✅ Track deployment frequency and success rate
- ✅ Review logs regularly for issues

### 🔄 Workflow Optimization
- ✅ Use caching for pip dependencies (already implemented)
- ✅ Run independent jobs in parallel when possible
- ✅ Keep workflows focused and modular
- ✅ Document any custom steps or requirements

---

## Advanced Configuration

### Adding Status Badges

Add to your main README.md:

```markdown
![Create Agent Workflow](https://github.com/{owner}/{repo}/actions/workflows/create-agent-multi-env.yml/badge.svg)
```

### Conditional Deployment

Deploy to prod only on specific tags:

```yaml
deploy-prod:
  if: startsWith(github.ref, 'refs/tags/v')
  # ... rest of job
```

### Slack/Teams Notifications

Add notification step after deployment:

```yaml
- name: Notify Success
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Matrix Strategy

Deploy to multiple regions:

```yaml
strategy:
  matrix:
    region: [eastus, westus, westeurope]
```

---

## Migration from Azure DevOps

If you're migrating from Azure DevOps pipelines:

1. **Export Variables**: Copy variable group values to GitHub Secrets
2. **Service Connections**: Create equivalent service principals
3. **Environments**: Recreate environments with same approval rules
4. **Triggers**: Adjust branch and path filters as needed
5. **Test**: Run workflow in parallel with Azure DevOps until validated

---

## Additional Resources

### Documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure Login Action](https://github.com/Azure/login)
- [Azure CLI in GitHub Actions](https://docs.microsoft.com/en-us/azure/developer/github/connect-from-azure)
- [Managing Secrets in GitHub](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

### Useful Commands

**Create service principal:**
```bash
az ad sp create-for-rbac --name "github-sp" --role contributor --scopes /subscriptions/{sub-id} --sdk-auth
```

**Test Azure login locally:**
```bash
az login --service-principal -u {client-id} -p {client-secret} --tenant {tenant-id}
```

**Validate workflow syntax:**
```bash
# Install actionlint
brew install actionlint  # macOS
# Or download from https://github.com/rhysd/actionlint

# Validate workflow file
actionlint .github/workflows/create-agent-multi-env.yml
```

---

## FAQ

**Q: Which workflow should I run first?**  
A: Run `create-agent-multi-env.yml` first to create agents, then `agent-consumption-multi-env.yml` to test them.

**Q: Can I run both workflows simultaneously?**  
A: Yes, they operate independently. The consumption workflow tests existing agents.

**Q: How long does red team testing take?**  
A: Typically 15-30 minutes, with a 45-minute timeout. It depends on the number of attack strategies and API rate limits.

**Q: Can I deploy to specific environments only?**  
A: Yes, use manual workflow trigger and modify the workflow to accept environment input.

**Q: How do I rollback a deployment?**  
A: Re-run a previous successful workflow or revert the code and push.

**Q: Why is red team testing set to `continue-on-error: true`?**  
A: Red team testing can be resource-intensive and may occasionally timeout. This prevents it from blocking the pipeline while still capturing results.

**Q: Can I disable the weekly scheduled security scan?**  
A: Yes, remove or comment out the `schedule` trigger in `agent-consumption-multi-env.yml`.

**Q: How do I view red team security results?**  
A: Go to the workflow run → Artifacts → Download `redteam-results-test` JSON file.

**Q: Can I deploy to multiple regions?**  
A: Yes, use matrix strategy or create separate jobs for each region.

**Q: Is this compatible with GitHub Enterprise?**  
A: Yes, GitHub Actions work the same on Enterprise with self-hosted runners.

**Q: Can I use managed identity instead of service principal?**  
A: Yes, if using self-hosted runners on Azure VMs, you can use managed identity.

**Q: How do I limit who can approve production deployments?**  
A: Configure "Required reviewers" in the production environment settings.

**Q: What evaluation metrics are tracked?**  
A: Tool call accuracy, intent resolution, task adherence, and response completeness.

---

## Support

For issues or questions:

1. **Workflow Issues**: Check Actions logs and workflow syntax
2. **Azure Issues**: Verify service principal permissions and Azure resources
3. **GitHub Issues**: Review repository settings and permissions
4. **Security Issues**: Contact repository administrators

---

**Last Updated**: December 2025  
**Version**: 1.0  
**Compatible with**: GitHub Actions, Azure AI Foundry, Python 3.11+
