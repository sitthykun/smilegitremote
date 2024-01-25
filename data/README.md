Just use standard file instead using any database application

# JSON
- auth.json
- project.json
- role.json

# auth.json
- no require:
  - username
  - password
  - role
- require:
  - none

# project.json
- no require:
	- datetime_format as string format
    - env as string
    - git_remote_url as string
    - git_token as string
    - git_username as string
    - name as string
    - note as string
    - trigger as dictionary (will execute the command that set in the list of before and after properties)
    - white_ip as list
- require:
  - git_dir
  - git_remote_origin
  - git_remote_url

# role.json
- no require:
  - role
  - enable
- require:
  - none
