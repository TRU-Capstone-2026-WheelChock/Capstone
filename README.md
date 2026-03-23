# Capstone

This repository manages the main project and the component repositories under `components/` as Git submodules.

## Repository Structure

- `components/capstone-center`
- `components/capstone-display`
- `components/capstone-motor-component`
- `components/capstone-thermal-sensor-component`
- `components/mock-sensor`
- `Docker/`
- `test/`

## Clone With Submodules

For the first clone, fetch submodules at the same time:

```bash
git clone --recurse-submodules <this-repository-url>
cd Capstone
```

If you already cloned the repository without submodules, run:

```bash
git submodule update --init --recursive
```

## Recommended Pull Workflow

When the root repository is updated and its submodule pointers have changed, run:

```bash
git pull
git submodule update --init --recursive
```

You can also do it in one command:

```bash
git pull --recurse-submodules
```

The important point is that `git pull` alone may update only the root repository. The working tree inside each submodule can remain on an older commit until `git submodule update --init --recursive` is run.

## How To Confirm Submodules Are Updated

Check the current submodule state with:

```bash
git submodule status
```

Typical prefixes:

- ` ` (space): the submodule is checked out at the commit recorded by the root repository
- `+`: the checked-out commit in the submodule does not match the commit recorded by the root repository
- `-`: the submodule is not initialized yet
- `U`: there is a merge conflict

Example:

```bash
git status
git submodule status
```

If `git status` is clean and `git submodule status` does not show `+` or `-`, the root repository and submodules are aligned.

## Normal Behavior In Submodules

Inside a submodule, `git status` often shows:

```bash
HEAD detached at <commit>
```

This is normal. A submodule is usually checked out at the exact commit recorded by the root repository, not automatically on a branch tip.

## If A Submodule Remote Has Newer Commits

There are two different cases:

### 1. The root repository already points to the newer submodule commit

In this case, run:

```bash
git pull
git submodule update --init --recursive
```

This is the usual daily workflow.

### 2. The submodule remote has moved, but the root repository has not recorded it yet

In this case, updating only the submodule is not enough. You also need to record the new submodule commit in the root repository.

Example with `capstone-display`:

```bash
git -C components/capstone-display checkout main
git -C components/capstone-display pull origin main
git add components/capstone-display
git commit -m "Update capstone-display submodule"
```

After that, push the root repository commit as usual.

Without `git add components/capstone-display`, the root repository will not remember the new submodule commit.

## Useful Commands

Initialize all submodules:

```bash
git submodule update --init --recursive
```

Sync submodule URLs from `.gitmodules`:

```bash
git submodule sync --recursive
```

Show which submodule is out of sync:

```bash
git diff --submodule
```

## Optional Convenience Setting

If you want Git commands like `pull` to recurse into submodules more often, you can enable:

```bash
git config --global submodule.recurse true
```

Even with this setting, when something looks off, `git submodule update --init --recursive` is still the safest recovery step.
