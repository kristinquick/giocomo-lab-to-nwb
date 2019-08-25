import yaml
import conversion


def yaml_as_python(val):
    """Convert YAML to dict"""
    try:
        return yaml.safe_load_all(val)
    except yaml.YAMLError as exc:
        return exc

with open('config.yaml','r') as input_file:
    results = yaml_as_python(input_file)
    for experiment_info in results:
        print('converting', experiment_info['input_file'])
        conversion.convert(**experiment_info)
