import os
import shutil

def clear_folder(path):
    """
    Deletes a folder, then create it again.
    """
    # deletetion
    try:
        shutil.rmtree(path)
        print(f"Folder {path} was successfully deleted")
    except OSError as e:
        print(f"Could not delete folder {path}: {e}")
    # creation
    os.makedirs(path)


def clean_output_dir(output, keep={".git", "CNAME"}):
    """
    Empties the output directory for a clean build, preserving the entries in
    `keep` (the hosting repo's .git and CNAME). Creates the directory if missing.

    Refuses to wipe a non-empty directory that is neither a git repo (contains
    .git) nor the default ./outsite build dir, to avoid nuking the wrong folder.
    """
    if not os.path.isdir(output):
        os.makedirs(output)
        return

    entries = os.listdir(output)
    is_repo = ".git" in entries
    is_default = os.path.abspath(output) == os.path.abspath("./outsite")
    if entries and not is_repo and not is_default:
        raise SystemExit(
            f"Refusing to clean '{output}': not empty, not a git repo, and not "
            f"the default ./outsite. Point --output at the hosting repo or an "
            f"empty/scratch directory."
        )

    print("Cleaning output dir (preserving .git, CNAME)")
    for entry in entries:
        if entry in keep:
            continue
        path = os.path.join(output, entry)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)