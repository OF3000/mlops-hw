# IAM Роль для Lambda-функцій
resource "aws_iam_role" "lambda_role" {
  name               = "${var.project_name}-lambda-exec-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# 1. Lambda: Validate
resource "aws_lambda_function" "validate" {
  filename         = "${path.module}/lambda/validate.zip"
  function_name    = "${var.project_name}-validate"
  role             = aws_iam_role.lambda_role.arn
  handler          = "validate.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/lambda/validate.zip")
  runtime          = "python3.9"
}

# 2. Lambda: Log Metrics
resource "aws_lambda_function" "log_metrics" {
  filename         = "${path.module}/lambda/log_metrics.zip"
  function_name    = "${var.project_name}-log-metrics"
  role             = aws_iam_role.lambda_role.arn
  handler          = "log_metrics.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/lambda/log_metrics.zip")
  runtime          = "python3.9"
}

# IAM Роль для AWS Step Functions
resource "aws_iam_role" "step_functions_role" {
  name               = "${var.project_name}-sfn-role"
  assume_role_policy = data.aws_iam_policy_document.step_functions_assume_role.json
}

# Дозвіл для Step Functions на виклик конкретних Lambda
resource "aws_iam_policy" "step_functions_lambda_invoke" {
  name = "${var.project_name}-sfn-lambda-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "lambda:InvokeFunction"
        Resource = [
          aws_lambda_function.validate.arn,
          aws_lambda_function.log_metrics.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sfn_policy_attach" {
  role       = aws_iam_role.step_functions_role.name
  policy_arn = aws_iam_policy.step_functions_lambda_invoke.arn
}

# AWS Step Functions State Machine (Validate -> Log Metrics)
resource "aws_sfn_state_machine" "training_pipeline" {
  name     = "${var.project_name}-state-machine"
  role_arn = aws_iam_role.step_functions_role.arn

  definition = jsonencode({
    Comment = "ML Training Pipeline via Step Functions"
    StartAt = "ValidateData"
    States = {
      ValidateData = {
        Type       = "Task"
        Resource   = aws_lambda_function.validate.arn
        ResultPath = "$"
        Next       = "LogMetrics"
      }
      LogMetrics = {
        Type     = "Task"
        Resource = aws_lambda_function.log_metrics.arn
        End      = true
      }
    }
  })
}

output "step_function_arn" {
  description = "ARN of the deployed Step Function"
  value       = aws_sfn_state_machine.training_pipeline.arn
}