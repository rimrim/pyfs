import unittest

from fs.tempfs import TempFS
from fs.memoryfs import MemoryFS
from fs import utils

from six import b

class TestUtils(unittest.TestCase):

    def _make_fs(self, fs):
        fs.setcontents("f1", b("file 1"))
        fs.setcontents("f2", b("file 2"))
        fs.setcontents("f3", b("file 3"))
        fs.makedir("foo/bar", recursive=True)
        fs.setcontents("foo/bar/fruit", b("apple"))

    def _check_fs(self, fs):
        self.assertTrue(fs.isfile("f1"))
        self.assertTrue(fs.isfile("f2"))
        self.assertTrue(fs.isfile("f3"))
        self.assertTrue(fs.isdir("foo/bar"))
        self.assertTrue(fs.isfile("foo/bar/fruit"))
        self.assertEqual(fs.getcontents("f1", "rb"), b("file 1"))
        self.assertEqual(fs.getcontents("f2", "rb"), b("file 2"))
        self.assertEqual(fs.getcontents("f3", "rb"), b("file 3"))
        self.assertEqual(fs.getcontents("foo/bar/fruit", "rb"), b("apple"))

    def test_copydir_root(self):
        """Test copydir from root"""
        fs1 = MemoryFS()
        self._make_fs(fs1)
        fs2 = MemoryFS()
        utils.copydir(fs1, fs2)
        self._check_fs(fs2)

        fs1 = TempFS()
        self._make_fs(fs1)
        fs2 = TempFS()
        utils.copydir(fs1, fs2)
        self._check_fs(fs2)

    def test_copydir_indir(self):
        """Test copydir in a directory"""
        fs1 = MemoryFS()
        fs2 = MemoryFS()
        self._make_fs(fs1)
        utils.copydir(fs1, (fs2, "copy"))
        self._check_fs(fs2.opendir("copy"))

        fs1 = TempFS()
        fs2 = TempFS()
        self._make_fs(fs1)
        utils.copydir(fs1, (fs2, "copy"))
        self._check_fs(fs2.opendir("copy"))

    def test_movedir_indir(self):
        """Test movedir in a directory"""
        fs1 = MemoryFS()
        fs2 = MemoryFS()
        fs1sub = fs1.makeopendir("from")
        self._make_fs(fs1sub)
        utils.movedir((fs1, "from"), (fs2, "copy"))
        self.assertTrue(not fs1.exists("from"))
        self._check_fs(fs2.opendir("copy"))

        fs1 = TempFS()
        fs2 = TempFS()
        fs1sub = fs1.makeopendir("from")
        self._make_fs(fs1sub)
        utils.movedir((fs1, "from"), (fs2, "copy"))
        self.assertTrue(not fs1.exists("from"))
        self._check_fs(fs2.opendir("copy"))

    def test_movedir_root(self):
        """Test movedir to root dir"""
        fs1 = MemoryFS()
        fs2 = MemoryFS()
        fs1sub = fs1.makeopendir("from")
        self._make_fs(fs1sub)
        utils.movedir((fs1, "from"), fs2)
        self.assertTrue(not fs1.exists("from"))
        self._check_fs(fs2)

        fs1 = TempFS()
        fs2 = TempFS()
        fs1sub = fs1.makeopendir("from")
        self._make_fs(fs1sub)
        utils.movedir((fs1, "from"), fs2)
        self.assertTrue(not fs1.exists("from"))
        self._check_fs(fs2)

    def test_remove_all(self):
        """Test remove_all function"""
        fs = TempFS()
        fs.setcontents("f1", b("file 1"))
        fs.setcontents("f2", b("file 2"))
        fs.setcontents("f3", b("file 3"))
        fs.makedir("foo/bar", recursive=True)
        fs.setcontents("foo/bar/fruit", b("apple"))
        fs.setcontents("foo/baz", b("baz"))

        utils.remove_all(fs, "foo/bar")
        self.assertTrue(not fs.exists("foo/bar/fruit"))
        self.assertTrue(fs.exists("foo/bar"))
        self.assertTrue(fs.exists("foo/baz"))
        utils.remove_all(fs,  "")
        self.assertTrue(not fs.exists("foo/bar/fruit"))
        self.assertTrue(not fs.exists("foo/bar/baz"))
        self.assertTrue(not fs.exists("foo/baz"))
        self.assertTrue(not fs.exists("foo"))
        self.assertTrue(not fs.exists("f1"))
        self.assertTrue(fs.isdirempty('/'))


