# HOMESERVER Sudoers Policy Framework

Enterprise-grade sudoers policy framework for the HOMESERVER digital sovereignty platform. Implements the principle of least privilege with granular access control for web-based system administration.

## Overview

The HOMESERVER platform requires sophisticated privilege management to enable web-based system administration while maintaining enterprise-grade security. This framework provides granular, auditable sudo permissions that allow the web interface to perform specific administrative tasks without compromising system security.

## Security Philosophy

- **Principle of Least Privilege**: Each policy grants only the minimum permissions necessary for specific functionality
- **Granular Control**: Separate policies for different functional areas (disk management, system control, etc.)
- **Audit Trail**: All privileged operations are logged through sudo's built-in logging
- **Web User Isolation**: `www-data` user has no shell access, only specific command execution

## Policy Files

### Core System Management
- **`flask-admin`** - Administrative operations including SSH configuration, certificate management, and premium module installation
- **`flask-systemctl`** - Systemd service management (start, stop, restart, status)
- **`flask-config`** - Configuration file access and validation using factoryFallback.sh

### Infrastructure Management
- **`flask-disk`** - Comprehensive disk and storage management including LUKS encryption, filesystem operations, and hardware testing
- **`flask-vault`** - LUKS vault operations and vault script execution
- **`flask-files`** - File system operations (permissions, ownership, ACLs)

### Network & Security
- **`flask-tailscale`** - Tailscale VPN management and configuration updates
- **`flask-vpn`** - VPN key management and transmission configuration
- **`flask-keyman`** - Cryptographic key management and LUKS key operations

### Development & Testing
- **`flask-dev`** - Development environment management, hard drive testing, and thermal validation
- **`flask-updates`** - System update management and module synchronization

### Monitoring & Diagnostics
- **`flask-cat`** - Power consumption monitoring (Intel RAPL)
- **`flask-commands`** - Network diagnostics and service status checks

## Installation

```bash
# Clone as submodule
git submodule add https://github.com/homeserversltd/sudo.git initialization/files/sudo

# Install to system
sudo cp -r initialization/files/sudo/* /etc/sudoers.d/
sudo chmod 440 /etc/sudoers.d/flask-*
sudo chown root:root /etc/sudoers.d/flask-*
```

## Usage

These policies are automatically loaded by the system's sudo configuration. The web interface (`www-data` user) can execute privileged commands without password prompts for the specified operations.

### Example Operations

```bash
# System service management
sudo systemctl restart gunicorn.service

# Disk operations
sudo harddrive_test.sh /dev/sdb full

# Configuration access
sudo factoryFallback.sh

# Tailscale management
sudo tailscale up
```

## Policy Structure

Each policy file follows a consistent pattern:

```bash
# Functional area description
www-data ALL=(root) NOPASSWD: /path/to/command [arguments]
```

- **`www-data`** - Web server user
- **`ALL=(root)`** - Can run as root user
- **`NOPASSWD`** - No password required (for web automation)
- **Command specification** - Exact command and argument patterns

## Security Considerations

- **No Shell Access**: `www-data` cannot spawn interactive shells
- **Command Whitelisting**: Only explicitly specified commands are allowed
- **Argument Validation**: Commands with wildcards are carefully scoped
- **Audit Logging**: All sudo operations are logged to `/var/log/auth.log`
- **Regular Review**: Policies should be reviewed and updated with system changes

## Integration

This framework integrates with the HOMESERVER platform through:

- **Web Interface**: Provides secure access to system administration features
- **API Endpoints**: Backend routes use these policies for privileged operations
- **Configuration Management**: Policies reference platform-specific tools and paths
- **Update System**: Integrated with the platform's module update system

## Maintenance

### Adding New Policies

1. Create new policy file in `/etc/sudoers.d/`
2. Follow naming convention: `flask-{function}`
3. Grant minimal necessary permissions
4. Test thoroughly in development environment
5. Deploy through platform update system

### Updating Existing Policies

1. Modify policy files in source repository
2. Test changes in development environment
3. Deploy through platform update system
4. Monitor logs for any permission issues

## Troubleshooting

### Common Issues

- **Permission Denied**: Check if command is in appropriate policy file
- **Argument Mismatch**: Verify command arguments match policy specification
- **Policy Not Loaded**: Ensure file permissions are 440 and owned by root:root

### Debugging

```bash
# Check sudo policy loading
sudo visudo -c

# View effective sudo permissions
sudo -l -U www-data

# Check sudo logs
sudo tail -f /var/log/auth.log | grep sudo
```

## Contributing

This framework is designed for enterprise environments. Contributions should maintain the security-first approach and follow the established policy patterns.

## License

[Include appropriate license information]

## Support

For HOMESERVER platform support, refer to the main project documentation. These policies are part of the core security infrastructure and are maintained as part of the platform.