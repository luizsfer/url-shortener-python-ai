variable "aws_region" {
  description = "Região AWS onde os recursos serão criados"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto, usado como prefixo para os recursos"
  type        = string
  default     = "url-shortener"
}

variable "vpc_cidr" {
  description = "CIDR block para a VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Lista de zonas de disponibilidade"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "private_subnet_cidrs" {
  description = "Lista de CIDR blocks para as subnets privadas"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnet_cidrs" {
  description = "Lista de CIDR blocks para as subnets públicas"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "redis_node_type" {
  description = "Tipo de instância para o Redis"
  type        = string
  default     = "cache.t3.micro"
}

variable "app_cpu" {
  description = "CPU units para a aplicação (1024 = 1 vCPU)"
  type        = number
  default     = 256
}

variable "app_memory" {
  description = "Memória para a aplicação em MB"
  type        = number
  default     = 512
}

variable "app_desired_count" {
  description = "Número desejado de instâncias da aplicação"
  type        = number
  default     = 2
}

variable "ecr_repository_url" {
  description = "URL do repositório ECR"
  type        = string
}

variable "tags" {
  description = "Tags para todos os recursos"
  type        = map(string)
  default = {
    Environment = "production"
    Terraform   = "true"
  }
} 