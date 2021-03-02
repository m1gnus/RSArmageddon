# RSArmageddon

Smashing RSA for fun and profit

## Description

RSArmageddon is a free software project released under GPL-3.0 license
aiming to bring a powerful tool to attack the RSA cryptosystem and to
manage ciphertexts and keys.

Many common attacks are provided as part of the default package and new
ones can be added in an extensible fashion. Attacks are written in
Sage, an extension of the Python programming language providing improved
math capabilities and greater execution speed for computation-heavy
tasks.

## Installation

For Arch users, this software is easily installed from the [AUR][1]

```sh
$ yaourt -S rsarmageddon
```

Packages will be provided for Ubuntu/Debian and Windows in the
[releases][5] section of the GitHub page.

A python package is available on [PyPI][2] for installation through pip
on unsupported systems (but Sage has to be installed manually, see
section [Sage](#Sage)

```sh
$ pip install rsarmageddon
```

The main python script can also be used or installed straight out from a
clone of this repo, although using the provided packages is more
advisable.

## Sage

On UNIX and Linux a supported version of Sage (9.x) must be present in
the system's PATH. In case multiple versions are installed, the correct
one should be the first one found. When installing via one of the
provided packages this will generally be taken care of automatically.

Sometimes though Sage requires manual installation, such as when running
from a cloned repo or on Windows, when installing through pip, or on
\*nix systems that do not ship Sage 9.x in their official repositories
(confirmed on Debian version 10 and below). For these and more, see the
instructions in the next paragraphs.

In some situations, including when:

* running RSArmageddon from a cloned repo
* running RSArmageddon on Windows
* running RSArmageddon on \*nix systems that do not ship Sage 9.x
* installing RSArmageddon through pip

and others, Sage requires manual installation. See the instructions in
the next paragraphs for directions on how to do that.

### Installing Sage manually on Linux

There are many ways to install Sage on a Linux system, and some are
harder than others. First of all, you should check if a supported
version is available through your distro's package manager. The way to
do this will be different on every system, but as an example on Ubuntu
you would

```sh
$ sudo apt update && sudo apt install sagemath-common
```

Check with your distro for specific instructions. After installing
through your package manager, check that the version installed is
supported with:

```sh
$ sage -v
```

You should see something like `SageMath version 9.2, Release Date:
2020-10-24`. If your version is not in the 9.x series, it is advised to
uninstall it and try one of the other methods below.

On Debian 10, Sage 9 is currently unavailable in the stable
repositories. One option could be switching to Debian unstable, which at
the time of writing ships Sage 9.2. If you are willing to do so, you can
use the following commands to replace the contents of your
/etc/apt/sources.list (doing a backup first) and install Sage 9 while
upgrading your system to Debian unstable in the process

```sh
$ sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
$ echo 'deb http://deb.debian.org/debian/ sid main contrib non-free' | sudo tee /etc/apt/sources.list
$ echo 'deb-src http://deb.debian.org/debian/ sid main contrib non-free' | sudo tee -a /etc/apt/sources.list
$ sudo apt update && sudo apt dist-upgrade && sudo apt install sagemath
```

Your system should then be rebooted.

When a system package is not available, Sage must be installed from
upstream. You can follow the instructions found in the [official
guide][3], section 2.1.

### Installing Sage manually on Windows

Download and run one of the installers for the latest supported version
(9.x) from the [sage-windows][4] GitHub page. RSArmageddon should now be
able to find the Sage installation automatically.

## Usage examples

Crack a key vulnerable to Wiener factorization
```sh
$ rsarmageddon attack wiener -k examples/wiener.pub
```

Compute whole keys from partial information
```sh
$ rsarmageddon pem --dumpvalues -e 65537 -p 59324049994823056990807521915169702002197665897051782389894568149461077528733573161772021466179722704578809854939465445017077058505643271895926748239061359104208689455055208330141778200932280078304275269116573373683890335591263445317053081574622277328277733269675848414776648578497072273924489742291466663664728135782470217482641655776586326036779608751043056008882799192671053855818424895726100126833103213177923610642055953481374647391755694567628770583606826727132842668407118774498338841740271125482904779282687648543113216718032163573461465800663302702757738475592812012962616560400622190059897874533689263969513 -q 56214247180961101472418904084010866028721084750603538850912412988629938657856050506199747131481758687951394659255916498984648545468149966951075957118009649410947195509540243734626631437077632294920348877778126106857190799098500548702150792996731448944864546089813716649988246458024209115269339139700713248173765122394228136275663424166384192546495220986511506395231230712368557643028950758002822402061597625771649228811312719338006284781996960825317128843424255164212087586472800077894183144689764968774192993792706953206432004848853187269871408285302806880768934306325931793314083485686465813811090736334222919041553
```

Find and break keys from a set that share one or more factors with one another
```sh
$ rsarmageddon attack common_factor -k examples/common_factor --exts pem,pub -r --okd cracked_keys
```

Attack a key using two different methods with a timeout of 30 seconds each
```sh
$ rsarmageddon attack fermat,wiener -k examples/wiener.pub --timeout 30 --ok
```

Attack a key using all available methods with a timeout of 1 minute each
```sh
$ rsarmageddon attack all -k examples/fermat.pub --timeout 1m
```

Create a private key from e, p and q and print it to stdout in PEM format
```sh
$ rsarmageddon pem -e 65537 -p 12779877140635552275193974526927174906313992988726945426212616053383820179306398832891367199026816638983953765799977121840616466620283861630627224899026453 -q 12779877140635552275193974526927174906313992988726945426212616053383820179306398832891367199026816638983953765799977121840616466620283861630627224899027521 --cpr -
```

Factor a number using PARI
```sh
$ rsarmageddon factor 9837918379182
```

Encrypt the bytes string hello\_bob using the OAEP encryption standard
```sh
$ rsarmageddon encrypt --ptr hello_bob --std oaep -k examples/wiener.pub
```

## Attack scripts

RSArmageddon supports the execution of user-created attacks in an
extensible fashion. New attacks can be added to an RSArmageddon
installation by dropping their files in user-wide and system-wide
configuration directories. These are
`$XDG_CONFIG_HOME/rsarmageddon/attacks` and
`/usr/share/rsarmageddon/attacks` on \*nix systems, and
`%LOCALAPPDATA%\RSArmageddon\attacks` on Windows. System-wide attacks
will shadow builtin attacks of the same name, and user-wide attacks will
shadow both system-wide and builtin ones.

Attack files are Sage scripts written using RSArmageddon's attack API.
The name of the attack will be equal to the attack file's name with the
trailing `.sage` extension removed. To properly integrate with
RSArmageddon, every attack should:

* `import attack`
* Call `attack.init()` with the full attack name, and a shorthand name
  to use as prefix for multiple key outputs. This returns the `list`s of
  keys and of ciphertexts to work on, in a tuple. `attack.init` takes
  optional keyword arguments `min_keys` to specify the minimum number of
  keys the attack needs to work, `min_ciphertexts` for the minimum
  number of ciphertexts, and `deduplicate` which can be set to `"keys"`
  or `"ns"` to filter out wholly duplicate keys or multiple keys with
  the same public modulus.
* Get any user interaction by calling `attack.input`, which takes one
  optional argument `prompt` and two keyword arguments `default` and
  `validator`. `default` provides a default value that will be used if
  the user presses enter without writing anything; when `prompt` is set
  to a string, it will be displayed to the user when asking for input
  while also showing the default value if one is provided. `validator`
  takes a callable that can be used to validate and type convert user
  input before `attack.input` returns it; it should raise `ValueError`
  on malformed input.
* Proceed to execute the required key or ciphertext cracking operations
  leveraging the full computational and expressive power of Sage's math
  primitives, printing any useful or interesting informations along the
  way with `attack.info`, such as intermediate values and heuristics.
* Every time one or more private keys or cleartexts are found, call the
  `attack.keys` and `attack.cleartexts` to send them to RSArmageddon.
  `attack.keys` takes any number of 5-tuples or 6-tuples in the form
  `(n, e, d, p, q, [name])` with the optional 6th element being the key
  name, only used for multi-key outputs to override the default
  auto-generated key names. `attack.cleartexts` takes any number of
  integer cleartexts, or tuples in the form `(cleartext, name)` where
  `name` overrides the default cleartext name for multiple cleartext
  outputs in the same way as for keys.
* When the attack has done all it can to recover every possible key and
  cleartext, it should call `attack.success` or `attack.fail` to signal
  the outcome and terminate the script. `attack.fail` takes an optional
  message and a boolean keyword `bad_key` which signals RSArmageddon one
  of the keys the attack was given is invalid.

**Note:** Attacks may freely use any feature of the Python programming
language version 3.7 and of SageMath 9 but they should **not** interact
with the standard file descriptors directly (e.g. using the `print`
function to print data to standard output or `input` to get lines from
standard input), as those are reserved for use by the attack API, and
RSArmageddon makes no guarantee they will be connected to a terminal or
anything sensible at all. Remember to use `attack.info` and
`attack.input` for all user interactions instead.

**Note:** interactive input should generally be avoided because it
hinders RSArmageddon's ability to try out many consecutive attacks on a
given set of keys, basically brute-forcing the attack method while
running unsupervised.

**Note:** Should a multiprocessing Pool need to be created (to greatly
improve computational performance of parallelizable computing tasks on
multicore hardware), make sure to use the `attack.Pool` wrapper to
ensure signals are properly handled in the attack script's execution
environment.

[1]: https://aur.archlinux.org/
[2]: https://pypi.org/project/rsarmageddon/
[3]: https://doc.sagemath.org/pdf/en/installation/installation.pdf
[4]: https://github.com/sagemath/sage-windows/releases
[5]: https://github.com/m1gnus/RSArmageddon/releases
