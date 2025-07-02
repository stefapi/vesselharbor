# Template Plugin

A sample plugin to demonstrate how to create and configure plugins for the platform.

## Description

This plugin provides a template structure that can be used as a starting point for developing new plugins. It includes examples of configuration, Docker Compose templates, build materials, and hooks.

## Configuration

### Basic Configuration

```yaml
# Example configuration
database:
  host: localhost
  port: 5432
  name: myapp
  user: dbuser
  password: dbpassword

app:
  debug: false
  log_level: info
  secret_key: your-secret-key-here

server:
  host_port: 8080
```

### Advanced Options

```yaml
# Advanced configuration
email:
  smtp_server: smtp.example.com
  smtp_port: 587
  use_tls: true
  sender: noreply@example.com

features:
  enable_registration: true
  enable_social_login: false
  maintenance_mode: false
```

## Environment Variables

The following environment variables can be used to override configuration:

- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `SECRET_KEY`: Application secret key
- `DEBUG`: Enable debug mode (true/false)
- `LOG_LEVEL`: Logging level (debug, info, warning, error, critical)
- `HOST_PORT`: Host port to bind

## Deployment Examples

### Basic Deployment

```bash
# Deploy with default configuration
platform plugin deploy template

# Deploy with custom configuration
platform plugin deploy template --config my-config.yaml
```

### Production Deployment

```bash
# Deploy for production
platform plugin deploy template --env production --replicas 3
```

### Development Setup

```bash
# Deploy for development with debugging
platform plugin deploy template --env development --debug
```

## Customization

The plugin can be customized by:

1. Modifying the configuration in `config/defaults.yaml`
2. Creating environment-specific overrides
3. Adding custom build materials in the `build/` directory
4. Implementing custom hooks in the `hooks/` directory

## License

This plugin is provided as an example and can be freely used as a template for your own plugins.
