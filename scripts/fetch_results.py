import json
import os
import sys
import urllib.parse
import urllib.request


def get_json(url, api_key):
    request = urllib.request.Request(url, headers={"X-Api-Key": api_key})
    with urllib.request.urlopen(request) as response:
        return json.load(response)


base_url = os.environ["DT_URL"].rstrip("/")
api_key = os.environ["DT_API_KEY"]
project_name = os.environ["DT_PROJECT_NAME"]

projects_url = f"{base_url}/api/v1/project?{urllib.parse.urlencode({'name': project_name})}"
projects = get_json(projects_url, api_key)
if not projects:
    print(f"No se encontró el proyecto: {project_name}", file=sys.stderr)
    sys.exit(1)

project = projects[0]
project_uuid = project["uuid"]
findings_url = f"{base_url}/api/v1/finding/project/{project_uuid}"
findings = get_json(findings_url, api_key)

result = {
    "project": project,
    "findings": findings,
}
with open("results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, indent=2, ensure_ascii=False)

print(f"Resultados guardados para {project_name}: {len(findings)} hallazgos")
