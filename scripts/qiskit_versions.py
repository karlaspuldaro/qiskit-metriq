import requests
import json
from datetime import datetime

def get_qiskit_versions_info() -> []:
    response = requests.get("https://pypi.org/pypi/qiskit-terra/json")
    data = response.json()
    data_items = data["releases"].items()

    # Temporary control dictionary for package release info
    temp = {}

    # Filter data
    for release, release_info in data_items:
        # Skip RCs
        if "rc" in release:
            continue

        # Filter releases starting from 2020-03
        date_str = release_info[0]["upload_time"]
        date_format = "%Y-%m-%dT%H:%M:%S"
        date_time_obj = datetime.strptime(date_str, date_format)
        year = date_time_obj.year
        month = date_time_obj.month

        if (year == 2020 and month < 3) or year < 2020:
            continue

        python_version = release_info[0]["requires_python"]

        # Parse the release string of format "x.y.z" into a list of "x","y","z"
        dot_char = "."
        major_minor_patch_list = release.split(dot_char)
        major_minor = dot_char.join(major_minor_patch_list[:2])

        # Get latest patch
        patch_number = int(major_minor_patch_list[2])
        temp_info = temp.get(major_minor)
        previous_patch_number = -1 if not temp_info else temp_info[0]

        if previous_patch_number < patch_number:
            # Replace to latest patch version found
            temp[major_minor] = (patch_number, {"version":release, "date": date_str, "python_version": python_version})
            continue

    filtered_releases = []
    for _, value in temp.items():
        filtered_releases.append(value[1])

    return filtered_releases

# Uncomment lines alone to test this file output on its own
versions_info = get_qiskit_versions_info()
print('Qiskit Terra versions:')
print(*versions_info, sep='\n')

"""
Qiskit Terra versions:
{'version': '0.13.0', 'date': '2020-04-09T21:22:39', 'python_version': '>=3.5'}
{'version': '0.14.2', 'date': '2020-06-15T21:02:04', 'python_version': '>=3.5'}
{'version': '0.15.2', 'date': '2020-09-08T18:01:48', 'python_version': '>=3.5'}
{'version': '0.16.4', 'date': '2021-02-08T17:16:48', 'python_version': '>=3.6'}
{'version': '0.17.4', 'date': '2021-05-18T21:24:27', 'python_version': '>=3.6'}
{'version': '0.18.3', 'date': '2021-09-29T11:57:07', 'python_version': '>=3.6'}
{'version': '0.19.2', 'date': '2022-02-02T14:03:42', 'python_version': '>=3.6'}
{'version': '0.20.2', 'date': '2022-05-18T15:29:49', 'python_version': '>=3.7'}
{'version': '0.21.2', 'date': '2022-08-23T21:07:29', 'python_version': '>=3.7'}
{'version': '0.22.4', 'date': '2023-01-17T13:01:47', 'python_version': '>=3.7'}
{'version': '0.23.3', 'date': '2023-03-21T19:16:16', 'python_version': '>=3.7'}
{'version': '0.24.2', 'date': '2023-07-19T18:23:22', 'python_version': '>=3.7'} => TODO: Update v0.24 results using this release
"""
