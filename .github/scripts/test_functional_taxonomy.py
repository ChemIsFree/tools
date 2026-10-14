#!/usr/bin/env python3
"""Validate the functional category taxonomy across data and submissions."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CATEGORIES = {
    "target-identification": "Target Identification",
    "protein-structures": "Protein Structures",
    "visualization": "Visualization",
    "binding-pockets": "Binding Pockets",
    "structure-based": "Structure-Based",
    "molecular-dynamics": "Molecular Dynamics",
    "cheminformatics": "Cheminformatics",
    "de-novo-design": "De Novo Design",
    "ligand-based-qsar": "Ligand-Based and QSAR",
    "admet-prediction": "ADMET Prediction",
    "retrosynthesis": "Retrosynthesis",
    "nomenclature-format-conversion": "Nomenclature and Format Conversion",
    "libraries-datasets": "Libraries and Datasets",
    "organization": "Organization",
}

taxonomy = yaml.safe_load((ROOT / "data" / "taxonomy.yaml").read_text(encoding="utf-8"))
tools_data = yaml.safe_load((ROOT / "data" / "tools.yaml").read_text(encoding="utf-8"))
form = yaml.safe_load((ROOT / ".github" / "ISSUE_TEMPLATE" / "suggest-a-tool.yml").read_text(encoding="utf-8"))
processor = (ROOT / ".github" / "scripts" / "process_accepted_tool.py").read_text(encoding="utf-8")

domain_taxonomy = taxonomy.get("domains", {})
assert set(domain_taxonomy) == set(CATEGORIES), (
    "Taxonomy category IDs differ from the required 14-category set: "
    f"{sorted(set(domain_taxonomy) ^ set(CATEGORIES))}"
)
for category_id, expected_name in CATEGORIES.items():
    assert domain_taxonomy[category_id].get("name") == expected_name, (
        f"Unexpected display name for {category_id}"
    )

records = tools_data.get("tools", [])
assert records, "No curated tool records were found."
record_ids = [record.get("id") for record in records]
assert len(record_ids) == len(set(record_ids)), "Duplicate tool IDs were found."

category_usage = {category_id: 0 for category_id in CATEGORIES}
for record in records:
    domains = record.get("domain") or []
    assert domains, f"{record.get('id')} has no category assignment."
    invalid = set(domains) - set(CATEGORIES)
    assert not invalid, f"{record.get('id')} contains legacy/unknown categories: {sorted(invalid)}"
    for category_id in set(domains):
        category_usage[category_id] += 1
assert all(category_usage.values()), f"Categories with no assigned records: {[key for key, value in category_usage.items() if not value]}"

domain_match = re.search(r"DOMAIN_MAP\s*=\s*\{(.*?)\n\}", processor, re.S)
assert domain_match, "DOMAIN_MAP not found in accepted-tool processing script."
domain_map = dict(re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', domain_match.group(1)))
assert domain_map == {label: category_id for category_id, label in CATEGORIES.items()}, (
    "Accepted-tool processing map does not match the taxonomy."
)

task_match = re.search(r"TASK_MAP\s*=\s*\{(.*?)\n\}", processor, re.S)
assert task_match, "TASK_MAP not found in accepted-tool processing script."
task_ids = set(re.findall(r':\s*"([^"]+)"', task_match.group(1)))
taxonomy_task_ids = {
    task.get("id")
    for category in domain_taxonomy.values()
    for task in category.get("tasks", [])
}
assert task_ids <= taxonomy_task_ids, (
    f"Submission task IDs missing from taxonomy: {sorted(task_ids - taxonomy_task_ids)}"
)

domain_field = next(
    (field for field in form.get("body", []) if field.get("id") == "domain"),
    None,
)
assert domain_field, "The Suggest a Tool form has no category dropdown."
form_categories = domain_field.get("attributes", {}).get("options", [])
assert form_categories == list(CATEGORIES.values()), (
    "Submission form category choices differ from the approved taxonomy."
)
assert 'domain = get_field(\n        "Primary category"\n    )' in processor, (
    "Accepted-tool processing must read the renamed Primary category field."
)

workflow = (ROOT / ".github" / "workflows" / "generate-categories.yml").read_text(encoding="utf-8")
assert '"data/taxonomy.yaml"' in workflow, "Taxonomy changes must trigger category-page regeneration."

print(
    "Functional taxonomy passed: 14 categories, "
    f"{len(records)} curated records, complete task mappings, and matching form/processor IDs."
)
