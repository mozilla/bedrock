# Install Node, NPM and LESS
# We DL and compile node manually.

class nodejs {

    package {
        ["python", "g++", "make"]:
            ensure => installed,
            require => Exec['update_apt']                
    } 

    file {'/src':
        ensure => directory,
        mode   => 0644,
    }    

    exec { "nodejs-download":
        command => "wget -N http://nodejs.org/dist/v0.10.13/node-v0.10.13.tar.gz",
        cwd     => "/src/", 
        timeout => 3600,
        unless => 'test -d /usr/local/bin/node', 
        require => [
            File['/src'],
        ];        
    }   

    exec { "nodejs-extract":
        command => "tar xzvf node-v0.10.13.tar.gz",
        cwd     => "/src/",         
        unless => 'test -d /usr/local/bin/node', 
        require => [
            File['/src'],
            Exec['nodejs-download']
        ];        
    }    

    exec { "nodejs-configure":
        command => "sudo ./configure",
        cwd     => "/src/node-v0.10.13/",  
        unless => 'test -d /usr/local/bin/node',      
        require => [
            File['/src'],
            Exec['nodejs-download'],
            Exec['nodejs-extract'] 
        ];          
    }  

    exec { "nodejs-install":
        command => "sudo make install",
        cwd     => "/src/node-v0.10.13/",
        timeout => 3600,
        unless => 'test -d /usr/local/bin/node',          
        require => [
            File['/src'],
            Exec['nodejs-download'],
            Exec['nodejs-extract'],
            Exec['nodejs-configure']
        ];         
          
    }                     
    
    #Install Less
    exec { "less-install":
        command => 'npm -g install less',
        unless => 'test -d /usr/local/bin/lessc',
        require => Exec['nodejs-install']  
    }         
  
}
