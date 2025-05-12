# Detect the changes to the dbt project
from git import Repo
import os


def get_changes_to_sql_file(base_branch='origin/main'):
    # Initialize the repository
    repo = Repo(os.getcwd())

    # Ensure the repo is not in a detached HEAD state
    if repo.head.is_detached:
        raise RuntimeError(
            "Repository is in a detached HEAD state. Cannot determine current branch.")

    # Get the current branch name
    current_branch = repo.active_branch.name

    # Get the diff between the base branch and the current branch
    diff = repo.git.diff(f'{base_branch}...{current_branch}', name_only=True)

    # Split the diff into a list of changed files
    changed_files = diff.splitlines()

    # Filter for changed .sql files inside the models/ directory
    sql_files = [file for file in changed_files if file.endswith(
        '.sql') and file.startswith('models/')]

    return sql_files


if __name__ == "__main__":
    # Example usage
    base_branch = 'origin/main'  # Change this to your base branch if needed
    changed_sql_files = get_changes_to_sql_file(base_branch)

    if changed_sql_files:
        print("Changed SQL files:")
        for file in changed_sql_files:
            print(f"- {file}")
    else:
        print("No SQL files have changed.")
