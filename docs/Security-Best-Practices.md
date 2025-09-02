# Security Best Practices

## Introduction
This document outlines best practices for securing your deployments, with a focus on the new `API_KEY` feature introduced in version 3.11. These guidelines help protect sensitive data and ensure robust authentication across environments. This document was last updated at 10:24 AM CEST on Tuesday, September 02, 2025.

## General Security Guidelines
- **Use Secure Credentials**: Avoid hardcoding usernames, passwords, or API keys in scripts or configuration files. Instead, leverage your CI/CD environment's secret store.
- **Regular Rotation**: Rotate credentials and API keys periodically (e.g., every 90 days) to minimize exposure risks.
- **Access Control**: Apply the principle of least privilege, granting only necessary permissions to users and services.
- **Monitoring**: Regularly audit logs and monitor for unusual activity to detect potential security breaches.

## New API_KEY Feature in Version 3.11
As of version 3.11, the `API_KEY` feature provides an alternative authentication method alongside traditional `USER` and `PASSWORD` credentials. This enhancement allows for more flexible and secure access to services, particularly in automated workflows.

### Key Benefits
- **Simplified Authentication**: Use a single `API_KEY` for authentication instead of managing separate username-password pairs.
- **Enhanced Security**: API keys can be scoped to specific actions or resources, reducing the risk if compromised.
- **Environment Integration**: Seamlessly integrate with CI/CD secret stores for secure management.

### Implementation
- **Storage**: Store the `API_KEY` as a secret in your CI/CD platform (e.g., GitHub Secrets, Azure DevOps Variables).
- **Usage**: Pass the `API_KEY` via environment variables in your deployment scripts. Example:
  ```yaml
  env:
    API_KEY: $(API_KEY)  # Retrieve from secret store
  ```
- **Either/Or Approach**: Use either `USER` and `PASSWORD` or `API_KEY`, not all together, depending on your authentication needs.

### Creating an API Key
As a portal admin, you can create an API Key with specific privileges to allow GaiaBuilder to authenticate and perform deployments without needing to store user credentials.
1. Go to "Content" — "New item" — "Developer credentials" — "Select API key credentials and Next".
2. Set Expiration date (up to one year).
3. Set Referrer URLs (this needs to match the `referer` in the `gaiaBuilder.ini` on the server) and click "Next".
4. Set Privileges (see details below) and click "Next".
5. Create API key now and copy the API key to the secret store of your environment, for example, Library in Azure DevOps.

### Best Practices for API_KEY
- **Generate Secure Keys**: Ensure API keys are cryptographically strong, with a minimum length of 32 characters.
- **Restrict Scope**: Limit the API key's permissions to the minimum required for its intended use.
- **Revoke and Regenerate**: Immediately revoke an API key if you suspect exposure and regenerate a new one.
- **Avoid Exposure**: Never commit API keys to version control; use environment variables or secret management tools (e.g., HashiCorp Vault).

## Minimum Privileges for GaiaBuilder (Version 3.11)
GaiaBuilder requires a minimal set of privileges to function effectively. As of version 3.11, features like creating groups are not supported. Below is a transformed representation of the necessary privileges, optimized for least privilege access, using a nested structure.

### General Privileges
- [ ] View
  - Allow application to view members of the organization.

### Content Privileges
- [x] Create, update, and delete
  - Allow application to create, edit, and delete the application owner's content.
- [x] Publish hosted feature layers
  - Allow application to publish hosted feature layers from shapefiles, CSVs, etc.
- [x] Publish server-based layers
  - This privilege grants the ability to publish layers powered by services from federated server sites. These services often reference registered data from geodatabases or file-based data sources.
- [x] Register data stores
  - This privilege grants the ability to register data stores to the portal.
- [x] Reassign ownership
  - Allow application to reassign content to other members within your organization.
- [x] Publish web tools
  - This privilege grants the ability to publish web tools backed by geoprocessing services from federated server sites.

### Sharing Privileges
- [x] Share with portal
  - Allow application to share content to your organization.

### Notes
- Privileges not listed (e.g., creating groups, editing features, managing versions) are not required for GaiaBuilder's core functionality in version 3.11. This has not been verified at the time of writing and may require further testing.
- Ensure all selected privileges are enabled during API key creation to support deployment tasks.

## Example Deployment Script
Below is an example PowerShell script snippet using the `API_KEY`:
```powershell
$args = @(
  "-f", $env:manual_build_list,
  "-s", $env:server,
  "-a", "true"
  # API_KEY is passed via environment variable, no specific flag needed
)
python $scriptPath $args
```

## Additional Considerations
- **Audit Trails**: Enable logging to track API key usage and detect anomalies.
- **Documentation**: Update your team’s documentation to reflect the use of `API_KEY` in workflows.
- **Testing**: Validate API key functionality in a development environment before production deployment.

For more details on securing other aspects of your deployment, refer to the [Environments](Environments.md) guide.