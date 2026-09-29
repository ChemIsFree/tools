import os
import re
from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOLS_FILE = ROOT / "data" / "tools.yaml"

ISSUE_BODY = os.environ["ISSUE_BODY"]
ISSUE_NUMBER = os.environ["ISSUE_NUMBER"]


def get_field(label):
    pattern = rf"### {re.escape(label)}\s*\n\s*(.*?)(?=\n### |\Z)"
    match = re.search(pattern, ISSUE_BODY, re.DOTALL)

    if not match:
        return ""

    value = match.group(1).strip()

    if value in {"_No response_", "None"}:
        return ""

    return value


def get_checkbox_values(label):
    value = get_field(label)

    if not value:
        return []

    values = []

    for line in value.splitlines():
        line = line.strip()

        if line.startswith("- [x]"):
            values.append(line[5:].strip())

    return values


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def main():

    name = get_field("Tool or resource name")
    description = get_field("What does it do?")
    category = get_field("Main category")
    website = get_field("Official website")
    repository = get_field("Source repository")
    documentation = get_field("Documentation")
    resource_type = get_field("Resource type")
    access = get_field("Access")
    license_name = get_field("License")
    developers = get_field("Developer or organization")
    citation = get_field("Scientific citation")

    platforms = get_checkbox_values("Platforms")
    interfaces = get_checkbox_values("Interface")

    if not name:
        raise ValueError("Tool name was not found in issue.")

    category_map = {
        "Cheminformatics": "cheminformatics",
        "Molecular Modelling": "molecular-modelling",
        "Drug Discovery": "drug-discovery",
        "Machine Learning": "machine-learning",
        "Data & Databases": "data-and-databases",
        "Visualization": "visualization",
        "Laboratory": "laboratory",
        "Utilities & Workflows": "utilities-and-workflows",
        "Other": "other",
    }

    type_map = {
        "Software": "software",
        "Library": "library",
        "Database": "database",
        "Dataset": "dataset",
        "Web Tool": "web-tool",
        "Web Service": "web-service",
        "Workflow": "workflow",
        "Platform": "platform",
        "Resource": "resource",
        "Tutorial": "tutorial",
        "Other": "resource",
    }

    access_map = {
        "Free": "free",
        "Free tier": "free-tier",
        "Open data": "open-data",
        "Public": "public",
        "Paid": "paid",
        "Unknown": "unknown",
    }

    platform_map = {
        "Linux": "linux",
        "macOS": "macos",
        "Windows": "windows",
        "Web": "web",
        "Android": "android",
        "iOS": "ios",
        "Desktop": "desktop",
        "Cloud": "cloud",
        "Other": "other",
    }

    interface_map = {
        "GUI": "gui",
        "Command line": "cli",
        "Python": "python",
        "R": "r",
        "C++": "c++",
        "Java": "java",
        "API": "api",
        "Web": "web",
        "Notebook": "notebook",
        "Other": "other",
    }

    tool = {
        "id": slugify(name),
        "name": name,
        "description": description,
        "category": [category_map.get(category, "other")],
        "type": type_map.get(resource_type, "resource"),
        "access": [access_map.get(access, "unknown")],
        "source_available": bool(repository),
        "license": license_name or "not-specified",
        "platforms": [
            platform_map[x]
            for x in platforms
            if x in platform_map
        ],
        "interface": [
            interface_map[x]
            for x in interfaces
            if x in interface_map
        ],
        "languages": [],
        "gpu": "unknown",
        "installation": [],
        "status": "active",
        "developers": [developers] if developers else [],
        "website": website or "",
        "repository": repository or "",
        "documentation": documentation or "",
        "citation": [citation] if citation else [],
        "chemisfree_status": "curated-resource",
        "verification": {
            "status": "verified",
            "last_checked": date.today().isoformat(),
        },
        "notes": (
            f"Accepted through ChemIsFree submission "
            f"issue #{ISSUE_NUMBER}."
        ),
    }

    with open(TOOLS_FILE, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    tools = data.setdefault("tools", [])

    existing_ids = {tool.get("id") for tool in tools}

    if tool["id"] in existing_ids:
        raise ValueError(
            f"A tool with id '{tool['id']}' already exists."
        )

    tools.append(tool)

    with open(TOOLS_FILE, "w", encoding="utf-8") as handle:
        yaml.safe_dump(
            data,
            handle,
            sort_keys=False,
            allow_unicode=True,
        )

    print(f"Added {name} to catalogue.")


if __name__ == "__main__":
    main()
