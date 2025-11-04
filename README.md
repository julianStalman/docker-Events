Aufgabenstellung: Fullstack Event-Tool
Projektbeschreibung
Entwicklung einer Fullstack-Webanwendung zur Verwaltung und Durchführung von Events. Die Anwendung richtet sich an drei Hauptnutzergruppen: Administratoren, Veranstalter und Besucher. Ziel ist es, eine Plattform bereitzustellen, auf der Events erstellt, verwaltet und besucht werden können. Besucher sollen Tickets kaufen können, Veranstalter ihre Events verwalten und Administratoren die gesamte Plattform kontrollieren.

Benutzerrollen
Administrator
Verwaltung aller Benutzergruppen
Einsicht und Kontrolle über alle Events und Ticketbestellungen
Veranstalter
Erstellung, Bearbeitung und Löschung eigener Events
Einsicht in Ticketbestellungen für eigene Events
Verwaltung von Eventdetails
Besucher
Anzeige von verfügbaren Events in Listen-/ Tabellenform
Möglichkeit zum Kauf von Tickets
Einsicht in eigene gekaufte Tickets
Funktionale Anforderungen
Eventverwaltung
Veranstalter können Events erstellen, bearbeiten und löschen
Events enthalten Titel, Beschreibung, Datum, Ort und Ticketanzahl
Events werden in Listen-/ Tabellenform angezeigt
Ticketverwaltung
Besucher können Tickets für Events kaufen
Gekaufte Tickets werden dem Benutzer zugeordnet
Tickets können storniert oder als gekauft markiert werden
Benutzerverwaltung
Administratoren können Benutzerrollen zuweisen und Benutzer verwalten
Rollenbasierte Zugriffskontrolle auf Funktionen und Daten
Anzeige und Interaktion
Eventlisten mit Filter- und Suchfunktion
Tabellenansicht für gekaufte Tickets
Detailansicht für einzelne Events mit Kaufoption (optional)
Nicht-funktionale Anforderungen
Sichere Authentifizierung und Autorisierung
Timeline
Sprint	Ziel & Meilensteine	Deliverables	Deadline
W0	Bootstrapping, Basis-Setup, Repo, venv, Alembic init, Linter/Formatter, pytest Setup	Initiales Projekt-Setup mit venv, Makefile, Alembic, pytest-Integration, Basis-Teststruktur (tests/-Ordner)	20.10
W1	UML-Klassendiagramm, DB-Entwurf	Klassendiagramm, ER-Abbild, erste Alembic-Migration	27.10
W2	SQLAlchemy-Models, Migrations, Seeds	Modelle (User, Role, Event, Ticket, ...), Migrationen, Seed-Daten	3.11
W3	Pydantic-Schemas, CRUD/Repos, Unit-Tests mit pytest	Create/Read/Update/Delete für Kern-Entities, Tests mit pytest (Fixtures, Mock-DB)	17.11
W4	Routen, Auth/JWT, RBAC, API-Tests	/auth, /events, /tickets, /orders, /admin; Rollen-Gates, pytest-Tests für Auth- und Rollenlogik	24.11
W5	Ticketkauf-Flow (Transaktionen), Suche, Integrationstests	Kauf/Reservierung mit Locking, Pagination, Such-/Filterparameter	15.12