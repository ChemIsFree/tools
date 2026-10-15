from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[2]

TOOLS_FILE = ROOT / "data" / "tools.yaml"
TAXONOMY_FILE = ROOT / "data" / "taxonomy.yaml"
CURATION_FILE = ROOT / "data" / "category_curation.yaml"
CATEGORIES_DIR = ROOT / "categories"


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def normalized_name(value):
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


def name_matches(tool, aliases):
    values = [normalized_name(tool.get("name")), normalized_name(tool.get("id"))]
    targets = [normalized_name(alias) for alias in aliases]
    return any(value and target and (value == target or (len(target) >= 5 and target in value))
               for value in values for target in targets)


def format_status(status):

    return {
        "chemisfree-project": "**ChemIsFree Project**",
        "community-project": "Community Project",
        "curated-resource": "Curated Resource",
        "archived": "Archived",
    }.get(
        status,
        status or ""
    )


def format_list(values):

    if not values:
        return "—"

    return " / ".join(
        str(value)
        .replace("-", " ")
        .title()
        for value in values
    )


def get_task_name(
    taxonomy,
    task_id
):

    for domain in taxonomy.get(
        "domains",
        {}
    ).values():

        for task in domain.get(
            "tasks",
            []
        ):

            if task.get("id") == task_id:

                return task.get(
                    "name",
                    task_id
                )

    return (
        str(task_id)
        .replace("-", " ")
        .title()
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    with open(
        TOOLS_FILE,
        "r",
        encoding="utf-8"
    ) as handle:

        tools_data = yaml.safe_load(
            handle
        )

    with open(
        TAXONOMY_FILE,
        "r",
        encoding="utf-8"
    ) as handle:

        taxonomy = yaml.safe_load(
            handle
        )

    with open(CURATION_FILE, "r", encoding="utf-8") as handle:
        curation_data = yaml.safe_load(handle) or {}

    target_keep = (curation_data.get("category_curation", {}).get("target-identification", {}) or {}).get("keep", [])

    tools = tools_data.get(
        "tools",
        []
    )

    domains = taxonomy.get(
        "domains",
        {}
    )


    # -----------------------------------------------------
    # Remove obsolete generated pages
    # -----------------------------------------------------

    CATEGORIES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    for file in CATEGORIES_DIR.glob(
        "*.md"
    ):

        file.unlink()


    # -----------------------------------------------------
    # Generate one page per major domain
    # -----------------------------------------------------

    for domain_id, domain in domains.items():

        if domain_id == "target-identification":
            # Target Identification is an editorial shortlist, not an automatic
            # keyword bucket. Keep only the names approved in category_curation.yaml.
            domain_tools = [
                tool for tool in tools
                if name_matches(tool, target_keep)
            ]
        else:
            domain_tools = [
                tool
                for tool in tools
                if domain_id in (
                    tool.get(
                        "domain",
                        []
                    )
                )
            ]

        if not domain_tools:
            continue


        output = []

        domain_name = domain.get(
            "name",
            domain_id
        )

        domain_description = domain.get(
            "description",
            ""
        )


        output.append(
            f"# {domain_name}\n"
        )

        if domain_description:

            output.append(
                f"{domain_description}\n"
            )


        output.append(
            "---\n"
        )

        output.append(
            "## Applications\n"
        )


        applications = [
            tool
            for tool in domain_tools
            if tool.get(
                "catalogue"
            ) == "app"
        ]


        resources = [
            tool
            for tool in domain_tools
            if tool.get(
                "catalogue"
            ) == "resource"
        ]


        # -------------------------------------------------
        # Applications
        # -------------------------------------------------

        if applications:

            output.append(
                "| Application | Tasks | Access | Interface | Platforms | Status |"
            )

            output.append(
                "|---|---|---|---|---|---|"
            )


            for tool in sorted(
                applications,
                key=lambda item:
                    item.get(
                        "name",
                        ""
                    ).lower()
            ):

                name = tool.get(
                    "name",
                    "Unnamed"
                )

                website = tool.get(
                    "website",
                    ""
                )

                if website:

                    name = (
                        f"[{name}]"
                        f"({website})"
                    )


                task_names = [
                    get_task_name(
                        taxonomy,
                        task_id
                    )
                    for task_id in tool.get(
                        "tasks",
                        []
                    )
                ]


                interface = []

                interfaces = tool.get(
                    "interface",
                    []
                )

                if (
                    "gui" in interfaces
                    or "web" in interfaces
                ):

                    interface.append(
                        "GUI / Web"
                    )

                if "cli" in interfaces:

                    interface.append(
                        "CLI"
                    )


                output.append(
                    "| "
                    f"{name} | "
                    f"{'; '.join(task_names) or '—'} | "
                    f"{format_list(tool.get('access', []))} | "
                    f"{' + '.join(interface) or '—'} | "
                    f"{format_list(tool.get('platforms', []))} | "
                    f"{format_status(tool.get('chemisfree_status'))} |"
                )


        else:

            output.append(
                "No applications are currently listed in this area.\n"
            )


        # -------------------------------------------------
        # Supporting resources
        # -------------------------------------------------

        if resources:

            output.append(
                "\n## Supporting Resources\n"
            )

            output.append(
                "| Resource | Type | Tasks | Access | Interface |"
            )

            output.append(
                "|---|---|---|---|---|"
            )


            for tool in sorted(
                resources,
                key=lambda item:
                    item.get(
                        "name",
                        ""
                    ).lower()
            ):

                name = tool.get(
                    "name",
                    "Unnamed"
                )

                website = tool.get(
                    "website",
                    ""
                )

                if website:

                    name = (
                        f"[{name}]"
                        f"({website})"
                    )


                task_names = [
                    get_task_name(
                        taxonomy,
                        task_id
                    )
                    for task_id in tool.get(
                        "tasks",
                        []
                    )
                ]


                interface = []

                interfaces = tool.get(
                    "interface",
                    []
                )

                if (
                    "gui" in interfaces
                    or "web" in interfaces
                ):

                    interface.append(
                        "GUI / Web"
                    )

                if "cli" in interfaces:

                    interface.append(
                        "CLI"
                    )


                resource_type = (
                    tool.get(
                        "resource_type"
                    )
                    or tool.get(
                        "type",
                        "resource"
                    )
                )


                output.append(
                    "| "
                    f"{name} | "
                    f"{resource_type} | "
                    f"{'; '.join(task_names) or '—'} | "
                    f"{format_list(tool.get('access', []))} | "
                    f"{' + '.join(interface) or '—'} |"
                )


        output.append(
            "\n---\n"
        )

        output.append(
            "[← Back to ChemIsFree Tools](../README.md)\n"
        )


        filename = (
            domain_id
            .replace(
                "/",
                "-"
            )
            + ".md"
        )


        output_file = (
            CATEGORIES_DIR /
            filename
        )


        output_file.write_text(
            "\n".join(output),
            encoding="utf-8"
        )


        print(
            f"Generated {output_file}"
        )


if __name__ == "__main__":
    main()
