#!/usr/bin/env python3
"""
GitHub Actions Workflow Test Script
Tests all the workflows mentioned in the strategy to identify issues
"""

import os
import json
import asyncio
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class GitHubActionsTester:
    def __init__(self):
        self.results = {
            "enhanced_wildlife_scanner": {"status": "unknown", "issues": []},
            "human_trafficking_scanner": {"status": "unknown", "issues": []},
            "test_enhanced_system": {"status": "unknown", "issues": []},
        }

    def test_file_existence(self):
        """Test if all required files exist"""
        logger.info("🔍 Testing file existence...")

        required_files = [
            "ultimate_wildguard_scanner.py",
            "complete_enhanced_scanner.py",
            "multilingual_wildlife_keywords.json",
            "enhanced_platforms/enhanced_threat_scorer.py",
            "enhanced_platforms/google_vision_controller.py",
            "enhanced_platforms/aliexpress_scanner.py",
            "enhanced_platforms/taobao_scanner.py",
            ".github/workflows/enhanced-wildlife-scanner.yml",
            ".github/workflows/human-trafficking-scanner.yml",
            ".github/workflows/test-enhanced-system.yml",
        ]

        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
            else:
                logger.info(f"✅ {file_path}")

        if missing_files:
            logger.error(f"❌ Missing files: {missing_files}")
            return False
        else:
            logger.info("✅ All required files exist")
            return True

    def test_imports(self):
        """Test if all required modules can be imported"""
        logger.info("📦 Testing module imports...")

        import_tests = [
            ("ultimate_wildguard_scanner", "UltimateWildGuardScanner"),
            ("complete_enhanced_scanner", "CompleteEnhancedScanner"),
            ("enhanced_platforms.enhanced_threat_scorer", "EnhancedThreatScorer"),
            ("enhanced_platforms.google_vision_controller", "GoogleVisionController"),
            ("enhanced_platforms.aliexpress_scanner", "AliExpressScanner"),
            ("enhanced_platforms.taobao_scanner", "TaobaoScanner"),
        ]

        failed_imports = []
        for module, class_name in import_tests:
            try:
                module_obj = __import__(module, fromlist=[class_name])
                class_obj = getattr(module_obj, class_name)
                logger.info(f"✅ {module}.{class_name}")
            except Exception as e:
                failed_imports.append(f"{module}.{class_name}: {e}")
                logger.error(f"❌ {module}.{class_name}: {e}")

        if failed_imports:
            logger.error(f"❌ Failed imports: {failed_imports}")
            return False
        else:
            logger.info("✅ All modules imported successfully")
            return True

    def test_environment_variables(self):
        """Test if required environment variables are set"""
        logger.info("🔧 Testing environment variables...")

        required_vars = [
            "SUPABASE_URL",
            "SUPABASE_ANON_KEY",
            "GOOGLE_VISION_API_KEY",
            "EBAY_APP_ID",
            "EBAY_CERT_ID",
        ]

        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
                logger.error(f"❌ {var}: Not set")
            else:
                # Mask sensitive values
                masked_value = (
                    f"{value[:3]}...{value[-3:]}" if len(value) > 6 else "***"
                )
                logger.info(f"✅ {var}: {masked_value}")

        if missing_vars:
            logger.error(f"❌ Missing environment variables: {missing_vars}")
            return False
        else:
            logger.info("✅ All environment variables are set")
            return True

    def test_multilingual_keywords(self):
        """Test multilingual keywords file"""
        logger.info("🌍 Testing multilingual keywords...")

        try:
            with open(
                "multilingual_wildlife_keywords.json", "r", encoding="utf-8"
            ) as f:
                data = json.load(f)

            keywords_by_language = data["keywords_by_language"]
            total_keywords = sum(len(words) for words in keywords_by_language.values())

            logger.info(f"✅ Languages: {len(keywords_by_language)}")
            logger.info(f"✅ Total keywords: {total_keywords:,}")

            # Test key languages
            key_languages = ["en", "zh", "es", "fr"]
            for lang in key_languages:
                if lang in keywords_by_language:
                    count = len(keywords_by_language[lang])
                    logger.info(f"✅ {lang}: {count} keywords")
                else:
                    logger.error(f"❌ Missing {lang} keywords")
                    return False

            logger.info("✅ Multilingual keywords loaded successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Multilingual keywords error: {e}")
            return False

    def test_enhanced_wildlife_scanner_workflow(self):
        """Test the enhanced wildlife scanner workflow logic"""
        logger.info("🦁 Testing enhanced wildlife scanner workflow...")

        try:
            # Test keyword loading logic
            state_file = "wildlife_keyword_state.json"
            default_state = {
                "last_index": 0,
                "total_keywords": 0,
                "last_run": None,
                "completed_cycles": 0,
                "platforms_rotation": [
                    "ebay",
                    "aliexpress",
                    "taobao",
                    "craigslist",
                    "olx",
                    "marktplaats",
                    "mercadolibre",
                ],
            }

            # Load or initialize state
            try:
                with open(state_file, "r") as f:
                    state = json.load(f)
            except FileNotFoundError:
                state = default_state

            # Load multilingual keywords
            with open("multilingual_wildlife_keywords.json", "r") as f:
                keywords_data = json.load(f)
                all_keywords = []
                for lang_keywords in keywords_data["keywords_by_language"].values():
                    all_keywords.extend(lang_keywords)
                all_keywords = list(set(all_keywords))
                state["total_keywords"] = len(all_keywords)

            # Calculate batch
            batch_size = 15
            start_idx = state["last_index"]
            end_idx = min(start_idx + batch_size, len(all_keywords))

            if start_idx >= len(all_keywords):
                start_idx = 0
                end_idx = min(batch_size, len(all_keywords))
                state["completed_cycles"] += 1

            current_batch = all_keywords[start_idx:end_idx]

            logger.info(
                f"✅ Keyword batch calculated: {start_idx}-{end_idx}/{len(all_keywords)}"
            )
            logger.info(f"✅ Current batch: {current_batch[:3]}...")
            logger.info(f"✅ Completed cycles: {state['completed_cycles']}")

            # Test scanner initialization (without running full scan)
            from ultimate_wildguard_scanner import UltimateWildGuardScanner

            # Test if scanner can be initialized
            scanner = UltimateWildGuardScanner()
            logger.info("✅ UltimateWildGuardScanner initialized successfully")

            self.results["enhanced_wildlife_scanner"]["status"] = "passed"
            return True

        except Exception as e:
            logger.error(f"❌ Enhanced wildlife scanner test failed: {e}")
            self.results["enhanced_wildlife_scanner"]["status"] = "failed"
            self.results["enhanced_wildlife_scanner"]["issues"].append(str(e))
            return False

    def test_human_trafficking_scanner_workflow(self):
        """Test the human trafficking scanner workflow logic"""
        logger.info("🚨 Testing human trafficking scanner workflow...")

        try:
            # Test keyword loading logic
            human_trafficking_keywords = [
                "massage therapy",
                "personal service",
                "companionship",
                "entertainment work",
                "modeling opportunity",
                "dance opportunity",
                "hostess needed",
                "waitress needed",
                "travel companion",
                "personal assistant",
                "no experience required",
            ]

            state_file = "human_trafficking_keyword_state.json"
            default_state = {
                "last_index": 0,
                "total_keywords": len(human_trafficking_keywords),
                "last_run": None,
                "completed_cycles": 0,
                "high_priority_platforms": ["craigslist", "gumtree", "olx", "facebook"],
            }

            # Load or initialize state
            try:
                with open(state_file, "r") as f:
                    state = json.load(f)
            except FileNotFoundError:
                state = default_state

            # Calculate batch
            batch_size = 10
            start_idx = state["last_index"]
            end_idx = min(start_idx + batch_size, len(human_trafficking_keywords))

            if start_idx >= len(human_trafficking_keywords):
                start_idx = 0
                end_idx = min(batch_size, len(human_trafficking_keywords))
                state["completed_cycles"] += 1

            current_batch = human_trafficking_keywords[start_idx:end_idx]

            logger.info(
                f"✅ Human trafficking keyword batch: {start_idx}-{end_idx}/{len(human_trafficking_keywords)}"
            )
            logger.info(f"✅ Current batch: {current_batch[:3]}...")
            logger.info(f"✅ Completed cycles: {state['completed_cycles']}")

            # Test component imports
            from enhanced_platforms.enhanced_threat_scorer import EnhancedThreatScorer
            from enhanced_platforms.google_vision_controller import (
                GoogleVisionController,
            )
            from complete_enhanced_scanner import CompleteEnhancedScanner

            logger.info("✅ All human trafficking scanner components imported")

            self.results["human_trafficking_scanner"]["status"] = "passed"
            return True

        except Exception as e:
            logger.error(f"❌ Human trafficking scanner test failed: {e}")
            self.results["human_trafficking_scanner"]["status"] = "failed"
            self.results["human_trafficking_scanner"]["issues"].append(str(e))
            return False

    def test_enhanced_system_workflow(self):
        """Test the test enhanced system workflow"""
        logger.info("🧪 Testing enhanced system workflow...")

        try:
            # Test component imports
            from enhanced_platforms.aliexpress_scanner import AliExpressScanner
            from enhanced_platforms.taobao_scanner import TaobaoScanner
            from enhanced_platforms.enhanced_threat_scorer import EnhancedThreatScorer
            from enhanced_platforms.google_vision_controller import (
                GoogleVisionController,
            )
            from ultimate_wildguard_scanner import UltimateWildGuardScanner

            logger.info("✅ All enhanced system components imported")

            # Test multilingual keywords
            with open(
                "multilingual_wildlife_keywords.json", "r", encoding="utf-8"
            ) as f:
                data = json.load(f)

            keywords_by_language = data["keywords_by_language"]
            total_keywords = sum(len(words) for words in keywords_by_language.values())

            logger.info(f"✅ Languages: {len(keywords_by_language)}")
            logger.info(f"✅ Total keywords: {total_keywords:,}")

            # Test key languages
            key_languages = ["en", "zh", "es", "fr"]
            for lang in key_languages:
                if lang in keywords_by_language:
                    count = len(keywords_by_language[lang])
                    logger.info(f"✅ {lang}: {count} keywords")
                else:
                    logger.error(f"❌ Missing {lang} keywords")
                    return False

            self.results["test_enhanced_system"]["status"] = "passed"
            return True

        except Exception as e:
            logger.error(f"❌ Enhanced system test failed: {e}")
            self.results["test_enhanced_system"]["status"] = "failed"
            self.results["test_enhanced_system"]["issues"].append(str(e))
            return False

    def run_all_tests(self):
        """Run all tests"""
        logger.info("🚀 Starting GitHub Actions Workflow Tests")
        logger.info("=" * 60)

        tests = [
            ("File Existence", self.test_file_existence),
            ("Module Imports", self.test_imports),
            ("Environment Variables", self.test_environment_variables),
            ("Multilingual Keywords", self.test_multilingual_keywords),
            ("Enhanced Wildlife Scanner", self.test_enhanced_wildlife_scanner_workflow),
            ("Human Trafficking Scanner", self.test_human_trafficking_scanner_workflow),
            ("Test Enhanced System", self.test_enhanced_system_workflow),
        ]

        results = {}
        for test_name, test_func in tests:
            logger.info(f"\n📋 Running: {test_name}")
            logger.info("-" * 40)
            try:
                success = test_func()
                results[test_name] = success
                if success:
                    logger.info(f"✅ {test_name}: PASSED")
                else:
                    logger.error(f"❌ {test_name}: FAILED")
            except Exception as e:
                logger.error(f"❌ {test_name}: ERROR - {e}")
                results[test_name] = False

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 TEST SUMMARY")
        logger.info("=" * 60)

        passed = sum(1 for result in results.values() if result)
        total = len(results)

        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{test_name}: {status}")

        logger.info(f"\nOverall: {passed}/{total} tests passed")

        if passed == total:
            logger.info("🎉 All tests passed! GitHub Actions should work correctly.")
        else:
            logger.info("⚠️ Some tests failed. Check the issues above.")

        # Workflow-specific results
        logger.info("\n🔧 WORKFLOW-SPECIFIC RESULTS")
        logger.info("=" * 60)

        for workflow, result in self.results.items():
            status = result["status"]
            issues = result["issues"]
            logger.info(f"{workflow}: {status}")
            if issues:
                for issue in issues:
                    logger.info(f"  • {issue}")

        return results


def main():
    """Main function"""
    tester = GitHubActionsTester()
    results = tester.run_all_tests()

    # Save results to file
    with open("github_actions_test_results.json", "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "results": results,
                "workflow_results": tester.results,
            },
            f,
            indent=2,
        )

    logger.info(f"\n📄 Results saved to: github_actions_test_results.json")


if __name__ == "__main__":
    main()
