workspace "Gry boty" "Model architektury C4" {

    !identifiers hierarchical

    model {
        user = person "Użytkownik"
	user_premium = person "Użytkownik Premium"
	admin = person "Superużytkownik (Admin)"
        system = softwareSystem "System do organizacji turniejów" {
            web_app_user = container "Aplikacja Webowa - Interfejs Użytkownika"{
		tags "Frontend"
	    } 
            database = container "Baza danych" {
                tags "Database"
            }
	    web_app_admin = container "Aplikacja Webowa - Interfejs Admina"{
		tags "Frontend"
	    }
            api_global = container "API"
	    
	    run = container "System do uruchamiania turniejów" {
		safe = component "Izolowane środowisko"
		logic = component "Moduł gry (logika)"
            }
        }
	user_premium -> system "Używa"
	user -> system "Używa"
	admin -> system "Zarządza"
	user_premium -> system.web_app_user "Wgrywa bota, bierze udział w turniejach, organizuje turnieje"
        user -> system.web_app_user "Wgrywa bota, bierze udział w turniejach"
	admin -> system.web_app_admin "Zarządza użytkownikami, turniejami"
        system.web_app_user -> system.api_global "Używa"
	system.api_global -> system.run "Wysyła"
	system.run.safe -> system.run.logic "Uruchamia"
	system.run -> system.database "Odczytuje i zapisuje"
	system.web_app_admin -> system.api_global "Używa"
    }

    views {
        systemContext system "Diagram1" {
            include *
            autolayout lr
        }

        container system "Diagram2" {
            include *
            autolayout lr
        }
	
	component system.run {
	    include *
	    autolayout lr
        }

        styles {
            element "Element" {
                color #ffffff
            }
            element "Person" {
                background #9b191f
                shape person
            }
            element "Software System" {
                background #ba1e25
            }
            element "Container" {
                background #d9232b
            }
            element "Database" {
                shape cylinder
            }
	    element "Frontend" {
		shape webbrowser
	    }
	    element "Sandbox" {
	        shape roundedbox   
		 }
	}
    }

    configuration {
        scope softwaresystem
	
    }

}
