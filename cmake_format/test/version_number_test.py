import json
import os
import re
import unittest


class TestVersionNumber(unittest.TestCase):
  """
  Verify that various documentation and configuration files are all using the
  same version number.
  """

  def __init__(self, *args):
    super(TestVersionNumber, self).__init__(*args)
    self.init_version = None
    self.repodir = None

  def setUp(self):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(thisdir)
    self.repodir = os.path.dirname(parent)
    with open(os.path.join(parent, "__init__.py")) as infile:
      initpy = infile.read()
    match = re.search("VERSION = ['\"]([^'\"]+)['\"]", initpy)
    if not match:
      self.fail("No version in __init__.py")
      return
    parts = match.group(1).split(".")
    self.init_version = ".".join(parts[:3])

  def test_install_documentation(self):
    filepath = os.path.join(self.repodir, "cmake_format/doc/installation.rst")
    with open(filepath) as infile:
      content = infile.read()

    match = re.search(r"pip install v(\S+).tar.gz", content)
    if not match:
      self.fail("Couldn't find 'pip install' in installation.rst")
      return

    self.assertEqual(self.init_version, match.group(1))

  def test_precommit_documentation(self):
    filepath = os.path.join(self.repodir, "cmake_format/doc/installation.rst")
    with open(filepath) as infile:
      content = infile.read()

    match = re.search(r"rev: v(\S+)", content)
    if not match:
      self.fail("Couldn't find 'rev:' in installation.rst")
      return

    self.assertEqual(self.init_version, match.group(1))

  def test_vscode_package_json(self):
    filepath = os.path.join(
        self.repodir, "cmake_format/vscode_extension/package.json")
    with open(filepath) as infile:
      data = json.load(infile)

    self.assertIn("version", data)
    self.assertEqual(data["version"], self.init_version)

  def test_vscode_packagelock_json(self):
    filepath = os.path.join(
        self.repodir, "cmake_format/vscode_extension/package.json")
    with open(filepath) as infile:
      data = json.load(infile)

    self.assertIn("version", data)
    self.assertEqual(data["version"], self.init_version)

  def test_changelog(self):
    """
    Ensure that the changelog includes an section for this version
    """
    version_str = "v" + self.init_version
    hruler = '-' * len(version_str)
    expect_str = version_str + "\n" + hruler

    filepath = os.path.join(
        self.repodir, "cmake_format/doc/changelog.rst")
    with open(filepath) as infile:
      content = infile.read()
    self.assertIn(expect_str, content)

  def test_relnotes(self):
    """
    Ensure that the release notes includes an section for this version
    """
    version_str = "v" + self.init_version
    hruler = '-' * len(version_str)
    expect_str = hruler + "\n" + version_str + "\n" + hruler

    filepath = os.path.join(
        self.repodir, "cmake_format/doc/release_notes.rst")
    with open(filepath) as infile:
      content = infile.read()
    self.assertIn(expect_str, content)


if __name__ == "__main__":
  unittest.main()
