variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Prefix for resources"
  type        = string
  default     = "mlops-pipeline"
}