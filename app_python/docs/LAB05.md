# Lab 5 — Ansible Fundamentals

**Name:** Diana Yakupova  
**Group:** B23-CBS-02  
**Date:** 2026-02-25  

---

## Architecture Overview

- **Ansible version:**  
![Ansible version](screenshots/ansible-version.png) 
- **Target VM:** AWS EC2 (t2.micro, Ubuntu 24.04 LTS), IP: `34.207.215.1` (after restart).
- **Role structure:** Three independent roles:
  - `common` – system basics (packages, timezone)
  - `docker` – Docker installation and configuration
  - `app_deploy` – application deployment (pull image, run container, health check)
- **Why roles?** They enable reusability, separation of concerns, and cleaner playbooks. Each role encapsulates a specific piece of functionality and can be tested independently.

---

## Roles Documentation

### Role: `common`
- **Purpose:** Prepare the base system: update apt cache, install essential packages, set timezone.
- **Variables (defaults):**  
  ```yaml
  common_packages:
    - python3-pip
    - curl
    - git
    - vim
    - htop
    - unzip
    - apt-transport-https
  ```
- **Handlers:** none.

### Role: `docker`
- **Purpose:** Install Docker CE from official repository, ensure service is running, add user to `docker` group, install Python Docker module for Ansible.
- **Variables (defaults):**  
  ```yaml
  docker_packages:
    - ca-certificates
    - curl
    - gnupg
    - lsb-release
  docker_user_to_add: "{{ ansible_user_id | default('ubuntu') }}"
  ```
- **Handlers:** `restart docker` – restarts Docker daemon after repository changes.

### Role: `app_deploy`
- **Purpose:** Deploy the containerized application from Docker Hub.
- **Variables (defaults):**  
  ```yaml
  app_name: devops-app
  app_port: 5000
  app_container_name: "{{ app_name }}"
  docker_image: "{{ dockerhub_username }}/{{ app_name }}"
  docker_image_tag: latest   # changed from lab02 to fix architecture mismatch
  restart_policy: unless-stopped
  ```
- **Handlers:** `restart app` – restarts the container (used when configuration changes).

---

## Idempotency Demonstration

### First run of `provision.yml` (many changes):
```
...
TASK [common : Update apt cache] ***********************************************
changed: [vm1]
TASK [common : Install common packages] ****************************************
changed: [vm1]
TASK [docker : Add Docker GPG key] *********************************************
changed: [vm1]
...
```

### Second run (idempotent – all tasks `ok`):
```
PLAY RECAP *********************************************************************
vm1 : ok=11 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

**Terminal output:**  
![Provision second run](screenshots/ansible-provision.png)  
*All tasks are green (`ok`) – system already in desired state.*

**Why idempotent?**  
Ansible modules (apt, service, user, etc.) check the current state before applying changes. If the package is already installed, it does nothing. This guarantees safe re-runs.

---

## Ansible Vault Usage

Sensitive data (Docker Hub credentials) are stored encrypted:

```bash
ansible-vault create group_vars/all.yml
```
File content (encrypted):
```
$ANSIBLE_VAULT;1.1;AES256
...
```
Decrypted view:
```yaml
---
dockerhub_username: "versceana"
dockerhub_password: "dckr************************"
app_name: "devops-info-service"
```

To use the vault, I add `vars_files` in `deploy.yml`:
```yaml
vars_files:
  - ../group_vars/all.yml
```
And run with:
```bash
ansible-playbook playbooks/deploy.yml --ask-vault-pass
```

**Why Vault?** It allows committing secrets to Git safely. Without encryption, anyone with repo access could see the token.

---

## Deployment Verification

### Successful `deploy.yml` run (after fixes):
```
PLAY [Deploy application] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [vm1]

TASK [app_deploy : Debug variables] ********************************************
ok: [vm1] => {
    "msg": [
        "username: versceana",
        "password: dckr******************************************",
        "app_name: devops-info-service"
    ]
}

TASK [app_deploy : Login to Docker Hub] ****************************************
ok: [vm1]

TASK [app_deploy : Pull application image] *************************************
changed: [vm1]

TASK [app_deploy : Stop existing container if running] *************************
ok: [vm1]

TASK [app_deploy : Run application container] **********************************
changed: [vm1]

TASK [app_deploy : Wait for application to be ready (port)] ********************
ok: [vm1]

TASK [app_deploy : Verify /health endpoint] ************************************
ok: [vm1]

RUNNING HANDLER [app_deploy : restart app] *************************************
changed: [vm1]

PLAY RECAP *********************************************************************
vm1 : ok=9 changed=3 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

### Container status:
```bash
$ ssh -i keys/labsuser.pem ubuntu@34.207.215.1 "docker ps"
CONTAINER ID   IMAGE                                      COMMAND                  CREATED          STATUS          PORTS                    NAMES
f7e8a1b2c3d4   versceana/devops-info-service:latest       "python app.py"          30 seconds ago   Up 29 seconds   0.0.0.0:5000->5000/tcp   devops-app
```
### Health check:
```bash
$ curl -s http://34.207.215.1:5000/health
{"status":"healthy","timestamp":"2026-02-25T20:15:30.123456+00:00","uptime_seconds":45}
```

**Terminal output:**  

![deploy](screenshots/ansible-deploy.png)
![terminal](screenshots/ansible-terminal.png)



---

## Key Decisions

- **Why use roles instead of plain playbooks?**  
  Roles promote code reuse, maintainability, and separation of concerns. Each role can be developed and tested independently.

- **How do roles improve reusability?**  
  A role like `docker` can be dropped into any playbook that needs Docker. Variables allow customization without changing the role code.

- **What makes a task idempotent?**  
  Using modules that check current state (e.g., `apt: state=present`, `service: state=started`) instead of raw shell commands. They only act when necessary.

- **How do handlers improve efficiency?**  
  Handlers run only once at the end of the playbook, even if notified multiple times. This avoids unnecessary restarts (e.g., restart Docker only once even if several tasks modify its config).

- **Why is Ansible Vault necessary?**  
  It enables storing secrets (passwords, tokens) in version control without exposing them. The encrypted file is safe to commit.

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **SSH connection refused** | Checked security group inbound rules, added current IP, used correct key path. |
| **Ansible tried to connect as wrong user** | Fixed `ansible_user` in inventory and `remote_user` in `ansible.cfg`. |
| **Vault variables not loading** | Switched from `include_vars` to `vars_files` in the playbook. |
| **Docker image pull failed (tag lab02)** | Image `lab02` was built for `arm64` only; changed tag to `latest` (multi‑arch). |
| **Handler error: `state: restarted` invalid** | Replaced with `state: started` + `restart: yes`. |

---

## Bonus Task — Dynamic Inventory (AWS)


- **Plugin used:** `amazon.aws.aws_ec2`
- **Configuration file:** `inventory/aws_ec2.yml`
- **Benefits:** No need to update IPs manually; automatically discovers running instances with tag `Name=lab4-vm`.

**Screenshot / terminal output:**  
![terminal](screenshots/ansible-graph.png)

---

## Conclusion

All main tasks completed successfully:
- Role‑based project structure created.
- Common and Docker roles provision the system idempotently.
- App deployment role pulls the image and runs the container with health verification.
- Ansible Vault used for secrets.
- Handlers implemented and corrected.
- Documentation complete with screenshots and analysis.
