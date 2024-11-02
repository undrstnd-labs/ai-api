from config.site import label

def clean_label(data):
    if isinstance(data, dict):
        return {k if not k.startswith('x_') else f'x_{label}': clean_label(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_label(i) for i in data]
    else:
        return data
