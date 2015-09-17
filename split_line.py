#!/usr/bin/env python3

import unittest

def split_line(line):
    """Splits a line up into individual arguments in a fashion similar to
       string.split(), but allowing for embedded spaces by using quotes.
    """
    arg = None
    args = []
    quote_char = None
    escape = False
    for ch in line:
        if escape:
            if ch == 'b':
                ch = '\b'
            elif ch == 'n':
                ch = '\n'
            elif ch == 'r':
                ch = '\r'
            elif ch == 't':
                ch = '\t'
            elif ch == '"' or ch == "'" or ch == '\\' or ch == ' ':
                pass
            elif ch == 'r':
                ch = '\r'
            else:
                ch = '\\' + ch
            escape = False
        else:
            if ch == '\\':
                escape = True
                continue
            if ch == quote_char:
                quote_char = None
                continue
            if quote_char is None:
                if (ch == "'" or ch == '"'):
                    quote_char = ch
                    if arg is None:
                        # This allows empty quotes to create an empty argument
                        arg = ''
                    continue
                if  ch.isspace():
                    if arg is not None:
                        args.append(arg)
                        arg = None
                    continue
        if arg is None:
            arg = ''
        arg += ch
    if arg is not None:
        args.append(arg)
    return args

TESTDATA = (
    ('', []),
    ('abc', ['abc']),
    ('This is a test', ['This', 'is', 'a', 'test']),
    ('This  is  a test', ['This', 'is', 'a', 'test']),
    ('a b c', ['a', 'b', 'c']),
    ('a  b  c', ['a', 'b', 'c']),
    ('a "b c" d', ['a', 'b c', 'd']),
    ('a "" d', ['a', '', 'd']),
    ("a '' d", ['a', '', 'd']),
    ("a b\\ c d", ['a', 'b c', 'd']),
    ("a 'b\\'c' d", ['a', "b'c", 'd']),
    ('a "b\\"c" d', ["a", 'b"c', 'd']),
    ('"\\b\\r\\n\\t\\\\"', ['\b\r\n\t\\']),
    ('\ta\tb\tc', ['a', 'b', 'c']),
)

class TestParser(unittest.TestCase):

    def __init__(self, line, expected_args):
        unittest.TestCase.__init__(self, 'parseTest')
        self.line = line
        self.expected_args = expected_args

    def parseTest(self):
        result = split_line(self.line)
        if result == self.expected_args:
            msg = ''
        else:
            msg = "For >>{}<< got >>{}<< expected >>{}<<".format(self.line, result, self.expected_args)
        self.assertEqual(result, self.expected_args, msg=msg)

def load_tests(loader, test, pattern):
    return unittest.TestSuite(TestParser(line, expected_args)
                              for line, expected_args in TESTDATA)


def test_input():
    """Manual testing function."""
    while True:
        try:
            line = input(">> ")
        except:
            break
        print("line = '%s'" % line)
        args = split_line(line)
        for i in range(len(args)):
            print("arg[%d] = '%s'" % (i, args[i]))
    print('')

if __name__ == "__main__":
    unittest.main()

