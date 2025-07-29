  graph TD
    A[Terraform Configuration] --> B[aws_lb "my_alb"<br>ALB Resource]
    B --> C[Attach to Subnets<br>(public/private)]
    B --> D[Associate Security Group]
    B --> E[aws_lb_target_group<br>Defines backend targets]
    E --> F[aws_lb_listener<br>Defines rules & ports]
    F --> G[EC2 / ECS / Lambda<br>Target services]
