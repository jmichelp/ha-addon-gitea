<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

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
