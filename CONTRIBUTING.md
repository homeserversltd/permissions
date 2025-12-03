# Contributing to HOMESERVER Sudoers Policy Framework

Thank you for your interest in contributing to the HOMESERVER sudoers policy framework. This is a **security-critical component** of the HOMESERVER platform, and we appreciate your careful attention to security best practices.

## About This Repository

This repository contains sudoers policies that enable the HOMESERVER web interface to perform privileged system administration tasks. These policies implement the principle of least privilege, granting only the minimum permissions necessary for specific functionality.

**Security Impact**: Changes to this repository directly affect system security. Improperly configured sudoers policies can:
- Create privilege escalation vulnerabilities
- Allow unauthorized system access
- Compromise the entire HOMESERVER platform

We take security seriously and review all contributions carefully.

## Ways to Contribute

### High-Value Contributions

- **Bug fixes**: Address security issues or misconfigurations
- **Security improvements**: Tighten permissions, add validation, reduce attack surface
- **New policies**: Support new HOMESERVER features with minimal necessary privileges
- **Documentation**: Clarify policy purposes and security implications
- **Testing**: Validate that policies work as intended without security gaps

### Security Vulnerability Reporting

**DO NOT** open public issues for security vulnerabilities.

If you discover a security issue:
1. **Email privately**: security@arpaservers.com or owner@arpaservers.com
2. **Include details**: Description, reproduction steps, potential impact
3. **Suggest fixes**: If you have a solution, include it
4. **Wait for response**: We'll acknowledge within 48 hours

We'll work with you to understand and fix the issue before public disclosure.

## Getting Started

### Prerequisites

- Understanding of Linux sudoers configuration
- Familiarity with privilege escalation risks
- Knowledge of HOMESERVER architecture (helpful but not required)
- Experience with security-critical system administration

### Repository Setup

1. **Fork the repository** on GitHub:
   ```bash
   git clone git@github.com:YOUR_USERNAME/permissions.git
   cd permissions
   ```

2. **Add upstream remote**:
   ```bash
   git remote add upstream git@github.com:homeserversltd/permissions.git
   ```

3. **Review existing policies**: Understand the patterns and conventions

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b security/your-improvement
# or
git checkout -b fix/issue-description
```

### 2. Make Your Changes

- **Minimal permissions**: Grant only what's absolutely necessary
- **Specific commands**: Avoid wildcards unless unavoidable
- **No shell access**: Never allow shell spawning or interactive sessions
- **Validated paths**: Use absolute paths, validate arguments
- **Document reasoning**: Explain why each permission is needed

### 3. Test Thoroughly

Security testing is mandatory. See [Testing Requirements](#testing-requirements) below.

### 4. Commit and Push

```bash
git add .
git commit -m "Descriptive security-focused message"
git push origin security/your-improvement
```

### 5. Open a Pull Request

Include detailed security analysis in your PR description.

## Code Quality Standards

### Sudoers Policy Best Practices

**Command Specification:**
```bash
# GOOD: Specific command with constrained arguments
www-data ALL=(root) NOPASSWD: /usr/bin/systemctl restart gunicorn.service

# BAD: Allows any systemctl command
www-data ALL=(root) NOPASSWD: /usr/bin/systemctl *

# ACCEPTABLE: Limited wildcards when necessary
www-data ALL=(root) NOPASSWD: /usr/local/sbin/harddrive_test.sh /dev/sd? *
```

**File Organization:**
- One policy file per functional area
- Clear naming: `flask-{function}`
- Comments explaining purpose and security rationale
- Permissions: 440, owned by root:root

**Security Principles:**
- Least privilege: Minimum permissions needed
- No NOPASSWD unless absolutely necessary (required for web automation)
- No SETENV unless specifically needed and safe
- Validate or constrain all arguments
- Absolute paths only
- No shell escapes or command chaining

### Documentation Standards

Every policy file should include:
```bash
# flask-example - Purpose of this policy file
#
# Security Considerations:
# - Explain why these permissions are needed
# - Note any potential risks
# - Describe validation or constraints applied
#
# Commands granted:
# - Specific list of what www-data can do
```

## Testing Requirements

**All security changes must be tested extensively.**

### Required Testing

1. **Functional testing**: Verify the policy allows intended operations
2. **Negative testing**: Verify the policy blocks unintended operations
3. **Privilege escalation testing**: Attempt to abuse the policy
4. **Integration testing**: Test with actual HOMESERVER web interface

### Testing Documentation

In your PR, include:

```markdown
## Security Testing Performed

### Functional Tests
- Tested command X with valid arguments: SUCCESS
- Verified integration with web interface: SUCCESS

### Security Tests  
- Attempted to execute arbitrary commands: BLOCKED
- Tested path traversal with ../../: BLOCKED
- Tried command injection with semicolons: BLOCKED
- Attempted shell escape: BLOCKED

### Test Environment
- OS: Debian 12
- Sudo version: 1.9.x
- HOMESERVER version: X.X.X

### Test Methodology
[Describe how you tested each scenario]
```

## Commit Message Guidelines

Security-focused commit messages should be detailed:

```
Add disk management sudoers policy for NAS setup

Implemented minimal sudoers permissions for disk management:
- Mount/unmount operations for specific devices
- Filesystem operations (mkfs, fsck) with device validation
- LUKS encryption operations for vault management
- No shell access or arbitrary command execution

Security considerations:
- Commands limited to /dev/sd* devices only
- No wildcard paths that could affect system directories
- All operations require explicit device arguments
- Tested against command injection and path traversal

Created policy file: flask-disk
```

## Pull Request Process

### PR Description Template

```markdown
## Summary
Brief description of the changes.

## Security Impact
What security implications does this change have?

## Permissions Added/Modified
- Specific command 1
- Specific command 2

## Why These Permissions Are Needed
Explanation of the functionality requirements.

## Security Analysis
How did you ensure these permissions are safe?

## Testing Performed
[Use the testing template above]

## Checklist
- [ ] Minimal necessary permissions granted
- [ ] No shell access or command injection vectors
- [ ] Absolute paths used
- [ ] Tested functionality works
- [ ] Tested security cannot be bypassed
- [ ] Documentation updated
- [ ] Security rationale documented
```

### Review Process

1. **Security review**: Maintainer performs security analysis
2. **Functional testing**: Verify the policy enables intended features
3. **Privilege escalation testing**: Attempt to abuse the policy
4. **Discussion**: Address any security concerns
5. **Approval**: Merge only after thorough security review

Security-critical changes may require additional review time.

## Architecture Understanding

### HOMESERVER Web Architecture

The HOMESERVER platform uses Flask running as `www-data` user. Privileged operations are performed through sudo with these policies.

**Key Constraints:**
- Web server runs as `www-data` (no login shell)
- Operations must be non-interactive (NOPASSWD required)
- Security depends entirely on sudoers configuration
- Vulnerabilities here can compromise the entire system

### Policy Organization

```
flask-admin       # Administrative operations
flask-systemctl   # Service management
flask-config      # Configuration access
flask-disk        # Disk operations
flask-vault       # Vault management
flask-tailscale   # VPN management
flask-keyman      # Credential management
# ... etc
```

Each policy file grants permissions for a specific functional area.

## Security Guidelines

### What to Avoid

- **Wildcards in paths**: `/*` can match anything
- **Command chaining**: `;`, `&&`, `||` in allowed commands
- **Shell invocation**: No `bash`, `sh`, or shell escapes
- **Environment variables**: SETENV can be dangerous
- **Relative paths**: Always use absolute paths
- **Overly broad patterns**: Be as specific as possible

### Safe Patterns

```bash
# Safe: Specific command, specific service
www-data ALL=(root) NOPASSWD: /usr/bin/systemctl restart gunicorn.service

# Safe: Constrained wildcard for device names
www-data ALL=(root) NOPASSWD: /sbin/cryptsetup luksOpen /dev/sd?? *

# Safe: Script with validated arguments
www-data ALL=(root) NOPASSWD: /usr/local/sbin/setupNAS.sh
```

## Getting Help

### Questions?

- **Open an issue**: For general questions about contributing
- **Email**: For security-related questions (owner@arpaservers.com)
- **Review existing policies**: Study patterns in the repository

### Resources

- [Sudoers manual](https://www.sudo.ws/docs/man/sudoers.man/)
- HOMESERVER architecture documentation
- Existing policy files in this repository

## Recognition

Contributors who improve HOMESERVER security:
- Are credited in the repository
- Help protect thousands of HOMESERVER users
- Build professional portfolio demonstrating security expertise

## License

This project is licensed under **GPL-3.0**. Contributions are accepted under this license, and no CLA is required.

---

**Thank you for helping keep HOMESERVER secure!**

Security is foundational to digital sovereignty. Your careful work protects user privacy and system integrity.

*HOMESERVER LLC - Professional Digital Sovereignty Solutions*

