# RSArmageddon
<p>Tested OS:</p>
<ul>
    <li>Debian 10
    <li>Kali linux 2020.2
    <li>Arch linux
</ul>

<p>work in progress for Windows</p>

## How to install (Kali linux, Debian)

```
$ git clone https://github.com/m1gnus/RSArmageddon.git && cd RSArmageddon && ./setup_deb.sh
...
$ rsarmageddon

______  _____  ___                                      _     _             
| ___ \/  ___|/ _ \                                    | |   | |             
| |_/ /\ `--./ /_\ \_ __ _ __ ___   __ _  __ _  ___  __| | __| | ___  _ __  
|    /  `--. \  _  | '__| '_ ` _ \ / _` |/ _` |/ _ \/ _` |/ _` |/ _ \| '_ \ 
| |\ \ /\__/ / | | | |  | | | | | | (_| | (_| |  __/ (_| | (_| | (_) | | | |
\_| \_|\____/\_| |_/_|  |_| |_| |_|\__,_|\__, |\___|\__,_|\__,_|\___/|_| |_|
                                          __/ |                             
                                         |___/  

Written by M1gnus && Lotus -- PGIATASTI
                                                                            
```

## How to install (Arch)

```
$ git clone https://github.com/m1gnus/RSArmageddon.git && cd RSArmageddon && ./setup_arch.sh
...
$ rsarmageddon

______  _____  ___                                      _     _             
| ___ \/  ___|/ _ \                                    | |   | |             
| |_/ /\ `--./ /_\ \_ __ _ __ ___   __ _  __ _  ___  __| | __| | ___  _ __  
|    /  `--. \  _  | '__| '_ ` _ \ / _` |/ _` |/ _ \/ _` |/ _` |/ _ \| '_ \ 
| |\ \ /\__/ / | | | |  | | | | | | (_| | (_| |  __/ (_| | (_| | (_) | | | |
\_| \_|\____/\_| |_/_|  |_| |_| |_|\__,_|\__, |\___|\__,_|\__,_|\___/|_| |_|
                                          __/ |                             
                                         |___/  

Written by M1gnus && Lotus -- PGIATASTI
                                                                            
```

## See implemented attacks

```
$ rsarmageddon --show-attacks
```

## Attack Examples

```
$ rsarmageddon attack --publickey examples/wiener.pub --attack wiener --private --uncipher 0x0279daafa1eada3984429e9bd4b8860411d308d4862cabc9e638841753437e853442de4c15206caaf71c1537a2170d69f734ed54c93b5d0b09060c1a48ef880465424a098bf995edc06c10f64c22fee5aefd952f7c0bf2cf12133256dffbf9f2d6deba4e383ab6f09cb5973bf2a3f0d0fa6c639e1058a980b6493300e9704d53fb4c9970bb0d6194e51244af579ddf602d12b4a603ab051f17950ade2a8d2fc51703d7e40bbd73e4f0c07224cda14823c628921df0d34160680c90bd5fe7d0257ccfaf9d18bf7d2aef69a6c1207c5666fd2948559ba793cd8a014c37b723950faf6aa378057c0a2c6e961cba77e5d360827ad1aabc23df038d88a2b5dba43128f87183d2422d482443792ea788ccf29f2a5947a1c5095e20cceb5ed2c522cbad349dd763237865c311e5c140ecb53830711a9c39c809e10e7a7b86b514455d1b5b1b3154dca80b6fd5e1db00ebbfe1dfd8bbc917332c42e6d5437697fa102361d44d3e03f8b5bde08228f4219283670de748ddc97eefc68775fb8aa7faf84c0f353a6ca12b11f3eaac65c48c031ee9844ac64b7750d13de8ae161b1bb68a06d5e6f8b87e7a4f035ddcf9e326aedd51b7f019375bf747821abfb1ae2188d32ad337a69f78442b1d8a98a5097ec3b6db5c4f62994a1603e1ceb1bd76956471b57feb1d5ef84937eefe5eea2319cfa8b4418e6fe38d29b83f3b4ca63d6157c4449c78
```

```
$ rsarmageddon attack --attack common_factor --publickeydir examples/common_factor/ --ext pub --private
```

<font size=10>Please read the <a href="https://github.com/m1gnus/RSArmageddon/blob/master/RSArmageddon.pdf">User manual</a>.</font>
