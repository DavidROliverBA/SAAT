---
description: Generate Terraform infrastructure-as-code from C4 model
---

I'll help you generate Terraform infrastructure-as-code from your C4 architecture model.

**What I'll do:**
1. Map C4 containers to cloud resources:
   - Containers → Compute (EC2, App Service, Compute Engine)
   - Databases → Managed databases (RDS, Azure SQL, Cloud SQL)
   - Storage → Object storage (S3, Blob Storage, Cloud Storage)
   - Queues → Message queues (SQS, Service Bus, Pub/Sub)
2. Apply criticality-based configurations:
   - **CS1 (Mission Critical)**:
     - Multi-AZ/zone-redundant deployment
     - Auto-scaling: min=2, max=10
     - Backup retention: 35 days
     - All metrics monitoring, tight alarms
   - **CS2 (Business Critical)**:
     - Multi-AZ deployment
     - Auto-scaling: min=2, max=5
     - Backup retention: 7 days
   - **SL1/SL2 (Standard)**:
     - Single-AZ or minimal redundancy
     - Fixed instances or minimal auto-scaling
     - Backup retention: 3 days
3. Generate networking:
   - VPC/VNet with subnets
   - Security groups/NSGs
   - Load balancers
   - NAT gateways
4. Add monitoring:
   - CloudWatch/Application Insights
   - Log aggregation
   - Alarms based on criticality

**What I need from you:**
1. Path to your C4 model JSON file (e.g., `architecture.json`)
2. Cloud provider: **aws**, **azure**, or **gcp** (default: aws)
3. Region (default: us-east-1 for AWS)
4. Output directory (default: `infrastructure/`)

**Output includes:**
- `main.tf` - Main Terraform configuration with all resources
- `variables.tf` - Configurable variables
- `outputs.tf` - Resource outputs (endpoints, IDs)
- `provider.tf` - Provider configuration
- `networking.tf` - VPC, subnets, security groups
- `monitoring.tf` - CloudWatch/monitoring resources
- `README.md` - Deployment instructions

**Next steps after generation:**
```bash
cd infrastructure/
terraform init
terraform plan
terraform apply
```

Please provide the path to your C4 model, cloud provider, and region.

**Pro tip**: If you've run architecture characteristics analysis (`/saat-analyze-characteristics`), I can include recommended infrastructure (load balancers, caching, monitoring) based on identified gaps!
