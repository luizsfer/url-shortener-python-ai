terraform {
  required_version = ">= 1.0.0"
  
  backend "s3" {
    bucket         = "url-shortener-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}

module "infrastructure" {
  source = "../../modules"
  
  aws_region = "us-east-1"
  project_name = "url-shortener"
  
  vpc_cidr = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b"]
  private_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnet_cidrs = ["10.0.101.0/24", "10.0.102.0/24"]
  
  redis_node_type = "cache.t3.small"
  app_cpu = 512
  app_memory = 1024
  app_desired_count = 2
  
  ecr_repository_url = "${module.infrastructure.ecr_repository_url}"
  
  tags = {
    Environment = "production"
    Terraform   = "true"
    Project     = "url-shortener"
  }
} 