from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOLS_FILE = ROOT / "data" / "tools.yaml"
CATEGORIES_DIR = ROOT / "categories"


def format_list(values):
    if not values:
        return ""

    return " / ".join(
        str(value).replace("-", " ").title()
        for value in values
    )


def format_status(status):
    return {
        "chemisfree-project": "**ChemIsFree Project**",
        "community-project": "Community Project",
        "curated-resource": "Curated Resource",
        "archived": "Archived",
    }.get(status, status)


def category_title(category):
    return category.replace("-", " ").title()


def main():
    with open(TOOLS_FILE, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    tools = data.get("tools", [])

    grouped = {}

    for tool in tools:
        for category in tool.get("category", []):
            grouped.setdefault(category, []).append(tool)

    for category, category_tools in grouped.items():

        output = []

        title = category_title(category)

        output.append(f"# {title}\n")

        output.append(
            "Tools and resources for chemistry, computational chemistry, "
            "drug discovery, and related research workflows.\n"
        )

        output.append("---\n")
        output.append("## Tools\n")

        output.append(
            "| Tool | Description | Type | Access | Interface | "
            "Platforms | ChemIsFree Status |"
        )
        output.append(
            "|---|---|---|---|---|---|---|"
        )

        for tool in sorted(category_tools, key=lambda x: x["name"].lower()):

            name = tool["name"]
            website = tool.get("website", "")

            if website:
                name = f"[{name}]({website})"

            description = " ".join(
                str(tool.get("description", "")).split()
            )

            tool_type = tool.get("type", "")
            access = format_list(tool.get("access", []))
            interface = format_list(tool.get("interface", []))
            platforms = format_list(tool.get("platforms", []))
            status = format_status(
                tool.get("chemisfree_status", "")
            )

            output.append(
                f"| {name} | {description} | {tool_type} | "
                f"{access} | {interface} | {platforms} | {status} |"
            )

        output.append("\n---\n")
        output.append("[← Back to ChemIsFree Tools](../README.md)\n")

        output_file = CATEGORIES_DIR / f"{category}.md"

        output_file.write_text(
            "\n".join(output),
            encoding="utf-8"
        )

        print(f"Generated {output_file}")


if __name__ == "__main__":
    main()
