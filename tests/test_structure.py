"""
HealthSim Hello - Basic Tests

These tests verify that the tutorial examples are properly structured.
They don't require the actual HealthSim packages to be installed.
"""

import pytest
from pathlib import Path


class TestDocumentation:
    """Tests for documentation completeness."""
    
    def test_readme_exists(self):
        """Test that README.md exists."""
        readme = Path(__file__).parent.parent / "README.md"
        assert readme.exists(), "README.md not found"
    
    def test_python_foundations_docs_exist(self):
        """Test that Python foundations docs exist."""
        docs_dir = Path(__file__).parent.parent / "docs" / "python-foundations"
        
        expected_files = [
            "virtual-environments.md",
            "pydantic-guide.md",
            "pytest-guide.md",
        ]
        
        for filename in expected_files:
            filepath = docs_dir / filename
            assert filepath.exists(), f"{filename} not found"
    
    def test_architecture_docs_exist(self):
        """Test that architecture docs exist."""
        docs_dir = Path(__file__).parent.parent / "docs" / "architecture"
        
        expected_files = [
            "platform-overview.md",
            "module-inventory.md",
        ]
        
        for filename in expected_files:
            filepath = docs_dir / filename
            assert filepath.exists(), f"{filename} not found"
    
    def test_tutorial_docs_exist(self):
        """Test that tutorial docs exist."""
        docs_dir = Path(__file__).parent.parent / "docs" / "tutorials"
        
        expected_files = [
            "environment-setup.md",
            "patientsim-tutorial.md",
            "membersim-tutorial.md",
        ]
        
        for filename in expected_files:
            filepath = docs_dir / filename
            assert filepath.exists(), f"{filename} not found"
    
    def test_interactive_docs_exist(self):
        """Test that interactive/MCP docs exist."""
        docs_dir = Path(__file__).parent.parent / "docs" / "interactive"
        
        expected_files = [
            "mcp-setup.md",
            "claude-desktop-config.md",
            "question-categories.md",
            "example-conversations.md",
        ]
        
        for filename in expected_files:
            filepath = docs_dir / filename
            assert filepath.exists(), f"{filename} not found"


class TestExamples:
    """Tests for example code files."""
    
    def test_patientsim_examples_exist(self):
        """Test that PatientSim examples exist."""
        examples_dir = Path(__file__).parent.parent / "examples" / "patientsim"
        
        expected_files = [
            "basic_generation.py",
            "fhir_export.py",
            "test_examples.py",
        ]
        
        for filename in expected_files:
            filepath = examples_dir / filename
            assert filepath.exists(), f"{filename} not found"
    
    def test_membersim_examples_exist(self):
        """Test that MemberSim examples exist."""
        examples_dir = Path(__file__).parent.parent / "examples" / "membersim"
        
        expected_files = [
            "basic_generation.py",
            "x12_export.py",
            "test_examples.py",
        ]
        
        for filename in expected_files:
            filepath = examples_dir / filename
            assert filepath.exists(), f"{filename} not found"


class TestProjectStructure:
    """Tests for project structure."""
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        pyproject = Path(__file__).parent.parent / "pyproject.toml"
        assert pyproject.exists(), "pyproject.toml not found"
    
    def test_gitignore_exists(self):
        """Test that .gitignore exists."""
        gitignore = Path(__file__).parent.parent / ".gitignore"
        assert gitignore.exists(), ".gitignore not found"
    
    def test_directory_structure(self):
        """Test that expected directories exist."""
        root = Path(__file__).parent.parent
        
        expected_dirs = [
            "docs",
            "docs/python-foundations",
            "docs/architecture",
            "docs/tutorials",
            "docs/interactive",
            "examples",
            "examples/patientsim",
            "examples/membersim",
            "tests",
        ]
        
        for dirname in expected_dirs:
            dirpath = root / dirname
            assert dirpath.exists(), f"Directory {dirname} not found"
            assert dirpath.is_dir(), f"{dirname} is not a directory"


class TestDocContent:
    """Tests for documentation content quality."""
    
    def test_readme_has_links(self):
        """Test that README contains links to docs."""
        readme = Path(__file__).parent.parent / "README.md"
        content = readme.read_text()
        
        # Should link to key sections
        assert "python-foundations" in content
        assert "architecture" in content
        assert "tutorials" in content
        assert "interactive" in content
    
    def test_docs_not_empty(self):
        """Test that docs are not empty or placeholder."""
        docs_dir = Path(__file__).parent.parent / "docs"
        
        for md_file in docs_dir.rglob("*.md"):
            content = md_file.read_text()
            # Should have more than just a title
            assert len(content) > 500, f"{md_file.name} seems too short"
    
    def test_examples_have_main(self):
        """Test that example scripts have main functions."""
        examples_dir = Path(__file__).parent.parent / "examples"
        
        for py_file in examples_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue  # Skip test files
            if py_file.name == "__init__.py":
                continue  # Skip init files
                
            content = py_file.read_text()
            assert "def main()" in content, f"{py_file.name} missing main()"
            assert 'if __name__ == "__main__"' in content, \
                f"{py_file.name} missing if __name__ block"
