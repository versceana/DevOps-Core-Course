# Lab 4: Infrastructure as Code (Terraform & Pulumi)

> Author: Diana Yakupova  
> Group: B23-CBS-02  
> Date: February 19th 2026

## Cloud Provider & Infrastructure

- **Provider:** Amazon Web Services (AWS), region `us-east-1`.
- **Instance type:** `t2.micro` (AWS Free Tier eligible).
- **Resources created:** VPC, public subnet, Internet Gateway, route table, security group, EC2 instance.
- **Rationale:** AWS Academy provides a stable lab environment with free tier access, suitable for learning IaC concepts without incurring costs.

## Terraform Implementation

- **Version:** `1.5.7`
- **Project structure:** `main.tf`, `variables.tf`, `outputs.tf`, `terraform.tfvars` (gitignored).
- **Key steps:**
  - Configured AWS provider with region `us-east-1`.
  - Created VPC, subnet, Internet Gateway, route table, security group (ports 22, 80, 5000).
  - Launched EC2 instance with Ubuntu 24.04 AMI and key pair `vockey`.
- **Execution:**
  ```bash
  terraform init
  terraform fmt
  terraform validate
  terraform plan
  terraform apply -auto-approve
  ```
- **Outputs:** `public_ip = 100.29.38.71`, `ssh_command = ssh -i ~/.ssh/labsuser.pem ubuntu@100.29.38.71`
- **SSH verification:** Successfully connected.
  <!-- ВСТАВИТЬ СКРИНШОТ 1: SSH к Terraform VM (терминал с приветствием Ubuntu) -->
- **Cleanup:** `terraform destroy -auto-approve` executed, all resources removed.
  <!-- ВСТАВИТЬ СКРИНШОТ 2: Вывод terraform destroy (сообщение Destroy complete) -->

## Pulumi Implementation

- **Version:** `3.221.0`
- **Language:** Python
- **Project structure:** `__main__.py`, `requirements.txt`, `Pulumi.yaml`, `Pulumi.dev.yaml`.
- **Configuration:**
  ```bash
  pulumi config set aws:region us-east-1
  pulumi config set key_name vockey
  pulumi config set allowed_ssh_ip 45.85.105.206/32 --secret
  ```
- **Key steps:** Code in `__main__.py` declares the same AWS resources as Terraform (VPC, subnet, Internet Gateway, route table, security group, EC2 instance).
- **Execution:**
  ```bash
  pulumi preview
  pulumi up -y
  ```
  <!-- ВСТАВИТЬ СКРИНШОТ 3: Вывод pulumi preview -->
  <!-- ВСТАВИТЬ СКРИНШОТ 4: Вывод pulumi up с финальным IP (54.159.8.55) -->
- **Outputs:** `public_ip = 54.159.8.55`, `ssh_command = ssh -i ~/.ssh/labsuser.pem ubuntu@54.159.8.55`
- **SSH verification:** Successfully connected.
  <!-- ВСТАВИТЬ СКРИНШОТ 5: SSH к Pulumi VM (терминал с приветствием Ubuntu) -->
- **Cleanup status:** VM is kept running for Lab 5 (Ansible).

## Terraform vs Pulumi Comparison

| Criteria             | Terraform                                                           | Pulumi                                                                              |
| -------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Ease of learning** | HCL is simple for static infra, but learning curve for expressions. | Python is familiar, but requires understanding of Pulumi's object model.            |
| **Code readability** | Declarative blocks, easy to see the desired state.                  | Imperative code, more flexible but can be more verbose.                             |
| **Debugging**        | Error messages can be cryptic, `terraform plan` helps.              | Python stack traces are clearer, IDE support helps.                                 |
| **Documentation**    | Extensive, mature, huge community.                                  | Good, rapidly growing, but smaller community.                                       |
| **State management** | Local `terraform.tfstate` (or remote).                              | Pulumi Cloud (free tier) handles state and secrets.                                 |
| **Use case**         | Excellent for pure infrastructure provisioning, wide cloud support. | Great when you need programming logic (loops, conditionals) in infrastructure code. |

**Personal preference:** Pulumi feels more natural as a developer due to using Python, but Terraform is still the industry standard for many teams. Both are powerful.

## Screenshots

1. SSH to Terraform VM (`100.29.38.71`)
2. `terraform destroy` output
3. `pulumi preview` output
4. `pulumi up` output (showing `54.159.8.55`)
5. SSH to Pulumi VM (`54.159.8.55`)
