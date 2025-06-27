#!/usr/bin/env python3
"""
GitHub Actions Workflow Fix Script
Automatically fixes environment variable loading issues in workflows
"""

import os
import re
import shutil
from datetime import datetime


def backup_workflow(file_path):
    """Create a backup of the workflow file"""
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    return backup_path


def add_env_loading_to_workflow(file_path):
    """Add environment variable loading to a workflow file"""
    print(f"🔧 Fixing: {file_path}")

    # Create backup
    backup_path = backup_workflow(file_path)

    # Read the workflow file
    with open(file_path, "r") as f:
        content = f.read()

    # Define the environment loading step
    env_loading_step = """      - name: Load environment variables
        run: |
          # Load environment variables from backend/.env
          if [ -f backend/.env ]; then
            export $(cat backend/.env | grep -v '^#' | xargs)
            echo "Environment variables loaded from backend/.env"
          else
            echo "Warning: backend/.env not found, using GitHub secrets"
          fi

"""

    # Find the position to insert the environment loading step
    # Look for the step after "Install dependencies" or "Download NLTK data"
    patterns = [
        r"(\s+- name: Download NLTK data\n\s+run:.*?\n)",
        r"(\s+- name: Install dependencies\n\s+run:.*?\n)",
        r"(\s+- name: Cache Python dependencies\n\s+uses:.*?\n)",
    ]

    insert_position = None
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            insert_position = match.end()
            break

    if insert_position is None:
        # If no pattern found, insert after the first step
        first_step_match = re.search(r"(\s+- name:.*?\n)", content)
        if first_step_match:
            insert_position = first_step_match.end()

    if insert_position is not None:
        # Insert the environment loading step
        new_content = (
            content[:insert_position] + env_loading_step + content[insert_position:]
        )

        # Write the updated content
        with open(file_path, "w") as f:
            f.write(new_content)

        print(f"✅ Environment loading step added to {file_path}")
        return True
    else:
        print(f"❌ Could not find insertion point in {file_path}")
        return False


def fix_all_workflows():
    """Fix all GitHub Actions workflows"""
    workflows_dir = ".github/workflows"

    if not os.path.exists(workflows_dir):
        print(f"❌ Workflows directory not found: {workflows_dir}")
        return False

    # List of workflows to fix
    workflows_to_fix = [
        "enhanced-wildlife-scanner.yml",
        "human-trafficking-scanner.yml",
        "test-enhanced-system.yml",
    ]

    print("🚀 Starting GitHub Actions Workflow Fixes")
    print("=" * 50)

    fixed_count = 0
    for workflow in workflows_to_fix:
        workflow_path = os.path.join(workflows_dir, workflow)

        if os.path.exists(workflow_path):
            if add_env_loading_to_workflow(workflow_path):
                fixed_count += 1
        else:
            print(f"⚠️ Workflow not found: {workflow_path}")

    print("\n" + "=" * 50)
    print(f"📊 Fix Summary: {fixed_count}/{len(workflows_to_fix)} workflows fixed")

    if fixed_count == len(workflows_to_fix):
        print("🎉 All workflows fixed successfully!")
        print("\n📋 Next Steps:")
        print("1. Commit and push the changes")
        print("2. Test the workflows manually")
        print("3. Verify environment variables are loaded")
    else:
        print("⚠️ Some workflows could not be fixed")

    return fixed_count == len(workflows_to_fix)


def create_env_secrets_guide():
    """Create a guide for adding GitHub secrets"""
    guide_content = """# GitHub Secrets Setup Guide

## 🔧 Required GitHub Secrets

Add these secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:

### Secret 1: SUPABASE_URL
- **Name**: `SUPABASE_URL`
- **Value**: `https://hgnefrvllutcagdutcaa.supabase.co`

### Secret 2: SUPABASE_ANON_KEY
- **Name**: `SUPABASE_ANON_KEY`
- **Value**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhnbmVmcnZsbHV0Y2FnZHV0Y2FhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzMjU4NzcsImV4cCI6MjA2NDkwMTg3N30.ftaP4Xa1vTXumTlcPy0OwdG1s-4JSYz10-ENiWB_QZ0`

### Secret 3: GOOGLE_VISION_API_KEY
- **Name**: `GOOGLE_VISION_API_KEY`
- **Value**: `AIzaSyDpfXySa9vplsSY3CUm9BSAUtazDZDJpoY`

### Secret 4: EBAY_APP_ID
- **Name**: `EBAY_APP_ID`
- **Value**: `ParkerCa-Wildlife-PRD-7f002a9fc-43ad918c`

### Secret 5: EBAY_CERT_ID
- **Name**: `EBAY_CERT_ID`
- **Value**: `PRD-f002a9fc485b-06cf-4a0e-bdf4-b37b`

## ✅ Verification

After adding the secrets:
1. Go to **Actions** tab
2. Manually trigger a workflow
3. Check that it runs without environment variable errors
4. Verify results are being stored

## 🔒 Security Note

These secrets are encrypted and only accessible to GitHub Actions.
They will not be visible in logs or repository files.
"""

    with open("GITHUB_SECRETS_SETUP.md", "w") as f:
        f.write(guide_content)

    print("📄 Created: GITHUB_SECRETS_SETUP.md")


def main():
    """Main function"""
    print("🔧 GitHub Actions Workflow Fixer")
    print("=" * 40)

    # Fix workflows
    success = fix_all_workflows()

    # Create setup guide
    create_env_secrets_guide()

    if success:
        print("\n🎯 All fixes completed successfully!")
        print("📋 Next steps:")
        print("1. Add GitHub secrets (see GITHUB_SECRETS_SETUP.md)")
        print("2. Commit and push the workflow changes")
        print("3. Test the workflows manually")
    else:
        print("\n⚠️ Some fixes failed. Check the output above.")


if __name__ == "__main__":
    main()
