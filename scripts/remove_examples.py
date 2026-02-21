#!/usr/bin/env python3
"""Remove all example/demo/placeholder content from the template.

This removes:
- Example views (breadcrumb, layout, dialog, error handling, error boundary demos)
- Example translations (en/de example.json)
- Example backend schema
- Example routes, nav items, and breadcrumb keys
- Placeholder sidebar sections (Playground, Documentation, Settings with url: '#')
- Placeholder NavUser menu items (Upgrade to Pro, Billing, Notifications)
- Dummy team data (simplifies to single "My App" team)
- Unused lucide icon imports
- Example E2E tests

Usage:
    python scripts/remove_examples.py          # Interactive confirmation
    python scripts/remove_examples.py --yes    # Skip confirmation
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Allow running from repo root or scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cleanup_utils import (
    confirm_action,
    delete_directories,
    delete_files,
    get_project_root,
    print_next_steps,
    remove_block,
    remove_json_keys,
    replace_in_file,
    self_clean,
)

FILES_TO_DELETE = [
    "backend/app/schemas/example.py",
    "frontend/src/locales/en/example.json",
    "frontend/src/locales/de/example.json",
    "frontend/e2e/tests/authenticated/examples.spec.ts",
]

DIRS_TO_DELETE = [
    "frontend/src/views/examples",
]

# Example route paths to remove from router/index.ts
EXAMPLE_ROUTE_PATHS = [
    "examples",
    "breadcrumb-examples",
    "layout-demo",
    "dialog-examples",
    "error-handling-demo",
    "error-boundary-demo",
]

# JSON keys to remove from navigation.json (both en and de)
NAVIGATION_KEYS_TO_REMOVE = [
    # Example breadcrumbs
    "breadcrumbs.breadcrumbExamples",
    "breadcrumbs.dialogExamples",
    "breadcrumbs.errorBoundaryDemo",
    "breadcrumbs.errorHandlingDemo",
    "breadcrumbs.examples",
    "breadcrumbs.layoutDemo",
    # Example sidebar items
    "sidebar.items.breadcrumbExamples",
    "sidebar.items.dialogExamples",
    "sidebar.items.errorBoundaryDemo",
    "sidebar.items.errorHandlingDemo",
    "sidebar.items.layoutDemo",
    "sidebar.sections.examples",
    # Placeholder sidebar items (Playground section)
    "sidebar.items.history",
    "sidebar.items.starred",
    "sidebar.sections.playground",
    # Placeholder sidebar items (Documentation section)
    "sidebar.items.changelog",
    "sidebar.items.getStarted",
    "sidebar.items.introduction",
    "sidebar.items.tutorials",
    "sidebar.sections.documentation",
    # Placeholder sidebar items (Settings section)
    "sidebar.items.billing",
    "sidebar.items.general",
    "sidebar.items.limits",
    "sidebar.items.team",
    "sidebar.sections.settings",
    # Placeholder user menu items
    "user.actions.billing",
    "user.actions.notifications",
    "user.actions.upgradeToPro",
]


def remove_example_routes(root: Path) -> None:
    """Remove example route blocks from the Vue router."""
    router_path = root / "frontend/src/router/index.ts"
    for route_path in EXAMPLE_ROUTE_PATHS:
        remove_block(router_path, rf"path:\s*'{re.escape(route_path)}'")


def remove_placeholder_nav(root: Path) -> None:
    """Remove placeholder sidebar sections and simplify teams data."""
    sidebar_path = root / "frontend/src/components/navigation/AppSidebar.vue"

    # Remove Examples, Playground, Documentation, Settings nav sections
    for title in ["Examples", "Playground", "Documentation", "Settings"]:
        remove_block(sidebar_path, rf"title:\s*'{title}'")

    # Simplify teams array: replace 3 dummy teams with one placeholder
    replace_in_file(
        sidebar_path,
        """  teams: [
    {
      name: 'Acme Inc',
      logo: GalleryVerticalEnd,
      plan: 'Enterprise',
    },
    {
      name: 'Acme Corp.',
      logo: AudioWaveform,
      plan: 'Startup',
    },
    {
      name: 'Evil Corp.',
      logo: Command,
      plan: 'Free',
    },
  ],""",
        """  teams: [
    {
      name: 'My App',
      logo: GalleryVerticalEnd,
      plan: 'Free',
    },
  ],""",
    )

    # Remove unused lucide icon imports (keep GalleryVerticalEnd for team, FolderKanban for Starter)
    for icon in [
        "AudioWaveform",
        "BookOpen",
        "Bot",
        "Command",
        "Settings2",
        "SquareTerminal",
    ]:
        replace_in_file(sidebar_path, f"  {icon},\n", "")


def remove_placeholder_user_menu(root: Path) -> None:
    """Remove placeholder items from NavUser dropdown."""
    nav_user_path = root / "frontend/src/components/navigation/NavUser.vue"

    # Remove "Upgrade to Pro" group (entire DropdownMenuGroup + separator before it)
    replace_in_file(
        nav_user_path,
        """          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuItem>
              <Sparkles />
              {{ $t('navigation.user.actions.upgradeToPro') }}
            </DropdownMenuItem>
          </DropdownMenuGroup>""",
        "",
    )

    # Remove "Billing" and "Notifications" items from the account group
    replace_in_file(
        nav_user_path,
        """            <DropdownMenuItem>
              <CreditCard />
              {{ $t('navigation.user.actions.billing') }}
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Bell />
              {{ $t('navigation.user.actions.notifications') }}
            </DropdownMenuItem>""",
        "",
    )

    # Remove unused icon imports
    for icon in ["Bell", "CreditCard", "Sparkles"]:
        replace_in_file(nav_user_path, f"  {icon},\n", "")


def remove_example_translations(root: Path) -> None:
    """Remove example and placeholder keys from navigation translation files."""
    for lang in ["en", "de"]:
        nav_path = root / f"frontend/src/locales/{lang}/navigation.json"
        remove_json_keys(nav_path, NAVIGATION_KEYS_TO_REMOVE)


def main() -> None:
    root = get_project_root()

    all_items = (
        FILES_TO_DELETE
        + [f"{d}/ (directory)" for d in DIRS_TO_DELETE]
        + [
            "frontend/src/router/index.ts (remove 6 example routes)",
            "frontend/src/components/navigation/AppSidebar.vue (remove placeholder nav sections, simplify teams)",
            "frontend/src/components/navigation/NavUser.vue (remove placeholder menu items)",
            "frontend/src/locales/en/navigation.json (remove example + placeholder keys)",
            "frontend/src/locales/de/navigation.json (remove example + placeholder keys)",
        ]
    )

    if not confirm_action("Remove all example/demo/placeholder content:", all_items):
        print("Aborted.")
        sys.exit(0)

    print("\nModifying files...")
    remove_example_routes(root)
    remove_placeholder_nav(root)
    remove_placeholder_user_menu(root)
    remove_example_translations(root)

    print("\nDeleting files...")
    delete_files(root, FILES_TO_DELETE)

    print("\nDeleting directories...")
    delete_directories(root, DIRS_TO_DELETE)

    print("\nCleaning up scripts...")
    self_clean(root)

    print_next_steps(
        [
            "Run: just generate-client",
            "Run: just lint-backend && just lint-frontend",
            "Run: just test-backend",
            "Commit your changes",
        ]
    )


if __name__ == "__main__":
    main()
