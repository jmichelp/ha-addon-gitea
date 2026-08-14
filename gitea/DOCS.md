# Home Assistant Add-on: Gitea

Gitea is a painless self-hosted Git service written in Go. It includes repository hosting, issue tracking, pull requests, user management, and Git LFS support.

## Features

- **Ingress Support:** Access the Gitea web interface directly from your Home Assistant sidebar.
- **Built-in SSH Server:** Isolated and unprivileged Git SSH access on port 3022.
- **SSL/TLS Support:** Optional HTTPS for direct web access or reverse proxy via NGINX.
- **SQLite Database:** Lightweight, zero-configuration local database stored in `/data/gitea/data/gitea.db`.
- **Git LFS Support:** Store large files directly in Gitea.
- **Persistent Data:** All repositories and configurations are preserved across add-on updates in `/data`.

## How to use

1. Install and start the add-on.
2. Click **Open Web UI** or access **Gitea** in the sidebar via Ingress.
3. On first startup, the add-on initializes a production-ready Gitea instance. Register your first user account; this account automatically becomes the administrator.
4. Add your SSH public keys under **User Settings > SSH / GPG Keys**.
5. Create or migrate your Git repositories!

## Access Modes

### 1. Home Assistant Ingress (Recommended for browser access)
Open Gitea directly from your Home Assistant sidebar. Authentication and session handling are managed seamlessly by Home Assistant.

### 2. Direct Web Port Access
Access Gitea directly at `http://<YOUR_HA_IP>:3000/` (or `https://...` if direct `ssl` is enabled). Useful for Git HTTP cloning and direct browser access.

### 3. NGINX Reverse Proxy
If using the **NGINX Home Assistant SSL Proxy** add-on (`use_nginx: true`), set the `domain` option to a dedicated subdomain (e.g. `gitea.yourdomain.com` or `gitea.local`) rather than sharing the exact same domain as Home Assistant Core, so NGINX routes traffic correctly.

## SSH Access

The add-on runs Gitea's internal SSH server on port `2222` inside the container, mapped to port `3022` on your Home Assistant host.

To clone repositories over SSH:

```bash
git clone ssh://git@<YOUR_HA_IP_OR_DOMAIN>:3022/<username>/<repo>.git
```

Or configure your `~/.ssh/config`:

```text
Host gitea-ha
    HostName <YOUR_HA_IP_OR_DOMAIN>
    Port 3022
    User git
```

Then clone using:

```bash
git clone gitea-ha:<username>/<repo>.git
```

## Configuration Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `domain` | string | `homeassistant.local` | FQDN or hostname used to access Gitea. If using NGINX proxy, use a dedicated subdomain (e.g. `gitea.local`). |
| `ssl` | boolean | `false` | Enable SSL/TLS for direct Web UI access. |
| `certfile` | string | `fullchain.pem` | Certificate filename in `/ssl/`. |
| `keyfile` | string | `privkey.pem` | Private key filename in `/ssl/`. |
| `root_url` | string | optional | Custom root URL (e.g. `https://gitea.example.com/`). |
| `use_nginx` | boolean | `false` | Generate reverse proxy configuration for the NGINX SSL Proxy add-on. |
| `ssh_server` | string | `builtin` | SSH server implementation (`builtin` for Gitea's embedded server, or `openssh` for OpenSSH daemon). |
| `password_check_pwn` | boolean | `false` | Check passwords against HaveIBeenPwned API on user registration/password changes. |
| `mailer_enabled` | boolean | `false` | Enable email notification and registration confirmation service. |
| `mailer_protocol` | string | `starttls` | SMTP protocol (`starttls`, `smtps`, `smtp`, `sendmail`, `dummy`). |
| `mailer_smtp_addr` | string | `""` | SMTP server hostname or IP address. |
| `mailer_smtp_port` | integer | `587` | SMTP server port number. |
| `mailer_user` | string | `""` | SMTP authentication username. |
| `mailer_password` | password | `""` | SMTP authentication password. |
| `mailer_from` | string | `""` | Sender email address (e.g. `gitea@example.com`). |
| `register_email_confirm` | boolean | `false` | Require email confirmation before new users can log in. |
| `captcha_enabled` | boolean | `false` | Enable CAPTCHA validation on registration. |
| `captcha_type` | string | `image` | CAPTCHA engine (`image`, `recaptcha`, `hcaptcha`, `mcaptcha`, `cfturnstile`). |

## Backups

Gitea data (database, repositories, SSH keys, configuration) is stored under `/data` and is included in standard Home Assistant backups.
