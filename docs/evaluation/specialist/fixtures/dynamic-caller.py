formatter = getattr(formatters, runtime_config['formatter'])
result = formatter(user_input)
