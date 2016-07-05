import uuid
import hashlib
import sys
import json
from kinto_http import cli_utils


DEFAULT_SERVER = "https://kinto-ota.dev.mozaws.net/v1/"


def _print(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def push(client):
    with open('config.json') as f:
        SCHEMA_V1 = json.load(f)['collections']

    with open('experiments.json') as f:
        experiments = json.loads(f.read())

    count = 0
    client.create_collection('experiments',
                             data=SCHEMA_V1['experiments']['config'],
                             permissions={"read": ["system.Everyone"]},
                             safe=False)

    kinto_experiments = {}
    for record in list(client.get_records()):
        kinto_experiments[record['name']] = record

    with client.batch() as b:
        for key, experiment in experiments.items():
            _print('.')
            experiment['name'] = key

            if key in kinto_experiments:
                # update
                experiment['id'] = kinto_experiments[key]['id']
            else:
                # creation
                hashed_key = hashlib.md5(key.encode('utf8')).hexdigest()
                experiment['id'] = str(uuid.UUID(hashed_key))

            b.update_record(experiment)
            count += 1

    _print('\nChanged %d records\n' % count)


def main():
    parser = cli_utils.add_parser_options(
        description='Upgrade the attachment structure',
        default_server=DEFAULT_SERVER,
        default_bucket='fennec',
        default_collection='experiments')

    args = parser.parse_args()
    client = cli_utils.create_client_from_args(args)
    push(client)


if __name__ == '__main__':
    main()
