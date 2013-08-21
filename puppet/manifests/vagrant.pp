#
# Calls all the things to install all the things.
#

import "classes/*.pp"

$PROJ_DIR = "/vagrant"


Exec {
    path => "/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin",
}

class dev {
    class {
        init: before => Class[python];
        python: before => Class[apache];
        apache: before => Class[nodejs];
        nodejs: before => Class[custom];
        custom: ;        
    }
}

include dev
