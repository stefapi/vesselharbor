# Physical Host Template

This template provides a way to deploy applications directly on physical hosts or VMs, without using Docker containers.

## Overview

The Physical Host Template is designed for deploying applications directly on physical machines or virtual machines. It uses SSH to connect to the target machine and install the application, configure services, and set up the environment.

## Features

- Supports both physical hosts and VMs
- Configurable installation directories
- Automatic setup of Python virtual environment
- Configuration of Supervisor for process management
- Nginx setup for web serving
- Database setup (PostgreSQL)
- Storage volume configuration
- Network interface configuration

## Requirements

- SSH access to the target machine
- Python 3.x on the target machine
- Sudo privileges on the target machine

## Configuration

The template is configured using a JSON schema defined in `config/schema.json`. The main configuration sections are:

### Host Configuration

```json
"host": {
  "type": "physical",  // or "vm"
  "connection": {
    "host": "example.com",
    "port": 22,
    "user": "admin",
    "key_file": "/path/to/key.pem"  // or use password
  },
  "os": {
    "family": "debian",  // or "redhat", "suse", "arch"
    "version": "11"
  },
  "resources": {
    "cpu_threads": 4,
    "ram_mb": 8192
  }
}
```

### Application Configuration

```json
"app": {
  "debug": false,
  "log_level": "info",
  "secret_key": "your-secret-key",
  "allowed_hosts": ["example.com", "localhost"],
  "install_dir": "/opt/app",
  "data_dir": "/var/lib/app",
  "log_dir": "/var/log/app",
  "user": "app",
  "group": "app"
}
```

### Database Configuration

```json
"database": {
  "host": "localhost",
  "port": 5432,
  "name": "app",
  "user": "postgres",
  "password": "postgres",
  "max_connections": 100
}
```

### Server Configuration

```json
"server": {
  "host_port": 8080,
  "workers": 4,
  "timeout": 60
}
```

### Storage Configuration

```json
"storage": {
  "volumes": [
    {
      "name": "data",
      "path": "/var/lib/app/data",
      "size_gb": 10,
      "type": "local"
    },
    {
      "name": "nfs-data",
      "path": "/mnt/nfs-data",
      "size_gb": 100,
      "type": "nfs",
      "options": {
        "server": "nfs-server.example.com",
        "export": "/exports/data"
      }
    }
  ]
}
```

### Network Configuration

```json
"network": {
  "networks": [
    {
      "name": "app-network",
      "cidr": "192.168.1.0/24",
      "type": "physical",
      "interface": "eth0"
    }
  ]
}
```

## Deployment Process

1. The pre-deployment script checks that the required tools are available.
2. The deployment script connects to the target machine via SSH.
3. It installs the required packages based on the OS family.
4. It creates the application user and group.
5. It creates the required directories.
6. It copies the application files to the target machine.
7. It sets up a Python virtual environment and installs dependencies.
8. It creates the application configuration.
9. It sets up Supervisor to manage the application process.
10. It sets up Nginx as a reverse proxy.
11. It configures the database (if local).
12. It configures storage volumes and network interfaces.
13. It restarts the services.
14. The post-deployment script verifies that the deployment was successful.

## Upgrade Process

1. The pre-upgrade script creates a backup of the current application.
2. The deployment script performs the same steps as for a new deployment.
3. The post-deployment script verifies that the upgrade was successful.

## Differences from Docker Template

This template differs from the Docker template in the following ways:

1. It deploys the application directly on the host, without using containers.
2. It uses SSH to connect to the target machine and execute commands.
3. It sets up Supervisor to manage the application process, instead of using Docker's process management.
4. It configures Nginx directly on the host, instead of using a container.
5. It sets up the database directly on the host, instead of using a container.
6. It configures storage volumes directly on the host, instead of using Docker volumes.
7. It configures network interfaces directly on the host, instead of using Docker networks.

## Example Usage

```json
{
  "host": {
    "type": "physical",
    "connection": {
      "host": "example.com",
      "port": 22,
      "user": "admin",
      "key_file": "/path/to/key.pem"
    },
    "os": {
      "family": "debian",
      "version": "11"
    }
  },
  "app": {
    "debug": false,
    "log_level": "info",
    "secret_key": "your-secret-key",
    "allowed_hosts": ["example.com"],
    "install_dir": "/opt/myapp",
    "user": "myapp",
    "group": "myapp"
  },
  "database": {
    "host": "localhost",
    "name": "myapp",
    "user": "myapp",
    "password": "mypassword"
  },
  "server": {
    "host_port": 8080,
    "workers": 4
  }
}
```
