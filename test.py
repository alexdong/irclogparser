#!/usr/bin/env python

import sys
import unittest
import doctest

from irclogparser import LogParser


def doctest_LogParser():
    r"""Tests for LogParser

    I'll define a helper function to test parsing.

        >>> def test(line):
        ...     for time, what, info in LogParser([line]):
        ...         print repr(time), what, repr(info)

    LogParser ignores empty lines

        >>> test('')
        >>> test('\n')
        >>> test('\r\n')

    All other lines result in a tuple (time, what, info)

        >>> test('14:18 * mg says Hello')
        '14:18' ACTION '* mg says Hello'

    Usually `info` is a string, but sometimes it is a tuple

        >>> test('14:18 <mg> Hello!')
        '14:18' COMMENT ('mg', 'Hello!')

    Newline characters are stripped from the line, if they are present

        >>> test('14:18 * mg says Hello\n')
        '14:18' ACTION '* mg says Hello'
        >>> test('14:18 * mg says Hello\r\n')
        '14:18' ACTION '* mg says Hello'
        >>> test('14:18 * mg says Hello\r')
        '14:18' ACTION '* mg says Hello'

    If there is no timestamp on the line, LogParser returns None

        >>> test('* mg says Hello')
        None ACTION '* mg says Hello'

    Several timestamp formats are recognized

        >>> test('14:18 <mg> Hello!')
        '14:18' COMMENT ('mg', 'Hello!')
        >>> test('[14:18] <mg> Hello!')
        '14:18' COMMENT ('mg', 'Hello!')
        >>> test('[14:18:55] <mg> Hello!')
        '14:18:55' COMMENT ('mg', 'Hello!')
        >>> test('[2004-02-04T14:18:55] <mg> Hello!')
        '2004-02-04T14:18:55' COMMENT ('mg', 'Hello!')
        >>> test('[02-Feb-2004 14:18:55] <mg> Hello!')
        '02-Feb-2004 14:18:55' COMMENT ('mg', 'Hello!')
        >>> test('[15 Jan 08:42] <mg> +++Hello+++')
        '15 Jan 08:42' COMMENT ('mg', '+++Hello+++')

    Excessive metainformation is stripped from nicknames

        >>> test('[15 Jan 08:42] <jsmith!n=jsmith@10.20.30.40> Hello!')
        '15 Jan 08:42' COMMENT ('jsmith', 'Hello!')

    `what` can be COMMENT...

        >>> test('<nick> text')
        None COMMENT ('nick', 'text')

    ...ACTION...

        >>> test('* nick text')
        None ACTION '* nick text'
        >>> test('*\tnick text')
        None ACTION '*\tnick text'

    ...JOIN...

        >>> test('*** someone joined #channel')
        None JOIN '*** someone joined #channel'
        >>> test('--> someone joined')
        None JOIN '--> someone joined'

    ...PART...

        >>> test('*** someone quit')
        None PART '*** someone quit'
        >>> test('<-- someone left #channel')
        None PART '<-- someone left #channel'

    ...NICKCHANGE...

        >>> test('*** X is now known as Y')
        None NICKCHANGE ('*** X is now known as Y', 'X', 'Y')
        >>> test('--- X are now known as Y')
        None NICKCHANGE ('--- X are now known as Y', 'X', 'Y')

    ...SERVER...

        >>> test('--- welcome to irc.example.org')
        None SERVER '--- welcome to irc.example.org'
        >>> test('*** welcome to irc.example.org')
        None SERVER '*** welcome to irc.example.org'

    All unrecognized lines are reported as OTHER

        >>> test('what is this line doing in my IRC log file?')
        None OTHER 'what is this line doing in my IRC log file?'

    """


def doctest_LogParser_dircproxy_support():
    r"""Tests for LogParser

    I'll define a helper function to test parsing.

        >>> def test(line):
        ...     for time, what, info in LogParser([line], dircproxy=True):
        ...         print repr(time), what, repr(info)

        >>> test('[15 Jan 08:42] <mg!n=user@10.0.0.1> -hmm')
        '15 Jan 08:42' COMMENT ('mg', 'hmm')
        >>> test('[15 Jan 08:42] <mg!n=user@10.0.0.1> +this')
        '15 Jan 08:42' COMMENT ('mg', 'this')
        >>> test('[15 Jan 08:42] <mg!n=user@10.0.0.1> maybe')
        '15 Jan 08:42' COMMENT ('mg', 'maybe')
        >>> test('[15 Jan 08:42] <mg!n=user@10.0.0.1> --1')
        '15 Jan 08:42' COMMENT ('mg', '-1')
        >>> test('[15 Jan 08:42] <mg!n=user@10.0.0.1> ++2')
        '15 Jan 08:42' COMMENT ('mg', '+2')
        >>> test('[15 Jan 08:42] <mg!n=user@10.0.0.1> +-3')
        '15 Jan 08:42' COMMENT ('mg', '-3')

    """


def doctest_LogParser_encodings():
    r"""Tests for LogParser

    I'll define a helper function to test parsing.

        >>> def test(line):
        ...     for time, what, info in LogParser([line]):
        ...         print repr(time), what, repr(info)

        >>> test('14:18 <mg> UTF-8: \xc4\x85')
        '14:18' COMMENT ('mg', u'UTF-8: \u0105')

        >>> test('14:18 <mg> cp1252: \x9a')
        '14:18' COMMENT ('mg', u'cp1252: \u0161')

    """

def test_suite():
    return unittest.TestSuite([
                doctest.DocTestSuite('irclogparser'),
                doctest.DocTestSuite()])

def main():
    unittest.main(defaultTest='test_suite')


if __name__ == '__main__':
    main()
