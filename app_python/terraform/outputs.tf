output "public_ip" {
  description = "Public IP of the instance"
  value       = aws_instance.lab4_vm.public_ip
}

output "ssh_command" {
  value = format("ssh -i ~/.ssh/labsuser.pem ubuntu@%s", aws_instance.lab4_vm.public_ip)
}