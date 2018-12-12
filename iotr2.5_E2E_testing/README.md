***************Itron-automated-test snap will check all E2E test*************************

#Command to install
$snap install itron-automated-test --devmode --dangerous

#To check
$snap list
core                      16-2.36.1      5898  stable    canonical✓  core
iotr2-automation          1.1            x3    -         -           devmode
iotr2-automation-testing  1.1            x3    -         -           devmode
itron-client              0+git.7edae9a  9     stable    korys.io    -
itron-edge                0+git.419548b  12    stable    korys.io    disabled
itron-gen4-fw             0+git.419548b  3     stable    korys.io    -
itron-ioter2              0+git.25811ff  x1    -         -           gadget
itron-ioter2-linux        0+git.d172009  x1    -         -           kernel

#Read the config var
$snap get itron-automated-test
Key                        Value
daily-excution-sleep-time  30
password                   XXXX
publickey                  XXXX
user-id                    XXXX


#Commands : 
1- systemctl status snap.iotr2-automation.daily-execution-test
2- journalctl -fu snap.iotr2-automation.daily-execution-test
3- snap stop iotr2-automation iotr2-automation.daily-execution-test
4- snap logs iotr2-automation
