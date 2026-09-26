resource "aws_ecr_repository" "inference" {
  name                 = "${var.project_name}-inference"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_s3_bucket" "artifacts" {
  bucket        = "${var.project_name}-artifacts-of3000"
  force_destroy = true
}
