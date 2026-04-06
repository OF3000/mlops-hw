variable "region" { default = "eu-central-1" }
variable "vpc_cidr" { default = "10.0.0.0/16" }
variable "azs" { default = ["eu-central-1a", "eu-central-1b"] }
variable "private_subnets" { default = ["10.0.1.0/24", "10.0.2.0/24"] }
variable "public_subnets" { default = ["10.0.101.0/24", "10.0.102.0/24"] }
variable "cluster_name" { default = "mlops-eks" }
variable "cluster_version" { default = "1.29" }