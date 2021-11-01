terraform {
  required_version = ">=0.12"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
}

provider "azurerm" {
  features {}

  #   Credential sourced from env
  #   Doc: https://docs.microsoft.com/en-us/azure/developer/terraform/get-started-cloud-shell-bash?tabs=bash
  # 
  #   subscription_id   env.ARM_SUBSCRIPTION_ID
  #   tenant_id         env.ARM_TENANT_ID
  #   client_id         env.ARM_CLIENT_ID
  #   client_secret     env.ARM_CLIENT_SECRET
}

resource "azurerm_resource_group" "rg" {
  # create azure resouce group
  name     = "5003-project"
  location = var.resource_group_location
}

resource "azurerm_postgresql_server" "rg" {
  # note: azurerm_postgresql_server.name hase to be globally unique
  name                = "5003-project-db-timescale"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  administrator_login          = "postgres"
  administrator_login_password = var.db_pass

  sku_name   = "B_Gen5_1"
  version    = "11"
  storage_mb = 5120

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = false

  public_network_access_enabled    = true
  ssl_enforcement_enabled          = true
  ssl_minimal_tls_version_enforced = "TLS1_2"
}

resource "azurerm_postgresql_firewall_rule" "allow_all" {
  # note: this setting is INSECURE, only for demo purpose
  name                = "AllowAll"
  resource_group_name = "5003-project"
  server_name         = azurerm_postgresql_server.rg.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}
