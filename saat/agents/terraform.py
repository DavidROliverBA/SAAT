"""Terraform Agent - Generates infrastructure-as-code from C4 architecture models."""

from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from saat.agents.base import BaseAgentWithChecklist
from saat.models import AgentChecklist, C4Model, ChecklistItem


class TerraformResource(BaseModel):
    """Terraform resource definition."""

    resource_type: str = Field(..., description="e.g., aws_instance, aws_rds_instance")
    resource_name: str = Field(..., description="Terraform resource name")
    configuration: dict[str, Any] = Field(default_factory=dict)
    depends_on: list[str] = Field(default_factory=list)


class TerraformModule(BaseModel):
    """Terraform module definition."""

    name: str
    source: str
    version: Optional[str] = None
    variables: dict[str, Any] = Field(default_factory=dict)


class TerraformConfiguration(BaseModel):
    """Complete Terraform configuration."""

    provider: str = Field(..., description="aws, azure, or gcp")
    region: str = Field(default="us-east-1")
    project_name: str
    resources: list[TerraformResource] = Field(default_factory=list)
    modules: list[TerraformModule] = Field(default_factory=list)
    variables: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, str] = Field(default_factory=dict)
    tags: dict[str, str] = Field(default_factory=dict)


class TerraformDependencies:
    """Dependencies for Terraform generation."""

    def __init__(
        self, model: C4Model, provider: str = "aws", region: str = "us-east-1"
    ):
        self.model = model
        self.provider = provider
        self.region = region
        self.generated_resources: list[TerraformResource] = []


def create_terraform_agent(
    model_name: str = "anthropic:claude-sonnet-4",
) -> Agent[TerraformDependencies, TerraformConfiguration]:
    """Create Terraform generation agent.

    Args:
        model_name: Model identifier

    Returns:
        Configured PydanticAI agent
    """
    agent: Agent[TerraformDependencies, TerraformConfiguration] = Agent(
        model_name,
        deps_type=TerraformDependencies,
        result_type=TerraformConfiguration,
        system_prompt="""You are an expert DevOps engineer specializing in infrastructure-as-code with Terraform.

Generate Terraform configurations from C4 architecture models:

1. **Resource Mapping**
   - Containers → Compute resources (EC2, App Service, Compute Engine)
   - Databases → Managed database services (RDS, Azure SQL, Cloud SQL)
   - Storage → Object storage (S3, Blob Storage, Cloud Storage)
   - Queue systems → Message queues (SQS, Service Bus, Pub/Sub)

2. **Criticality-Based Configuration**
   - **CS1 (Mission Critical)**:
     * Multi-AZ deployment (AWS) or zone-redundant (Azure/GCP)
     * Auto-scaling: min=2, max=10
     * Backup retention: 35 days
     * Monitoring: All metrics, alarms for CPU>70%, errors>5%
     * High-availability load balancers

   - **CS2 (Business Critical)**:
     * Multi-AZ deployment
     * Auto-scaling: min=2, max=5
     * Backup retention: 7 days
     * Monitoring: Key metrics, alarms for CPU>80%

   - **SL1/SL2 (Standard)**:
     * Single-AZ deployment
     * Fixed instance count or minimal auto-scaling
     * Backup retention: 3 days
     * Basic monitoring

   - **STANDARD (Low Priority)**:
     * Single-AZ deployment
     * No auto-scaling
     * No backups
     * Minimal monitoring

3. **Network Architecture**
   - VPC/VNet with public and private subnets
   - Security groups based on interfaces and protocols
   - NAT gateways for private subnets
   - Load balancers for multi-instance deployments

4. **Security**
   - Encryption at rest for CS1/CS2 systems
   - Encryption in transit (TLS) for all external interfaces
   - IAM roles with least privilege
   - Secrets management (Secrets Manager, Key Vault, Secret Manager)

5. **Monitoring & Observability**
   - CloudWatch/Azure Monitor/Cloud Monitoring
   - Log aggregation for CS1/CS2
   - Alarms for critical metrics
   - Dashboard for system health

Generate production-ready Terraform with:
- Clear variable definitions
- Proper resource dependencies
- Appropriate tagging
- Output values for integration
""",
    )

    @agent.tool
    async def map_containers_to_compute(
        ctx: RunContext[TerraformDependencies],
    ) -> dict[str, Any]:
        """Map containers to compute resources.

        Args:
            ctx: Agent context

        Returns:
            Dictionary with compute resource mappings
        """
        model = ctx.deps.model
        provider = ctx.deps.provider
        mappings = []

        for container in model.containers:
            # Determine instance type based on criticality
            if provider == "aws":
                instance_type = {
                    "CS1": "m5.large",
                    "CS2": "m5.large",
                    "SL1": "t3.medium",
                    "SL2": "t3.medium",
                    "STANDARD": "t3.small",
                }.get(container.criticality, "t3.micro")

                multi_az = container.criticality in ["CS1", "CS2"]

                mapping = {
                    "container": container.name,
                    "resource_type": "aws_instance" if not multi_az else "aws_autoscaling_group",
                    "instance_type": instance_type,
                    "multi_az": multi_az,
                    "min_instances": 2 if container.criticality == "CS1" else (2 if container.criticality == "CS2" else 1),
                    "max_instances": 10 if container.criticality == "CS1" else (5 if container.criticality == "CS2" else 1),
                }

            elif provider == "azure":
                sku = {
                    "CS1": "Standard_D2s_v3",
                    "CS2": "Standard_D2s_v3",
                    "SL1": "Standard_B2s",
                    "SL2": "Standard_B2s",
                    "STANDARD": "Standard_B1s",
                }.get(container.criticality, "Standard_B1s")

                mapping = {
                    "container": container.name,
                    "resource_type": "azurerm_linux_virtual_machine",
                    "sku": sku,
                    "zone_redundant": container.criticality in ["CS1", "CS2"],
                }

            elif provider == "gcp":
                machine_type = {
                    "CS1": "n1-standard-2",
                    "CS2": "n1-standard-2",
                    "SL1": "n1-standard-1",
                    "SL2": "n1-standard-1",
                    "STANDARD": "f1-micro",
                }.get(container.criticality, "f1-micro")

                mapping = {
                    "container": container.name,
                    "resource_type": "google_compute_instance",
                    "machine_type": machine_type,
                    "high_availability": container.criticality in ["CS1", "CS2"],
                }

            else:
                mapping = {"container": container.name, "error": "Unsupported provider"}

            mappings.append(mapping)

        return {"provider": provider, "mappings": mappings}

    @agent.tool
    async def generate_database_resources(
        ctx: RunContext[TerraformDependencies],
    ) -> dict[str, Any]:
        """Generate database resource configurations.

        Args:
            ctx: Agent context

        Returns:
            Dictionary with database configurations
        """
        model = ctx.deps.model
        provider = ctx.deps.provider
        databases = []

        for container in model.containers:
            # Check if container has database technology
            db_techs = ["postgresql", "mysql", "mongodb", "redis", "dynamodb"]
            is_database = any(
                tech.lower() in db_tech.lower()
                for tech in container.technology
                for db_tech in db_techs
            )

            if is_database:
                # Determine backup retention based on criticality
                backup_retention = {
                    "CS1": 35,
                    "CS2": 7,
                    "SL1": 3,
                    "SL2": 3,
                    "STANDARD": 0,
                }.get(container.criticality, 0)

                db_config = {
                    "container": container.name,
                    "criticality": container.criticality,
                    "backup_retention_days": backup_retention,
                    "multi_az": container.criticality in ["CS1", "CS2"],
                    "encryption_at_rest": container.criticality in ["CS1", "CS2"],
                }

                if provider == "aws":
                    db_config["resource_type"] = "aws_db_instance"
                    db_config["instance_class"] = (
                        "db.m5.large"
                        if container.criticality in ["CS1", "CS2"]
                        else "db.t3.medium"
                    )
                elif provider == "azure":
                    db_config["resource_type"] = "azurerm_postgresql_server"
                    db_config["sku_name"] = (
                        "GP_Gen5_2"
                        if container.criticality in ["CS1", "CS2"]
                        else "B_Gen5_1"
                    )
                elif provider == "gcp":
                    db_config["resource_type"] = "google_sql_database_instance"
                    db_config["tier"] = (
                        "db-n1-standard-2"
                        if container.criticality in ["CS1", "CS2"]
                        else "db-f1-micro"
                    )

                databases.append(db_config)

        return {"databases": databases}

    @agent.tool
    async def generate_network_config(
        ctx: RunContext[TerraformDependencies],
    ) -> dict[str, Any]:
        """Generate VPC/network configuration.

        Args:
            ctx: Agent context

        Returns:
            Dictionary with network configuration
        """
        model = ctx.deps.model
        provider = ctx.deps.provider

        # Analyze relationships to understand network topology
        public_containers = []
        private_containers = []

        for container in model.containers:
            # Check if container has external-facing interfaces
            has_public_interface = any(
                interface.port in [80, 443, 8080]
                for interface in container.interfaces
            )

            if has_public_interface:
                public_containers.append(container.name)
            else:
                private_containers.append(container.name)

        network_config = {
            "provider": provider,
            "public_subnets": len(public_containers),
            "private_subnets": len(private_containers),
            "nat_gateway_required": len(private_containers) > 0,
            "load_balancer_required": any(
                c.criticality in ["CS1", "CS2"] for c in model.containers
            ),
        }

        if provider == "aws":
            network_config["vpc_cidr"] = "10.0.0.0/16"
            network_config["resource_type"] = "aws_vpc"
        elif provider == "azure":
            network_config["address_space"] = ["10.0.0.0/16"]
            network_config["resource_type"] = "azurerm_virtual_network"
        elif provider == "gcp":
            network_config["resource_type"] = "google_compute_network"

        return network_config

    @agent.tool
    async def generate_monitoring_config(
        ctx: RunContext[TerraformDependencies],
    ) -> dict[str, Any]:
        """Generate monitoring and alerting configuration.

        Args:
            ctx: Agent context

        Returns:
            Dictionary with monitoring configuration
        """
        model = ctx.deps.model
        provider = ctx.deps.provider
        alarms = []

        for container in model.containers:
            if container.criticality in ["CS1", "CS2"]:
                # Critical systems get comprehensive monitoring
                alarm_config = {
                    "container": container.name,
                    "metrics": [
                        {"name": "CPUUtilization", "threshold": 70 if container.criticality == "CS1" else 80},
                        {"name": "MemoryUtilization", "threshold": 80},
                        {"name": "ErrorRate", "threshold": 5},
                    ],
                    "log_retention_days": 90 if container.criticality == "CS1" else 30,
                }
                alarms.append(alarm_config)

        monitoring = {
            "provider": provider,
            "alarms": alarms,
            "dashboard_required": len(alarms) > 0,
        }

        return monitoring

    return agent


class TerraformAgent(BaseAgentWithChecklist):
    """Terraform Agent for generating infrastructure-as-code."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize Terraform agent.

        Args:
            model: Model identifier
        """
        super().__init__("TerraformAgent", model)
        self.agent = create_terraform_agent(model)

    async def create_checklist(
        self, task_description: str, context: Optional[dict[str, Any]] = None
    ) -> AgentChecklist:
        """Generate Terraform generation checklist.

        Args:
            task_description: Task description
            context: Should contain 'provider'

        Returns:
            AgentChecklist
        """
        provider = context.get("provider", "aws") if context else "aws"

        items = [
            ChecklistItem(
                id="1",
                description="Load and analyze C4 model",
                estimated_duration="5s",
            ),
            ChecklistItem(
                id="2",
                description="Map containers to cloud compute resources",
                estimated_duration="15s",
                dependencies=["1"],
            ),
            ChecklistItem(
                id="3",
                description=f"Generate VPC/network configuration for {provider.upper()}",
                estimated_duration="15s",
                dependencies=["1"],
            ),
            ChecklistItem(
                id="4",
                description="Create database resources with criticality-based configs",
                estimated_duration="15s",
                dependencies=["1"],
            ),
            ChecklistItem(
                id="5",
                description="Set up load balancers and auto-scaling",
                estimated_duration="15s",
                dependencies=["2"],
            ),
            ChecklistItem(
                id="6",
                description="Configure backup policies (CS1=35d, CS2=7d)",
                estimated_duration="10s",
                dependencies=["4"],
            ),
            ChecklistItem(
                id="7",
                description="Set up monitoring and alerting",
                estimated_duration="15s",
                dependencies=["2", "4"],
            ),
            ChecklistItem(
                id="8",
                description="Create IAM roles and security policies",
                estimated_duration="15s",
                dependencies=["2", "4"],
            ),
            ChecklistItem(
                id="9",
                description="Generate Terraform files (main.tf, variables.tf, outputs.tf)",
                estimated_duration="10s",
                dependencies=["2", "3", "4", "5", "6", "7", "8"],
            ),
        ]

        return AgentChecklist(
            agent_name=self.agent_name,
            task_description=task_description,
            items=items,
            estimated_total_duration="2-3 minutes",
            requires_approval=True,
        )

    async def generate_terraform(
        self,
        model: C4Model,
        provider: str = "aws",
        region: str = "us-east-1",
        output_dir: str = "infrastructure/",
        auto_approve: bool = False,
    ) -> dict[str, Any]:
        """Generate Terraform infrastructure from C4 model.

        Args:
            model: C4 model to generate from
            provider: Cloud provider (aws, azure, gcp)
            region: Cloud region
            output_dir: Output directory for Terraform files
            auto_approve: Skip approval prompts

        Returns:
            Dictionary with generated files and configuration
        """
        context = {"model": model, "provider": provider, "region": region}

        # Execute with checklist
        result = await self.execute_with_checklist(
            task_description=f"Generate Terraform for {provider.upper()}",
            auto_approve=auto_approve,
            context=context,
        )

        if result["cancelled"]:
            return result

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Perform Terraform generation
        deps = TerraformDependencies(model, provider, region)

        prompt = f"""Generate a complete Terraform configuration for this architecture:

**Model**: {model.metadata.project}
**Provider**: {provider.upper()}
**Region**: {region}
**Systems**: {len(model.systems)}
**Containers**: {len(model.containers)}

Use the tools to:
1. Map containers to compute resources
2. Generate network configuration
3. Create database resources
4. Generate monitoring configuration

Then create a complete TerraformConfiguration with:
- All resources with proper dependencies
- Variables for environment-specific values
- Outputs for resource identifiers
- Appropriate tags for cost tracking

Apply criticality-based configurations as specified.
"""

        agent_result = await self.agent.run(prompt, deps=deps)
        tf_config = agent_result.data

        # Generate Terraform files
        generated_files = []

        # main.tf
        main_tf = self._generate_main_tf(tf_config)
        main_file = output_path / "main.tf"
        main_file.write_text(main_tf)
        generated_files.append(str(main_file))

        # variables.tf
        variables_tf = self._generate_variables_tf(tf_config)
        variables_file = output_path / "variables.tf"
        variables_file.write_text(variables_tf)
        generated_files.append(str(variables_file))

        # outputs.tf
        outputs_tf = self._generate_outputs_tf(tf_config)
        outputs_file = output_path / "outputs.tf"
        outputs_file.write_text(outputs_tf)
        generated_files.append(str(outputs_file))

        # terraform.tfvars.example
        tfvars = self._generate_tfvars_example(tf_config)
        tfvars_file = output_path / "terraform.tfvars.example"
        tfvars_file.write_text(tfvars)
        generated_files.append(str(tfvars_file))

        result["terraform_config"] = tf_config
        result["generated_files"] = generated_files
        result["output_dir"] = output_dir
        result["summary"] = {
            "provider": provider,
            "total_resources": len(tf_config.resources),
            "total_files": len(generated_files),
        }

        return result

    def _generate_main_tf(self, config: TerraformConfiguration) -> str:
        """Generate main.tf content."""
        tf = f"""# Generated by SAAT - {config.project_name}
# Provider: {config.provider.upper()}

terraform {{
  required_version = ">= 1.0"
  required_providers {{
"""

        if config.provider == "aws":
            tf += """    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
"""
        elif config.provider == "azure":
            tf += """    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
"""
        elif config.provider == "gcp":
            tf += """    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
"""

        tf += """  }
}

"""

        # Provider configuration
        if config.provider == "aws":
            tf += f"""provider "aws" {{
  region = var.region

  default_tags {{
    tags = {{
      Project     = "{config.project_name}"
      ManagedBy   = "Terraform"
      Environment = var.environment
    }}
  }}
}}

"""
        elif config.provider == "azure":
            tf += f"""provider "azurerm" {{
  features {{}}
}}

"""
        elif config.provider == "gcp":
            tf += f"""provider "google" {{
  project = var.project_id
  region  = var.region
}}

"""

        # Resources
        for resource in config.resources:
            tf += f"""
resource "{resource.resource_type}" "{resource.resource_name}" {{
"""
            for key, value in resource.configuration.items():
                if isinstance(value, str):
                    tf += f'  {key} = "{value}"\n'
                elif isinstance(value, bool):
                    tf += f"  {key} = {str(value).lower()}\n"
                elif isinstance(value, (int, float)):
                    tf += f"  {key} = {value}\n"
                else:
                    tf += f"  {key} = {value}\n"

            if resource.depends_on:
                tf += f"  depends_on = [{', '.join(resource.depends_on)}]\n"

            tf += "}\n"

        return tf

    def _generate_variables_tf(self, config: TerraformConfiguration) -> str:
        """Generate variables.tf content."""
        tf = f"""# Variables for {config.project_name}

variable "region" {{
  description = "Cloud region for resources"
  type        = string
  default     = "{config.region}"
}}

variable "environment" {{
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}}

variable "project_name" {{
  description = "Project name for tagging"
  type        = string
  default     = "{config.project_name}"
}}

"""

        if config.provider == "gcp":
            tf += """variable "project_id" {
  description = "GCP project ID"
  type        = string
}

"""

        # Add custom variables from config
        for var_name, var_value in config.variables.items():
            var_type = "string"
            if isinstance(var_value, bool):
                var_type = "bool"
            elif isinstance(var_value, int):
                var_type = "number"
            elif isinstance(var_value, list):
                var_type = "list(string)"

            tf += f"""variable "{var_name}" {{
  description = "{var_name}"
  type        = {var_type}
}}

"""

        return tf

    def _generate_outputs_tf(self, config: TerraformConfiguration) -> str:
        """Generate outputs.tf content."""
        tf = f"""# Outputs for {config.project_name}

"""

        for output_name, output_value in config.outputs.items():
            tf += f"""output "{output_name}" {{
  description = "{output_name}"
  value       = {output_value}
}}

"""

        return tf

    def _generate_tfvars_example(self, config: TerraformConfiguration) -> str:
        """Generate terraform.tfvars.example content."""
        tfvars = f"""# Example Terraform variables for {config.project_name}
# Copy this file to terraform.tfvars and customize

region       = "{config.region}"
environment  = "dev"
project_name = "{config.project_name}"

"""

        if config.provider == "gcp":
            tfvars += """project_id = "your-gcp-project-id"

"""

        for var_name, var_value in config.variables.items():
            if isinstance(var_value, str):
                tfvars += f'{var_name} = "{var_value}"\n'
            else:
                tfvars += f"{var_name} = {var_value}\n"

        return tfvars


async def generate_terraform(
    model: C4Model,
    provider: str = "aws",
    region: str = "us-east-1",
    output_dir: str = "infrastructure/",
    model_name: str = "anthropic:claude-sonnet-4",
    auto_approve: bool = False,
) -> dict[str, Any]:
    """Convenience function to generate Terraform.

    Args:
        model: C4 model
        provider: Cloud provider
        region: Cloud region
        output_dir: Output directory
        model_name: Model to use
        auto_approve: Skip approval prompts

    Returns:
        Dictionary with results
    """
    agent = TerraformAgent(model_name)
    result = await agent.generate_terraform(
        model, provider, region, output_dir, auto_approve
    )

    if result.get("cancelled"):
        raise ValueError("Terraform generation was cancelled")

    return result
