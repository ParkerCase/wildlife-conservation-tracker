#!/usr/bin/env python3
"""
WildGuard Workflow Consolidation - Disable Competing Workflows
Disables 9 competing workflows to prevent database conflicts
"""

import os
import shutil
from datetime import datetime

class WorkflowConsolidator:
    def __init__(self):
        self.workflows_dir = ".github/workflows"
        
        # Workflows to KEEP (the 3 coordinated ones)
        self.keep_workflows = [
            "final-production-scanner.yml",
            "enhanced-production-scanner.yml", 
            "continuous-conservation-scanner.yml"
        ]
        
        # Workflows to DISABLE (the 9 competing ones)
        self.disable_workflows = [
            "massive-scale-production.yml",
            "complete-enhanced-scanner.yml",
            "wildguard-scanner-v2-fixed.yml",
            "fixed-multilingual-scanner.yml",
            "fixed-production-scanner.yml",
            "gumtree-avito-scanner.yml",
            "historical-backfill.yml",
            "scanner-fixed-simple.yml",
            "enhanced-global-scanner.yml"
        ]
        
        self.backup_dir = f".github/disabled_workflows_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def create_backup_directory(self):
        """Create backup directory for disabled workflows"""
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            print(f"📁 Created backup directory: {self.backup_dir}")
            return True
        except Exception as e:
            print(f"❌ Could not create backup directory: {e}")
            return False
    
    def disable_workflow(self, workflow_name):
        """Disable a workflow by moving it to backup directory"""
        source_path = os.path.join(self.workflows_dir, workflow_name)
        backup_path = os.path.join(self.backup_dir, workflow_name)
        
        try:
            if os.path.exists(source_path):
                shutil.move(source_path, backup_path)
                print(f"✅ Disabled: {workflow_name}")
                return True
            else:
                print(f"⚠️  Not found: {workflow_name}")
                return False
        except Exception as e:
            print(f"❌ Error disabling {workflow_name}: {e}")
            return False
    
    def list_current_workflows(self):
        """List all current workflows"""
        print("📋 Current workflows:")
        try:
            workflows = [f for f in os.listdir(self.workflows_dir) if f.endswith('.yml')]
            for workflow in sorted(workflows):
                status = "🟢 KEEP" if workflow in self.keep_workflows else "🔴 DISABLE"
                print(f"   {status} {workflow}")
            return workflows
        except Exception as e:
            print(f"❌ Could not list workflows: {e}")
            return []
    
    def consolidate_workflows(self):
        """Main consolidation process"""
        print("🚀 WildGuard Workflow Consolidation")
        print("=" * 50)
        print("This will disable 9 competing workflows to prevent database conflicts.")
        print("The 3 coordinated workflows will remain active.")
        print()
        
        # Step 1: List current workflows
        current_workflows = self.list_current_workflows()
        
        if not current_workflows:
            print("❌ No workflows found")
            return False
        
        print(f"\n📊 Found {len(current_workflows)} total workflows")
        print(f"🟢 Keeping: {len(self.keep_workflows)} workflows")
        print(f"🔴 Disabling: {len(self.disable_workflows)} workflows")
        
        # Step 2: Create backup directory
        if not self.create_backup_directory():
            return False
        
        # Step 3: Disable competing workflows
        print(f"\n🔧 Disabling competing workflows...")
        disabled_count = 0
        
        for workflow in self.disable_workflows:
            if self.disable_workflow(workflow):
                disabled_count += 1
        
        # Step 4: Verify remaining workflows
        print(f"\n📋 Remaining active workflows:")
        remaining_workflows = [f for f in os.listdir(self.workflows_dir) if f.endswith('.yml')]
        
        for workflow in sorted(remaining_workflows):
            print(f"   ✅ {workflow}")
        
        # Step 5: Results
        print(f"\n🎯 CONSOLIDATION RESULTS:")
        print(f"   🔴 Disabled: {disabled_count} workflows")
        print(f"   🟢 Active: {len(remaining_workflows)} workflows")
        print(f"   📁 Backup location: {self.backup_dir}")
        
        if disabled_count == len(self.disable_workflows):
            print("\n✅ Workflow consolidation successful!")
            print("\n💡 NEXT STEPS:")
            print("1. Commit and push these changes to GitHub")
            print("2. Run the database cleanup script: python fix_database_limits.py")
            print("3. Monitor your workflows in GitHub Actions")
            print("\n🎯 EXPECTED RESULTS:")
            print("• Zero workflow conflicts")
            print("• Coordinated 9 scans per day (3 workflows × 3 times each)")
            print("• 100k-200k listings per day target")
            print("• No more Supabase limit issues")
            return True
        else:
            print(f"\n⚠️  Only {disabled_count}/{len(self.disable_workflows)} workflows disabled")
            print("Some workflows may not have existed or had permission issues.")
            return False
    
    def restore_workflows(self):
        """Restore disabled workflows if needed"""
        print("🔄 Restoring disabled workflows...")
        
        if not os.path.exists(self.backup_dir):
            print("❌ No backup directory found")
            return False
        
        try:
            backup_workflows = [f for f in os.listdir(self.backup_dir) if f.endswith('.yml')]
            restored_count = 0
            
            for workflow in backup_workflows:
                backup_path = os.path.join(self.backup_dir, workflow)
                restore_path = os.path.join(self.workflows_dir, workflow)
                
                shutil.move(backup_path, restore_path)
                print(f"✅ Restored: {workflow}")
                restored_count += 1
            
            print(f"\n🎯 Restored {restored_count} workflows")
            return True
            
        except Exception as e:
            print(f"❌ Error during restoration: {e}")
            return False

def main():
    print("🌍 WildGuard Workflow Consolidation Tool")
    print("=" * 50)
    
    consolidator = WorkflowConsolidator()
    
    # Check if we're in the right directory
    if not os.path.exists(".github/workflows"):
        print("❌ Not in the correct directory!")
        print("Please run this from your conservation-bot root directory.")
        return
    
    # Run consolidation
    success = consolidator.consolidate_workflows()
    
    if success:
        print("\n🎉 Workflow consolidation completed!")
        print("Your GitHub Actions will now run in coordination without conflicts.")
    else:
        print("\n⚠️  Consolidation encountered some issues.")
        print("Check the output above for details.")

if __name__ == "__main__":
    main()
