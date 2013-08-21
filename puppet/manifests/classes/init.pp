# Commands to run before all others in puppet.

class init {
    group { "puppet":
        ensure => "present",
    }

    exec { "update_apt":
        command => "sudo apt-get update",
    }

    # Provides "add-apt-repository" command, useful if you need
    # to install software from other apt repositories.
    package { "python-software-properties":
        ensure => present,
        require => [
            Exec['update_apt'],
        ];
    }

    # LESSC & Installing Requirements Require Git
    package {
        ["git"]:
            ensure => installed;
    }    
        
}

