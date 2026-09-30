import os
import re
from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOLS_FILE = ROOT / "data" / "tools.yaml"

ISSUE_BODY = os.environ["ISSUE_BODY"]
ISSUE_NUMBER = os.environ["ISSUE_NUMBER"]


# ---------------------------------------------------------
# Field parsing
# ---------------------------------------------------------

def get_field(label):
    pattern = rf"### {re.escape(label)}\s*\n\s*(.*?)(?=\n### |\Z)"

    match = re.search(
        pattern,
        ISSUE_BODY,
        re.DOTALL,
    )

    if not match:
        return ""

    value = match.group(1).strip()

    if value in {
        "_No response_",
        "None",
    }:
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

            values.append(
                line[5:].strip()
            )

    return values


# ---------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------

def slugify(value):

    value = value.lower().strip()

    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value,
    )

    return value.strip("-")


def split_languages(value):

    if not value:
        return []

    parts = re.split(
        r"[,;\n]+",
        value,
    )

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


# ---------------------------------------------------------
# Taxonomy mappings
# ---------------------------------------------------------

DOMAIN_MAP = {

    "Chemical Structures":
        "chemical-structures",

    "Ligand-Based Discovery":
        "ligand-based-discovery",

    "Structure-Based Discovery":
        "structure-based-discovery",

    "Molecular Properties & ADMET":
        "molecular-properties-admet",

    "Synthesis & Reaction Design":
        "synthesis-reaction-design",

    "Data & Chemical Analysis":
        "data-analysis",

    "Visualization & Interpretation":
        "visualization",

    "Laboratory & Workflows":
        "laboratory-workflows",
}


TASK_MAP = {

    "Inventory Management":
        "inventory-management",

    "Draw & Edit Structures":
        "structure-drawing",

    "Structure Elucidation":
        "structure-elucidation",

    "Molecular Descriptors & Properties":
        "molecular-descriptors-properties",

    "Structure Search":
        "structure-search",

    "Structure Conversion":
        "structure-conversion",

    "Ligand Preparation":
        "ligand-preparation",

    "Chemical Space Analysis":
        "chemical-space",

    "Pharmacophore Modelling":
        "pharmacophore-modelling",

    "QSAR & Predictive Modelling":
        "qsar",

    "Scaffold Analysis":
        "scaffold-analysis",

    "Ligand-Based Virtual Screening":
        "ligand-based-screening",

    "Protein Preparation":
        "protein-preparation",

    "Binding-Site Analysis":
        "binding-site-analysis",

    "Molecular Docking":
        "molecular-docking",

    "Structure-Based Virtual Screening":
        "structure-based-screening",

    "Molecular Dynamics":
        "molecular-dynamics",

    "Interaction Analysis":
        "interaction-analysis",

    "Free-Energy Calculations":
        "free-energy",

    "Physicochemical Properties":
        "physicochemical-properties",

    "ADME Prediction":
        "adme",

    "Toxicity Prediction":
        "toxicity",

    "Drug-Likeness":
        "drug-likeness",

    "Retrosynthesis":
        "retrosynthesis",

    "Reaction Prediction":
        "reaction-prediction",

    "Synthetic Route Planning":
        "route-planning",

    "Reaction Analysis":
        "reaction-analysis",

    "Bioactivity Analysis":
        "bioactivity-analysis",

    "Data Curation":
        "data-curation",

    "Chemical Data Analysis":
        "chemical-data-analysis",

    "Machine Learning":
        "machine-learning",

    "Generative Chemistry":
        "generative-chemistry",

    "Molecular Visualization":
        "molecular-visualization",

    "3D Structure Analysis":
        "three-dimensional-analysis",

    "Trajectory Analysis":
        "trajectory-analysis",

    "Scientific Visualization":
        "scientific-visualization",


    "Laboratory Automation":
        "laboratory-automation",

    "Workflow Construction":
        "workflow-construction",

    "Pipeline Execution":
        "pipeline-execution",
}


INTERFACE_MAP = {

    "GUI":
        "gui",

    "Web":
        "web",

    "Command line":
        "cli",
}


PLATFORM_MAP = {

    "Linux":
        "linux",

    "macOS":
        "macos",

    "Windows":
        "windows",

    "Web":
        "web",

    "Android":
        "android",

    "iOS":
        "ios",

    "Desktop":
        "desktop",

    "Cloud":
        "cloud",

    "Other":
        "other",
}


ACCESS_MAP = {

    "Free":
        ["free"],

    "Open Source":
        ["free", "open-source"],

    "Unknown / needs verification":
        ["unknown"],
}


RESOURCE_TYPE_MAP = {

    "Library":
        "library",

    "Database":
        "database",

    "Dataset":
        "dataset",

    "Educational":
        "educational",
}


# ---------------------------------------------------------
# Main processing
# ---------------------------------------------------------

def main():

    name = get_field(
        "Tool or resource name"
    )

    description = get_field(
        "What does it do?"
    )

    catalogue = get_field(
        "Catalogue section"
    )

    domain = get_field(
        "Main area"
    )

    primary_task = get_field(
        "Primary task"
    )

    additional_tasks = get_checkbox_values(
        "Additional tasks"
    )

    website = get_field(
        "Official website"
    )

    repository = get_field(
        "Source repository"
    )

    documentation = get_field(
        "Documentation"
    )

    resource_type = get_field(
        "Resource type"
    )

    access = get_field(
        "Access"
    )

    license_name = get_field(
        "License"
    )

    interfaces = get_checkbox_values(
        "User interface"
    )

    platforms = get_checkbox_values(
        "Platforms"
    )

    languages = split_languages(
        get_field("Languages / technologies")
    )

    developers = get_field(
        "Developer or organization"
    )

    citation = get_field(
        "Scientific citation"
    )

    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    if not name:
        raise ValueError(
            "Tool name was not found in issue."
        )

    if not description:
        raise ValueError(
            "Description was not found in issue."
        )

    if catalogue not in {
        "Application",
        "Supporting Resource",
    }:
        raise ValueError(
            f"Invalid catalogue section: {catalogue}"
        )

    if domain not in DOMAIN_MAP:
        raise ValueError(
            f"Invalid main area: {domain}"
        )

    if primary_task not in TASK_MAP:
        raise ValueError(
            f"Invalid primary task: {primary_task}"
        )

    # -----------------------------------------------------
    # Domains
    # -----------------------------------------------------

    domain_ids = [
        DOMAIN_MAP[domain]
    ]

    # -----------------------------------------------------
    # Tasks
    # -----------------------------------------------------

    task_labels = [
        primary_task,
        *additional_tasks,
    ]

    task_ids = []

    for label in task_labels:

        task_id = TASK_MAP.get(label)

        if not task_id:
            continue

        if task_id not in task_ids:
            task_ids.append(task_id)

    if not task_ids:
        raise ValueError(
            "No valid tasks were provided."
        )

    # -----------------------------------------------------
    # Catalogue / resource classification
    # -----------------------------------------------------

    tool = {
        "id": slugify(name),
        "name": name,
        "description": description,

        "catalogue":
            "app"
            if catalogue == "Application"
            else "resource",

        "domain":
            domain_ids,

        "tasks":
            task_ids,

        "category":
            [],

        "type":
            "software"
            if catalogue == "Application"
            else "resource",

        "access":
            ACCESS_MAP.get(
                access,
                ["unknown"],
            ),

        "source_available":
            (
                access == "Open Source"
            ),

        "license":
            license_name
            or "not-specified",

        "platforms": [
            PLATFORM_MAP[item]
            for item in platforms
            if item in PLATFORM_MAP
        ],

        "interface": [
            INTERFACE_MAP[item]
            for item in interfaces
            if item in INTERFACE_MAP
        ],

        "languages":
            languages,

        "gpu":
            "unknown",

        "installation":
            [],

        "status":
            "active",

        "developers":
            [developers]
            if developers
            else [],

        "website":
            website
            or "",

        "repository":
            repository
            or "",

        "documentation":
            documentation
            or "",

        "citation":
            [citation]
            if citation
            else [],

        "chemisfree_status":
            "curated-resource",

        "verification": {
            "status": "verified",
            "last_checked": date.today().isoformat(),
        },

        "notes":
            (
                "Accepted through ChemIsFree submission "
                f"issue #{ISSUE_NUMBER}."
            ),
    }

    # -----------------------------------------------------
    # Resource type
    # -----------------------------------------------------

    if (
        catalogue == "Supporting Resource"
        and resource_type in RESOURCE_TYPE_MAP
    ):

        tool["resource_type"] = (
            RESOURCE_TYPE_MAP[
                resource_type
            ]
        )

        # Set the actual resource type for the
        # catalogue entry rather than generic "resource".
        tool["type"] = tool["resource_type"]

    # -----------------------------------------------------
    # Read existing catalogue
    # -----------------------------------------------------

    with open(
        TOOLS_FILE,
        "r",
        encoding="utf-8",
    ) as handle:

        data = yaml.safe_load(handle)

    if not isinstance(data, dict):
        raise ValueError(
            "tools.yaml does not contain a valid mapping."
        )

    tools = data.setdefault(
        "tools",
        []
    )

    existing_ids = {
        tool.get("id")
        for tool in tools
    }

    if tool["id"] in existing_ids:
        raise ValueError(
            f"A tool with id '{tool['id']}' already exists."
        )

    # -----------------------------------------------------
    # Add tool
    # -----------------------------------------------------

    tools.append(tool)

    with open(
        TOOLS_FILE,
        "w",
        encoding="utf-8",
    ) as handle:

        yaml.safe_dump(
            data,
            handle,
            sort_keys=False,
            allow_unicode=True,
        )

    print(
        f"Added {name} to catalogue."
    )


if __name__ == "__main__":
    main()
