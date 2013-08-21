# Install python.

class python {

    package {
        ["python-dev", "libapache2-mod-wsgi", "python-pip", "libxml2-dev", "libxslt-dev"]:
            ensure => installed;
    }

    exec { "pip-install-compiled":
        command => "sudo pip install -r /vagrant/requirements/compiled.txt",
        require => Package['python-pip']
    }

    exec { "pip-install-dev":
        command => "sudo pip install -r /vagrant/requirements/dev.txt",
        timeout => 3600,
        require => [
            Package['python-pip'],
            Exec['pip-install-compiled']
        ];        
    }       
        
}
