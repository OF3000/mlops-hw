terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. Архівування ваших Lambda функцій
data "archive_file" "validate_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/validate.py"
  output_path = "${path.module}/lambda/validate.zip"
}

data "archive_file" "log_metrics_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/log_metrics.py"
  output_path = "${path.module}/lambda/log_metrics.zip"
}

# 2. IAM Роль для Lambda (з принципом найменших привілеїв)
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# 3. Ваші Lambda функції з lesson10
resource "aws_lambda_function" "validate" {
  filename         = data.archive_file.validate_zip.output_path
  function_name    = "${var.project_name}-validate"
  role             = aws_iam_role.lambda_role.arn
  handler          = "validate.lambda_handler"
  runtime          = "python3.10"
  source_code_hash = data.archive_file.validate_zip.output_base64sha256
  timeout          = 30
}

resource "aws_lambda_function" "log_metrics" {
  filename         = data.archive_file.log_metrics_zip.output_path
  function_name    = "${var.project_name}-log-metrics"
  role             = aws_iam_role.lambda_role.arn
  handler          = "log_metrics.lambda_handler"
  runtime          = "python3.10"
  source_code_hash = data.archive_file.log_metrics_zip.output_base64sha256
  timeout          = 30
}

# 4. IAM Роль для Step Functions
resource "aws_iam_role" "sfn_role" {
  name = "${var.project_name}-sfn-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "states.amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "sfn_lambda_invoke" {
  name = "${var.project_name}-sfn-invoke-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "lambda:InvokeFunction"
      Resource = [
        aws_lambda_function.validate.arn,
        aws_lambda_function.log_metrics.arn
      ]
    }]
  })
}

resource "aws_iam_role_policy_attachment" "sfn_invoke_attach" {
  role       = aws_iam_role.sfn_role.name
  policy_arn = aws_iam_policy.sfn_lambda_invoke.arn
}

# 5. AWS Step Functions State Machine (Validate -> Train -> Eval -> Register)
resource "aws_sfn_state_machine" "pipeline" {
  name     = "${var.project_name}-training-pipeline"
  role_arn = aws_iam_role.sfn_role.arn

  definition = jsonencode({
    Comment = "Final MLOps 4-Step Pipeline based on Lesson 10"
    StartAt = "ValidateData"
    States = {
      ValidateData = {
        Type       = "Task"
        Resource   = aws_lambda_function.validate.arn
        ResultPath = "$.validation_result"
        Next       = "TrainModel"
      }
      TrainModel = {
        Type = "Pass"
        Result = {
          status     = "TRAINED"
          model_name = "IrisClassifier"
          version    = "v1.0.0"
        }
        ResultPath = "$.training_result"
        Next       = "EvaluateModel"
      }
      EvaluateModel = {
        Type = "Pass"
        Result = {
          accuracy         = 0.96
          f1_score         = 0.95
          passed_threshold = true
        }
        ResultPath = "$.eval_result"
        Next       = "RegisterAndLogMetrics"
      }
      RegisterAndLogMetrics = {
        Type       = "Task"
        Resource   = aws_lambda_function.log_metrics.arn
        ResultPath = "$.registry_result"
        End        = true
      }
    }
  })
}
