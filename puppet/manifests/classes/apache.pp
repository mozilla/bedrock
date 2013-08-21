# Install and configure apache.

class apache {
    
    package { "apache2":
        ensure => present,
        before => File['/etc/apache2/sites-enabled/mozilla-legacy.conf']; 
    }

    package { "libapache2-mod-php5":
        ensure => present,
        require => [
            Package['apache2']
        ];
    }            

    file { "/etc/apache2/sites-enabled/mozilla-legacy.conf":
        source => "$PROJ_DIR/puppet/files/etc/httpd/conf.d/mozilla-legacy.conf",
        owner => "root", group => "root", mode => 0644,
        require => [
            Package['apache2']
        ];
    }            

    exec {
        'a2enmod actions':
         onlyif => 'test ! -e /etc/apache2/mods-enabled/actions.load';
        'a2enmod expires':
         onlyif => 'test ! -e /etc/apache2/mods-enabled/expires.load';
        'a2enmod headers':
         onlyif => 'test ! -e /etc/apache2/mods-enabled/headers.load';
        'a2enmod proxy':
         onlyif => 'test ! -e /etc/apache2/mods-enabled/proxy.load';
        'a2enmod proxy_http':
         onlyif => 'test ! -e /etc/apache2/mods-enabled/proxy_http.load';
        'a2enmod rewrite':
         onlyif => 'test ! -e /etc/apache2/mods-enabled/rewrite.load';
        'a2enmod status':
         onlyif => 'test ! -e /etc/apache2/mods-enabled/status.load';
        'a2enmod vhost_alias':
         onlyif => 'test ! -e /etc/apache2/mods-enabled/vhost_alias.load';                                                                                                                                        
    }                     

    service { "apache2":
        ensure => running,
        enable => true,
        require => [
            Package['apache2'],
            File['/etc/apache2/sites-enabled/mozilla-legacy.conf'],
        ];
    }
        
}
