"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws

config = pulumi.Config()
region = config.get("region", "us-east-1")
instance_type = config.get("instance_type", "t2.micro")
key_name = config.require("key_name")
allowed_ssh_ip = config.require("allowed_ssh_ip")

ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["099720109477"],
    filters=[
        {"name": "name", "values": ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]},
        {"name": "virtualization-type", "values": ["hvm"]},
    ],
)

vpc = aws.ec2.Vpc("lab4-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={"Name": "lab4-vpc"}
)

subnet = aws.ec2.Subnet("lab4-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    availability_zone=f"{region}a",
    tags={"Name": "lab4-subnet"}
)

igw = aws.ec2.InternetGateway("lab4-igw",
    vpc_id=vpc.id,
    tags={"Name": "lab4-igw"}
)

route_table = aws.ec2.RouteTable("lab4-rt",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        gateway_id=igw.id,
    )],
    tags={"Name": "lab4-rt"}
)

route_table_assoc = aws.ec2.RouteTableAssociation("lab4-rta",
    subnet_id=subnet.id,
    route_table_id=route_table.id
)

sg = aws.ec2.SecurityGroup("lab4-sg",
    name="lab4-sg",
    description="Allow SSH, HTTP, port 5000",
    vpc_id=vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            description="SSH from my IP",
            from_port=22,
            to_port=22,
            protocol="tcp",
            cidr_blocks=[allowed_ssh_ip],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            description="HTTP",
            from_port=80,
            to_port=80,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            description="Custom port 5000",
            from_port=5000,
            to_port=5000,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        from_port=0,
        to_port=0,
        protocol="-1",
        cidr_blocks=["0.0.0.0/0"],
    )],
    tags={"Name": "lab4-sg"}
)

instance = aws.ec2.Instance("lab4-vm",
    instance_type=instance_type,
    ami=ami.id,
    key_name=key_name,
    subnet_id=subnet.id,
    vpc_security_group_ids=[sg.id],
    root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
        volume_size=8,
        volume_type="gp3",
    ),
    tags={"Name": "lab4-vm"}
)

pulumi.export("public_ip", instance.public_ip)
pulumi.export("ssh_command", instance.public_ip.apply(lambda ip: f"ssh -i ~/.ssh/labsuser.pem ubuntu@{ip}"))
