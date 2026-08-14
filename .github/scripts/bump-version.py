#!/usr/bin/env python3
"""Bump addon minor version in config.yaml and add entry to CHANGELOG.md."""

import argparse
import os
import re
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Bump addon minor version and update changelog.")
    parser.add_argument(
        "--config",
        default="gitea/config.yaml",
        help="Path to config.yaml (default: gitea/config.yaml)",
    )
    parser.add_argument(
        "--changelog",
        default="gitea/CHANGELOG.md",
        help="Path to CHANGELOG.md (default: gitea/CHANGELOG.md)",
    )
    parser.add_argument(
        "--upstream-version",
        required=True,
        help="Upstream Gitea package version from Alpine (e.g. 1.22.3-r0)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write changes to disk, only print them.",
    )
    return parser.parse_args()


def bump_minor_version(version_str: str) -> str:
    """Bump the minor component of a semantic version string (e.g., 0.3.4 -> 0.4.0)."""
    parts = version_str.strip().split(".")
    if len(parts) >= 2:
        major = int(parts[0])
        minor = int(parts[1])
        return f"{major}.{minor + 1}.0"
    elif len(parts) == 1:
        major = int(parts[0])
        return f"{major + 1}.0.0"
    else:
        raise ValueError(f"Unable to parse version string: {version_str}")


def update_config_file(config_path: str, dry_run: bool = False) -> tuple[str, str]:
    """Read config.yaml, bump minor version, and write back."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'^(version:\s*["\']?)([^"\'\n]+)(["\']?)', content, re.MULTILINE)
    if not match:
        raise ValueError(f"Could not find 'version:' field in {config_path}")

    prefix, current_version, suffix = match.group(1), match.group(2), match.group(3)
    new_version = bump_minor_version(current_version)

    new_content = re.sub(
        r'^(version:\s*["\']?)[^"\'\n]+(["\']?)',
        rf'\g<1>{new_version}\g<2>',
        content,
        count=1,
        flags=re.MULTILINE,
    )

    if not dry_run:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(new_content)

    return current_version, new_version


def update_changelog_file(
    changelog_path: str,
    new_addon_version: str,
    upstream_version: str,
    dry_run: bool = False,
):
    """Insert new version entry into CHANGELOG.md."""
    if not os.path.exists(changelog_path):
        raise FileNotFoundError(f"Changelog file not found: {changelog_path}")

    with open(changelog_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_entry = f"## {new_addon_version}\n\n- Update Gitea to {upstream_version}\n"

    # Preserve any top comments (e.g. <!-- ... -->)
    comment_match = re.search(r'^(<!--.*?-->\n*)', content, re.DOTALL)
    if comment_match:
        header = comment_match.group(1).rstrip() + "\n\n"
        rest = content[comment_match.end():].lstrip()
        new_content = f"{header}{new_entry}\n{rest}"
    else:
        new_content = f"{new_entry}\n{content}"

    if not dry_run:
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(new_content)


def main():
    args = parse_args()

    print(f"Upstream Gitea version: {args.upstream_version}")
    current_ver, new_ver = update_config_file(args.config, dry_run=args.dry_run)
    print(f"Addon version bumped from {current_ver} -> {new_ver} in {args.config}")

    update_changelog_file(
        args.changelog,
        new_ver,
        args.upstream_version,
        dry_run=args.dry_run,
    )
    print(f"Updated {args.changelog} with release {new_ver}")

    # Set GITHUB_OUTPUT if available
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"previous_addon_version={current_ver}\n")
            f.write(f"new_addon_version={new_ver}\n")
            f.write(f"upstream_version={args.upstream_version}\n")


if __name__ == "__main__":
    main()
