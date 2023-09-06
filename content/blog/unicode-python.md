+++
title = "Unicode, String Encodings, and Python"
date = "2022-09-01T11:20:59-07:00"
toc = true
tags = [
    "python"
]
+++

I've been working on the [cryptopals challenges](https://www.cryptopals.com/) and avoiding stock libraries, to learn more about string encodings and the `bytes` type in Python 3.
So here, we'll learn way more than we need to know about Unicode.

## Text as Unicode Strings

To work with **text data**, computers need to work with many different types of characters.
From all the world's languages to symbols to emojis, the list goes on.
Unicode[^unicode] is a specification that aims to give every character used in human texts its own unique and standard code.

Strings in Python 3 are **Unicode strings**[^python-2].
A Unicode string is sequence of Unicode **code points**.
A code point has an integer value between 0 and 0x10FFFF (1,114,111 in decimal).
A code point corresponds to a Unicode character in the Unicode specification.

Text data can be specified in Python with Unicode string literals:[^python-literal]

```py
assert "A unicode \u265E \N{BLACK CHESS KNIGHT}" == "A unicode ♞ ♞"
assert "string \u00f0 \xf0" == "string ð ð"
assert ord("♞") == 9822    # returns the decimal code point
assert chr(9822) == "♞"    # returns the UTF-8 character at the decimal code point
```

- `\u265E` is an escape sequence that takes four hex digits and returns a character,
- `\N{BLACK CHESS KNIGHT}` is an escape sequence that takes a character name,
- `\xf0` takes two hex digits.

`\u265E` is an escape sequence corresponding to the Unicode code point `U+265E`, which corresponds to the character ♞.

## Encoded Data as `bytes`

When writing a string to file or to memory, computers use an **encoding** to represent the characters as sequences of bits.
One way to encode a string into binary in Python is to use `str.encode`.
This method returns a [`bytes` type](https://docs.python.org/3.10/library/stdtypes.html?highlight=bytes#binary-sequence-types-bytes-bytearray-memoryview), which is meant for working with binary data.
For example:

```py
# Str to Bytes
assert "10100\u265E".encode("utf-8") == b"10100\xe2\x99\x9e"
```

We can think of the `bytes` string above as a representation of the bit string

```py
# Bytes to Binary String Representation
assert "".join(bin(x) for x in b"10100\xe2\x99\x9e") == "0b1100010b1100000b1100010b1100000b1100000b111000100b100110010b10011110"
```

(I did not remove the "b" to make each character's binary string easily distinguishable.
Also note the variable length of each bit string.)

UTF-8, used above, is one of the encodings of Unicode.[^utf-8]
The [built-in `open()`](https://docs.python.org/3.10/library/functions.html#open) often uses the UTF-8 encoding by default, but generally this depends on your [locale](<https://en.wikipedia.org/wiki/Locale_(computer_software)>).

The built-in `open()` can also be used to read data in its pure binary form, by using `mode='b'`.
This avoids passing the data through any decoding methods and allows for direct operation on the binary data.

Note that `bytes` can be specified with a string literal such as `b"L10"`, where `b` is followed by a string of ASCII characters or escape sequences (see the string literals specification for more[^python-literal-spec]).
This is also how `bytes` is represented when printed (which happens implicitly via the [`repr()` built-in](https://docs.python.org/3.10/library/functions.html#repr)).

```py
# Hex String to Bytes
assert bytes.fromhex("4c") == b"L"

# Bytes to Hex String
assert b"L".hex() == "4c"

# Integer to Bytes
assert (90).to_bytes(1, byteorder="big") == b"Z"

# Bytes to List of Integers (ASCII Int Codes)
assert list(b"L13") == [76, 49, 51]

# Bytes to Str
assert b"abcd".decode("utf-8") == b"abcd".decode("ascii") == str(b"abcd", "ascii") == "abcd"
```

The `bytes` type should not be confused with a string representation of an integer.[^string-representations]

## References

- A nice high-level introduction to Unicode (and plenty of further reading references) can be found in [Python Unicode HOWTO](https://docs.python.org/3/howto/unicode.html).

## Footnotes

[^python-2]: Python [changed its handling of Unicode in a big way](https://docs.python.org/3.0/whatsnew/3.0.html#text-vs-data-instead-of-unicode-vs-8-bit) when moving from 2 to 3.
[^python-literal]:
    A Python literal is something that the parser interprets as syntax for writing an object directly.

    ```py
    # Python Literals
    "abcd"                              # text string
    b"\x00104"                          # byte string
    42, 4_2, 0x2A, 0b101010             # integer
    1.2e-14                             # float
    1 + 2.0j                            # complex
    True                                # bool
    None                                # None
    (1, 2)                              # tuple
    [1, 2]                              # list
    {1, 2}                              # set
    {1: 1, 2: 2}                        # dict
    ```

[^python-literal-spec]:
    [Python's literal spec](https://docs.python.org/3.10/reference/lexical_analysis.html#literals) for more details.
    These specifications may also be useful: [f-string Syntax](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) and [Format String Syntax](https://docs.python.org/3/library/string.html#formatstrings).

[^unicode]:
    You can see the 1062 common English Unicode characters [here](https://en.wikipedia.org/wiki/List_of_Unicode_characters#Basic_Latin).
    The full Unicode specification can be found [here](https://www.unicode.org/versions/Unicode14.0.0/#Summary).
    [See the wiki](https://en.wikipedia.org/wiki/Unicode) for some high level info.

[^utf-8]:
    [Here is a worked example](https://en.wikipedia.org/wiki/UTF-8#Examples) of how to encode the 3-byte euro sign €.
    While the string encodings (e.g. when using `str.encode`) can be any from [this list of standard encodings](https://docs.python.org/3.0/library/codecs.html#standard-encodings), UTF-8 is [the one you're most likely to encounter](https://w3techs.com/technologies/cross/character_encoding/ranking).

[^string-representations]:
    String representations of integers are just Python strings that represent integers using standard numerical systems.
    Here are few examples:

    ```py
    # String Representations of Integers
    assert bin(20) == "0b10100" == format(20, "#b") == "0b" + format(20, "b")
    assert hex(76) == "0x4c"
    assert int("0b10100", 2) == int("10100", 2) == 20
    assert int("0x4c", 16) == int("4c", 16) == 76
    ```
