variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "SSH key pair name (vockey)"
  type        = string
}

variable "allowed_ssh_ip" {
  description = "Your public IP with /32"
  type        = string
}