terraform {
  required_version = ">=0.12"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
    grafana = {
      source  = "grafana/grafana"
      version = "1.14.0"
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

provider "grafana" {
  url  = "https://dennislau.grafana.net"
  auth = var.grafana_auth
}

resource "azurerm_resource_group" "rg" {
  # create azure resouce group
  name     = "5003-project"
  location = var.resource_group_location

  tags = {
    environment = "development"
  }
}

resource "azurerm_network_security_group" "rg" {
  name                = "default_security_group"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    # note: this setting is INSECURE, only for demo purpose
    name                       = "allow_all"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_virtual_network" "rg" {
  name                = "default_vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "rg" {
  name                 = "default_subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.rg.name
  address_prefixes     = ["10.0.0.0/24"]
  service_endpoints    = ["Microsoft.Sql"]
}

resource "azurerm_subnet_network_security_group_association" "rg" {
  subnet_id                 = azurerm_subnet.rg.id
  network_security_group_id = azurerm_network_security_group.rg.id
}

# postgres

resource "azurerm_postgresql_virtual_network_rule" "rg" {
  # assign postgres to subnet
  name                                 = "postgresql-vnet-rule"
  resource_group_name                  = azurerm_resource_group.rg.name
  server_name                          = azurerm_postgresql_server.rg.name
  subnet_id                            = azurerm_subnet.rg.id
  ignore_missing_vnet_service_endpoint = true
}

resource "azurerm_postgresql_server" "rg" {
  # postgres instance
  # note: azurerm_postgresql_server.name hase to be globally unique
  name                = "5003-project-db-timescale"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  administrator_login          = "postgres"
  administrator_login_password = var.db_pass

  sku_name   = "GP_Gen5_2"
  version    = "11"
  storage_mb = 5120

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = false

  public_network_access_enabled    = true
  ssl_enforcement_enabled          = true
  ssl_minimal_tls_version_enforced = "TLS1_2"
}

resource "azurerm_postgresql_configuration" "timescaledb" {
  name                = "shared_preload_libraries"
  resource_group_name = azurerm_postgresql_server.rg.resource_group_name
  server_name         = azurerm_postgresql_server.rg.name
  value               = "timescaledb"

  provisioner "local-exec" {
    # restart to take effect
    command = "az postgres server restart -g ${azurerm_postgresql_server.rg.resource_group_name} -n ${azurerm_postgresql_server.rg.name}"
  }
}

resource "azurerm_postgresql_firewall_rule" "allow_all" {
  # note: this setting is INSECURE, only for demo purpose
  name                = "AllowAll"
  resource_group_name = "5003-project"
  server_name         = azurerm_postgresql_server.rg.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}
