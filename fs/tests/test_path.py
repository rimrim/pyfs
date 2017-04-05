"""

  fs.tests.test_path:  testcases for the fs path functions

"""


import unittest
import fs.tests

from fs.path import *

class TestPathFunctions(unittest.TestCase):
    """Testcases for FS path functions."""

    def test_normpath(self):
        tests = [   ("\\a\\b\\c", "\\a\\b\\c"),
                    (".", ""),
                    ("./", ""),
                    ("", ""),
                    ("/.", "/"),
                    ("/a/b/c", "/a/b/c"),
                    ("a/b/c", "a/b/c"),
                    ("a/b/../c/", "a/c"),
                    ("/","/"),
                    ("a/\N{GREEK SMALL LETTER BETA}/c","a/\N{GREEK SMALL LETTER BETA}/c"),
                    ]
        for path, result in tests:
            self.assertEqual(normpath(path), result)

    def test_pathjoin(self):
        tests = [   ("", "a", "a"),
                    ("a", "a", "a/a"),
                    ("a/b", "../c", "a/c"),
                    ("a/b/../c", "d", "a/c/d"),
                    ("/a/b/c", "d", "/a/b/c/d"),
                    ("/a/b/c", "../../../d", "/d"),
                    ("a", "b", "c", "a/b/c"),
                    ("a/b/c", "../d", "c", "a/b/d/c"),
                    ("a/b/c", "../d", "/a", "/a"),
                    ("aaa", "bbb/ccc", "aaa/bbb/ccc"),
                    ("aaa", "bbb\\ccc", "aaa/bbb\\ccc"),
                    ("aaa", "bbb", "ccc", "/aaa", "eee", "/aaa/eee"),
                    ("a/b", "./d", "e", "a/b/d/e"),
                    ("/", "/", "/"),
                    ("/", "", "/"),
                    ("a/\N{GREEK SMALL LETTER BETA}","c","a/\N{GREEK SMALL LETTER BETA}/c"),
        ]
        for testpaths in tests:
            paths = testpaths[:-1]
            result = testpaths[-1]
            self.assertEqual(pathjoin(*paths), result)

        self.assertRaises(ValueError, pathjoin, "..")
        self.assertRaises(ValueError, pathjoin, "../")
        self.assertRaises(ValueError, pathjoin, "/..")
        self.assertRaises(ValueError, pathjoin, "./../")
        self.assertRaises(ValueError, pathjoin, "a/b", "../../..")
        self.assertRaises(ValueError, pathjoin, "a/b/../../../d")

    def test_relpath(self):
        tests = [   ("/a/b", "a/b"),
                    ("a/b", "a/b"),
                    ("/", "") ]

        for path, result in tests:
            self.assertEqual(relpath(path), result)

    def test_abspath(self):
        tests = [   ("/a/b", "/a/b"),
                    ("a/b", "/a/b"),
                    ("/", "/") ]

        for path, result in tests:
            self.assertEqual(abspath(path), result)

    def test_iteratepath(self):
        tests = [   ("a/b", ["a", "b"]),
                    ("", [] ),
                    ("aaa/bbb/ccc", ["aaa", "bbb", "ccc"]),
                    ("a/b/c/../d", ["a", "b", "d"]) ]

        for path, results in tests:
            for path_component, expected in zip(iteratepath(path), results):
                self.assertEqual(path_component, expected)

        self.assertEqual(list(iteratepath("a/b/c/d", 1)), ["a", "b/c/d"])
        self.assertEqual(list(iteratepath("a/b/c/d", 2)), ["a", "b", "c/d"])

    def test_pathsplit(self):
        tests = [   ("a/b", ("a", "b")),
                    ("a/b/c", ("a/b", "c")),
                    ("a", ("", "a")),
                    ("", ("", "")),
                    ("/", ("/", "")),
                    ("/foo", ("/", "foo")),
                    ("foo/bar", ("foo", "bar")),
                    ("foo/bar/baz", ("foo/bar", "baz")),
                ]
        for path, result in tests:
            self.assertEqual(pathsplit(path), result)

    def test_recursepath(self):
        self.assertEqual(recursepath("/"),["/"])
        self.assertEqual(recursepath("hello"),["/","/hello"])
        self.assertEqual(recursepath("/hello/world/"),["/","/hello","/hello/world"])
        self.assertEqual(recursepath("/hello/world/",reverse=True),["/hello/world","/hello","/"])
        self.assertEqual(recursepath("hello",reverse=True),["/hello","/"])
        self.assertEqual(recursepath("",reverse=True),["/"])

    def test_isdotfile(self):
        for path in ['.foo',
                     '.svn',
                     'foo/.svn',
                     'foo/bar/.svn',
                     '/foo/.bar']:
            self.assertTrue(isdotfile(path))

        for path in ['asfoo',
                     'df.svn',
                     'foo/er.svn',
                     'foo/bar/test.txt',
                     '/foo/bar']:
            self.assertFalse(isdotfile(path))

    def test_dirname(self):
        tests = [('foo', ''),
                 ('foo/bar', 'foo'),
                 ('foo/bar/baz', 'foo/bar'),
                 ('/foo/bar', '/foo'),
                 ('/foo', '/'),
                 ('/', '/')]
        for path, test_dirname in tests:
            self.assertEqual(dirname(path), test_dirname)

    def test_basename(self):
        tests = [('foo', 'foo'),
                 ('foo/bar', 'bar'),
                 ('foo/bar/baz', 'baz'),
                 ('/', '')]
        for path, test_basename in tests:
            self.assertEqual(basename(path), test_basename)

    def test_iswildcard(self):
        self.assertTrue(iswildcard('*'))
        self.assertTrue(iswildcard('*.jpg'))
        self.assertTrue(iswildcard('foo/*'))
        self.assertTrue(iswildcard('foo/{}'))
        self.assertFalse(iswildcard('foo'))
        self.assertFalse(iswildcard('img.jpg'))
        self.assertFalse(iswildcard('foo/bar'))

    def test_realtivefrom(self):
        tests = [('/', '/foo.html', 'foo.html'),
                 ('/foo', '/foo/bar.html', 'bar.html'),
                 ('/foo/bar/', '/egg.html', '../../egg.html'),
                 ('/a/b/c/d', 'e', '../../../../e'),
                 ('/a/b/c/d', 'a/d', '../../../d'),
                 ('/docs/', 'tags/index.html', '../tags/index.html'),
                 ('foo/bar', 'baz/index.html', '../../baz/index.html'),
                 ('', 'a', 'a'),
                 ('a', 'b/c', '../b/c')
                 ]

        for base, path, result in tests:
            self.assertEqual(relativefrom(base, path), result)


class Test_PathMap(unittest.TestCase):

    def test_basics(self):
        map = PathMap()
        map["hello"] = "world"
        self.assertEqual(map["/hello"],"world")
        self.assertEqual(map["/hello/"],"world")
        self.assertEqual(map.get("hello"),"world")

    def test_iteration(self):
        map = PathMap()
        map["hello/world"] = 1
        map["hello/world/howareya"] = 2
        map["hello/world/iamfine"] = 3
        map["hello/kitty"] = 4
        map["hello/kitty/islame"] = 5
        map["batman/isawesome"] = 6
        self.assertEqual(set(map.keys()),set(("/hello/world","/hello/world/howareya","/hello/world/iamfine","/hello/kitty","/hello/kitty/islame","/batman/isawesome")))
        self.assertEqual(sorted(map.values()),list(range(1,7)))
        self.assertEqual(sorted(map.items("/hello/world/")),[("/hello/world",1),("/hello/world/howareya",2),("/hello/world/iamfine",3)])
        self.assertEqual(list(zip(list(map.keys()),list(map.values()))),list(map.items()))
        self.assertEqual(list(zip(map.keys("batman"),map.values("batman"))),map.items("batman"))
        self.assertEqual(set(map.iternames("hello")),set(("world","kitty")))
        self.assertEqual(set(map.iternames("/hello/kitty")),set(("islame",)))

        del map["hello/kitty/islame"]
        self.assertEqual(set(map.iternames("/hello/kitty")),set())
        self.assertEqual(set(map.keys()),set(("/hello/world","/hello/world/howareya","/hello/world/iamfine","/hello/kitty","/batman/isawesome")))
        self.assertEqual(set(map.values()),set(range(1,7)) - set((5,)))


