import json
from collections import Counter


with open("results.json", encoding="utf-8") as source:
    data = json.load(source)

project = data.get("project", {})
findings = data.get("findings", [])
severities = Counter((item.get("vulnerability", {}).get("severity") or "UNKNOWN").upper() for item in findings)

lines = [
    "# Informe de análisis de vulnerabilidades",
    "",
    f"**Proyecto:** {project.get('name', 'N/D')}",
    f"**Versión:** {project.get('version', 'N/D')}",
    "",
    "## Resumen",
    "",
    f"Se identificaron **{len(findings)} hallazgos** en las dependencias analizadas.",
    "",
    "| Severidad | Cantidad |",
    "|---|---:|",
]

for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"):
    lines.append(f"| {severity} | {severities.get(severity, 0)} |")

lines.extend(["", "## Vulnerabilidades detectadas", ""])
if not findings:
    lines.append("No se encontraron vulnerabilidades en los resultados consultados.")
else:
    lines.extend([
        "| Vulnerabilidad | Componente | Severidad |",
        "|---|---|---|",
    ])
    for item in findings:
        vulnerability = item.get("vulnerability", {})
        component = item.get("component", {})
        identifier = vulnerability.get("vulnId", "N/D")
        component_name = component.get("name", "N/D")
        severity = vulnerability.get("severity", "UNKNOWN")
        lines.append(f"| {identifier} | {component_name} | {severity} |")

lines.extend([
    "",
    "## Recomendaciones",
    "",
    "- Actualizar las dependencias a versiones soportadas y corregidas.",
    "- Revisar cada CVE en la fuente de vulnerabilidades correspondiente.",
    "- No utilizar las versiones vulnerables en entornos productivos.",
    "",
    "## Alcance y limitaciones",
    "",
    "Este análisis evalúa las dependencias declaradas en el SBOM. No sustituye una prueba de penetración ni un análisis del código fuente.",
])

with open("report.md", "w", encoding="utf-8") as output:
    output.write("\n".join(lines) + "\n")
