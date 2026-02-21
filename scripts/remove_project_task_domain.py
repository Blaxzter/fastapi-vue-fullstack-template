#!/usr/bin/env python3
"""Remove the project/task sample domain from the template.

This removes:
- Backend: models, CRUD, schemas, routes, migration, tests, fixtures, demo data
- Frontend: project views, routes, nav items, E2E tests
- Leaves: auth, user management, health endpoints, base CRUD infrastructure

Usage:
    python scripts/remove_project_task_domain.py          # Interactive confirmation
    python scripts/remove_project_task_domain.py --yes    # Skip confirmation
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
    remove_lines_matching,
    replace_in_file,
    self_clean,
)

FILES_TO_DELETE = [
    # Backend models
    "backend/app/models/project.py",
    "backend/app/models/task.py",
    # Backend CRUD
    "backend/app/crud/project.py",
    "backend/app/crud/task.py",
    # Backend schemas
    "backend/app/schemas/project.py",
    "backend/app/schemas/task.py",
    # Backend API routes
    "backend/app/api/routes/projects.py",
    "backend/app/api/routes/tasks.py",
    # Alembic migration for projects/tasks
    "backend/app/alembic/versions/20260131_0002_projects_tasks.py",
    # Demo data scripts
    "backend/app/scripts/reset_demo_data.py",
    # Backend tests
    "backend/tests/crud/test_project.py",
    "backend/tests/crud/test_task.py",
    "backend/tests/api/routes/test_projects.py",
    "backend/tests/api/routes/test_tasks.py",
    "backend/tests/fixtures/projects.py",
    "backend/tests/fixtures/tasks.py",
    # Frontend E2E tests
    "frontend/e2e/tests/authenticated/projects-tasks.spec.ts",
]

DIRS_TO_DELETE = [
    "backend/app/scripts/demo",
    "frontend/src/views/projects",
]

# Route paths to remove from router/index.ts
PROJECT_ROUTE_PATHS = [
    "projects/:projectId",  # Remove detail route first (more specific path)
    "projects",
]

# JSON keys to remove from navigation.json
NAVIGATION_KEYS_TO_REMOVE = [
    "breadcrumbs.project",
    "breadcrumbs.projects",
    "sidebar.items.projects",
    "sidebar.sections.starter",
]


def modify_backend_api_router(root: Path) -> None:
    """Remove project and task router includes from api.py."""
    api_path = root / "backend/app/api/api.py"

    # Fix import line
    replace_in_file(
        api_path,
        "from app.api.routes import health, projects, tasks, users",
        "from app.api.routes import health, users",
    )

    # Remove router includes
    remove_lines_matching(
        api_path,
        [
            r"api_router\.include_router\(projects\.router\)",
            r"api_router\.include_router\(tasks\.router\)",
        ],
    )


def modify_backend_models_init(root: Path) -> None:
    """Remove Project and Task from models/__init__.py."""
    init_path = root / "backend/app/models/__init__.py"

    # Remove import lines
    remove_lines_matching(
        init_path,
        [
            r"from \.project import Project",
            r"from \.task import Task",
        ],
    )

    # Remove from __all__ list
    replace_in_file(init_path, '    "Project",\n', "")
    replace_in_file(init_path, '    "Task",\n', "")


def modify_backend_initial_data(root: Path) -> None:
    """Remove demo data seeding from initial_data.py."""
    init_data_path = root / "backend/app/scripts/initial_data.py"

    remove_lines_matching(
        init_data_path,
        [
            r"from app\.scripts\.demo\.demo_data import seed_demo_data",
            r"await seed_demo_data\(",
        ],
    )


def modify_backend_conftest(root: Path) -> None:
    """Remove project/task fixture imports from conftest.py."""
    conftest_path = root / "backend/tests/conftest.py"

    remove_lines_matching(
        conftest_path,
        [
            r"from tests\.fixtures\.projects import",
            r"from tests\.fixtures\.tasks import",
        ],
    )


def modify_frontend_router(root: Path) -> None:
    """Remove project routes from Vue router."""
    router_path = root / "frontend/src/router/index.ts"
    for route_path in PROJECT_ROUTE_PATHS:
        remove_block(router_path, rf"path:\s*'{re.escape(route_path)}'")


def modify_frontend_sidebar(root: Path) -> None:
    """Remove project-related nav from AppSidebar.vue."""
    sidebar_path = root / "frontend/src/components/navigation/AppSidebar.vue"

    # Remove "Starter" nav section
    remove_block(sidebar_path, r"title:\s*'Starter'")

    # Remove the projects data array
    remove_block(sidebar_path, r"^\s*projects:\s*\[", open_char="[", close_char="]")

    # Remove NavProjects import and usage
    remove_lines_matching(
        sidebar_path,
        [
            r"import NavProjects from",
            r"<NavProjects",
        ],
    )

    # Remove lucide icons used only by projects data and Starter nav
    for icon in ["FolderKanban", "Frame", "Map", "PieChart"]:
        replace_in_file(sidebar_path, f"  {icon},\n", "")


def modify_frontend_translations(root: Path) -> None:
    """Remove project-related keys from navigation translation files."""
    for lang in ["en", "de"]:
        nav_path = root / f"frontend/src/locales/{lang}/navigation.json"
        remove_json_keys(nav_path, NAVIGATION_KEYS_TO_REMOVE)


def main() -> None:
    root: Path = get_project_root()

    all_items = (
        FILES_TO_DELETE
        + [f"{d}/ (directory)" for d in DIRS_TO_DELETE]
        + [
            "backend/app/api/api.py (remove project/task router includes)",
            "backend/app/models/__init__.py (remove Project/Task imports)",
            "backend/app/scripts/initial_data.py (remove demo data seeding)",
            "backend/tests/conftest.py (remove project/task fixture imports)",
            "frontend/src/router/index.ts (remove project routes)",
            "frontend/src/components/navigation/AppSidebar.vue (remove Starter nav + projects)",
            "frontend/src/locales/en/navigation.json (remove project keys)",
            "frontend/src/locales/de/navigation.json (remove project keys)",
        ]
    )

    if not confirm_action("Remove project/task domain content:", all_items):
        print("Aborted.")
        sys.exit(0)

    print("\nModifying backend files...")
    modify_backend_api_router(root)
    modify_backend_models_init(root)
    modify_backend_initial_data(root)
    modify_backend_conftest(root)

    print("\nModifying frontend files...")
    modify_frontend_router(root)
    modify_frontend_sidebar(root)
    modify_frontend_translations(root)

    print("\nDeleting files...")
    delete_files(root, FILES_TO_DELETE)

    print("\nDeleting directories...")
    delete_directories(root, DIRS_TO_DELETE)

    print("\nCleaning up scripts...")
    self_clean(root)

    print_next_steps(
        [
            "Run: just generate-client  (regenerate frontend API client)",
            "Run: just lint-backend && just lint-frontend",
            "Run: just test-backend",
            "If your DB already has project/task tables, drop and recreate it",
            "Commit your changes",
        ]
    )


if __name__ == "__main__":
    main()
