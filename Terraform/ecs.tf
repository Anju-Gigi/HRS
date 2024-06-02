# Create ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "my-cluster"
}

# Define Task Definition
resource "aws_ecs_task_definition" "app" {
  family = "my-app"
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = "256"
  memory = "512"
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  container_definitions = jsonencode([{
    name = "app"
    image = "627562689753.dkr.ecr.eu-north-1.amazonaws.com/java:latest"
    essential = true
    portMappings = [{
      containerPort = 8080
      hostPort = 8080
    }]
  }])
}

# Define ECS Service
resource "aws_ecs_service" "app_service" {
  name            = "app-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = [aws_subnet.main_subnet.id]
    security_groups  = [aws_security_group.ecs_sg.id]
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8080
  }
}
