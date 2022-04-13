provider "aws" {
   region = "eu-north-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_vpc" "net" {
  cidr_block = "10.2.0.0/16"
}

resource "aws_subnet" "subnet" {
  vpc_id            = aws_vpc.net.id
  cidr_block        = "10.2.0.0/24"
  availability_zone = "us-west-2a"
}

module "ec2_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  name = "single-instance"

  ami                    = "ami-00514a528eadbc95b"
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.subnet.id
}