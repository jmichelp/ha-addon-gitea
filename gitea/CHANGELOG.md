<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 0.3.2

- Try to fix Ingress access

## 0.3.1

- Fix nginx reverse proxy configuration
- Add optiosn to disable account creation

## 0.3.0

- Automatic app.ini template detection, synchronization, and migration on startup
- Add option to choose between OpenSSH server and Gitea embedded SSH server (`ssh_server`)
- Generate unique secrets via `gitea generate secret` and persist key files under `/data` using `SECRET_KEY_URI`, `INTERNAL_TOKEN_URI`, and `JWT_SECRET_URI`
- Set `PASSWORD_HASH_ALGO` to `argon2` and add `password_check_pwn` configuration option
- Ensure WebAuthn passkey authentication works properly with HTTPS and RP ID/Origin binding
- Add email notifications and registration confirmation configuration options (`mailer_*`)
- Add CAPTCHA configuration options (`captcha_*`)
- Ensure `git`, `openssh-server`, and `openssh-sftp-server` are explicitly installed in container
- Configure `REVERSE_PROXY_TRUSTED_PROXIES` and `REVERSE_PROXY_LIMIT` to eliminate URL scheme mismatch warnings
- Fix Ingress mixed content error on login and 2FA form actions
- Optimize external reverse proxy and Ingress with unbuffered low-latency streaming

## 0.2.5

- Fix Ingress mixed content error on login and 2FA form actions by mapping forwarded HTTPS scheme and hostname
- Fix Ingress appSubUrl dynamic binding and proxy redirects
- Optimize external reverse proxy and Ingress with unbuffered low-latency streaming

## 0.2.4

- Dynamically inject ROOT_URL, DOMAIN, and SSH settings directly into app.ini on startup
- Apply environment variables to app.ini before starting Gitea
- Fix Ingress appSubUrl dynamic binding
- Optimize SQLite database with WAL mode and normal synchronous PRAGMAs
- Remove GODEBUG netdns=go to allow standard DNS resolution

## 0.2.3

- Fix duplicate NGINX directives and variable collision with Alpine base
- Enable Gravatar support while keeping Libravatar federated avatar DNS lookups disabled
- Remove redundant default ingress_port in config.yaml to satisfy app linter

## 0.2.2

- Optimize web UI navigation performance for both Ingress and reverse proxy
- Enable in-memory caching and session handling
- Switch SQLite to WAL journal mode for concurrent database access
- Configure NGINX upstream persistent keepalive connection pooling and buffer tuning
- Restrict Ingress sub_filter strictly to HTML to eliminate JS/CSS buffering overhead
- Enable static asset caching and GZIP compression
- Remove dangling static asset symlinks and rely on in-memory bindata

## 0.2.1

- Fix port binding

## 0.2.0

- Make both ingress and nginx reverse proxy work
- Fix nginx reverse proxy warning

## 0.1.5

- Fix static asset path

## 0.1.4

- Fix apparmor profile

## 0.1.3

- Use Alpine package instead of manually install it
- Fix nginx config

## 0.1.2

- Update dependencies, profile, etc.
- Update badges

## 0.0.8

- Try to use Nginx reverse proxy
- Replace configuration file editing with env variables
- Try to start opensshd server as it doesn't seem to listen

## 0.0.7

- Verify downloaded binary with gpg
- Fix installation not working due to path errors

## 0.0.6

- Fix SSL handling
- Add network communication to apparmor profile
- Add more configuration option to adapt the server configuration at startup

## 0.0.5

- Revert chown in startup
- Grant apparmor capabilities to chown/suexec

## 0.0.4

- Remove chown in startup script

## 0.0.3

- Update logo and icon
- Prepare filesystem/permissions in Dockerfile

## 0.0.2

- Fix legacy parts of Dockerfile
- Update base image
- Fix inconsistency in licences
- Apparmor profile tuning

## 0.0.1

- Initial release
