from envyaml import EnvYAML

# read file env.yaml and parse config
env = EnvYAML('./build_templates/credentials_template.yml')

print(env['twilio'])