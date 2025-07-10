Here's a **basic Terraform configuration** to provision an **EC2 instance** on AWS:

---

### ✅ Assumptions:

* You have AWS credentials configured (`~/.aws/credentials` or via environment variables).
* You want a **t2.micro** instance in **us-east-1** using **Amazon Linux 2**.
* You want to use an existing **key pair** for SSH (e.g., `my-key`).

---

### 📁 Terraform File Structure:

```shell
ec2-provision/
├── main.tf
├── variables.tf
└── outputs.tf
```

---

### 🔧 `main.tf`

```hcl
provider "aws" {
  region = var.region
}

resource "aws_instance" "my_ec2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  tags = {
    Name = "MyEC2Instance"
  }

  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
}

resource "aws_security_group" "ec2_sg" {
  name        = "allow_ssh_http"
  description = "Allow SSH and HTTP"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

### ⚙️ `variables.tf`

```hcl
variable "region" {
  default = "us-east-1"
}

variable "ami_id" {
  description = "AMI ID for Amazon Linux 2"
  default     = "ami-0c02fb55956c7d316" # Update as per your region
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  description = "Name of the existing EC2 key pair"
  default     = "my-key"
}
```

---

### 📤 `outputs.tf`

```hcl
output "instance_id" {
  value = aws_instance.my_ec2.id
}

output "public_ip" {
  value = aws_instance.my_ec2.public_ip
}
```

---

### 🚀 Deploy Steps:

```bash
terraform init
terraform plan
terraform apply
```

---

### ✅ Optional Add-ons:

* Add `user_data` to install packages or configure instance at boot.
* Use `terraform.tfvars` to override variables.
* Use a dedicated VPC, subnet, and key pair resources if needed.

---

Want me to include **EBS volumes**, **user\_data**, or **attach to a specific subnet**? Let me know.
