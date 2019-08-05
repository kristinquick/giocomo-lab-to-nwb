import yaml
import conversion


def yaml_as_python(val):
    """Convert YAML to dict"""
    try:
        return yaml.load_all(val)
    except yaml.YAMLError as exc:
        return exc

with open('config.yaml','r') as input_file:
    results = yaml_as_python(input_file)
    print(results)
    for experiment_info in results:
        gio_tuple = list(experiment_info.values())
        conversion.convert(*gio_tuple)
