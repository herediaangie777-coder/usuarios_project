USE proyecto_sena;
GO

INSERT INTO Plataforma (codigoId, nombre, marca) VALUES
(1, 'PC', 'Custom'),
(2, 'PlayStation 5', 'Sony'),
(3, 'Xbox Series X', 'Microsoft'),
(4, 'Nintendo Switch', 'Nintendo'),
(5, 'Mobile', 'Android');

INSERT INTO Juego (codigoId, nombre, calificacionESRB, estudioDesarrollador, numeroJugadores, tipo, totalExistencias) VALUES
(1, 'Valorant', 'T', 'Riot Games', 10, 'Digital', 20),
(2, 'League of Legends', 'T', 'Riot Games', 10, 'Digital', 20),
(3, 'EA Sports FC', 'E', 'EA Sports', 4, 'Fisico', 8),
(4, 'Rocket League', 'E', 'Psyonix', 8, 'Digital', 12),
(5, 'Fortnite', 'T', 'Epic Games', 100, 'Digital', 25);

INSERT INTO JuegoPlataforma (juegoId_FK, plataformaId_FK) VALUES
(1,1),(2,1),(3,2),(3,3),(4,1),(4,2),(4,3),(5,1),(5,5);

INSERT INTO Usuario (codigoId, tipoDocumento, numeroDocumento, nombreCompleto, edad, sexo, direccionDomicilio, nickName, contrasena, tipoUsuario, nivel) VALUES
(1,'CC','1001','Sara Mejia',17,'F','Ciudad del Rio 101','saraaim','hash1','atleta',1),
(2,'CC','1002','Juan Toro',19,'M','Ciudad del Rio 102','juantop','hash2','atleta',2),
(3,'CC','1003','Laura Gil',22,'F','Ciudad del Rio 103','laurajuez','hash3','arbitro',1),
(4,'CC','1004','Andres Mesa',28,'M','Ciudad del Rio 104','amesa','hash4','administrativo',1),
(5,'CC','1005','Carlos Ruiz',31,'M','Ciudad del Rio 105','cruizprov','hash5','proveedor',1),
(6,'CC','1006','Mateo Arango',16,'M','Ciudad del Rio 106','mateoarc','hash6','atleta',1),
(7,'CC','1007','Paula Velez',24,'F','Ciudad del Rio 107','paularef','hash7','arbitro',1);

INSERT INTO Telefono (id, usuarioId_FK, numero, tipo) VALUES
(1,1,'3000000001','Movil'),
(2,2,'3000000002','Movil'),
(3,3,'3000000003','Movil'),
(4,4,'3000000004','Trabajo'),
(5,5,'3000000005','Trabajo');

INSERT INTO RedSocial (id, usuarioId_FK, plataforma, usuarioRed) VALUES
(1,1,'Discord','saraaim#1001'),
(2,2,'Discord','juantop#1002'),
(3,3,'Discord','laurajuez#1003'),
(4,6,'Instagram','mateoarc'),
(5,7,'Discord','paularef#1007');

INSERT INTO EquipoJuego (codigoId, nombre, horasJuego, nivelEquipo, puntosExperiencia, codigoJuego_FK) VALUES
(1,'Phoenix Core','12',3,240,1),
(2,'Dragon Rift','10',2,180,2),
(3,'Turbo Squad','8',2,160,3),
(4,'Orbit Racers','9',2,150,4),
(5,'Storm Drop','11',3,260,5);

INSERT INTO Atleta (codigoId, puntosExperiencia, codigoEquipo_FK) VALUES
(1,90,1),
(2,150,2),
(6,70,1);

INSERT INTO Arbitro (codigoId) VALUES
(3),(7);

INSERT INTO Administrativo (codigoId) VALUES
(4);

INSERT INTO Proveedor (codigoId) VALUES
(5);

INSERT INTO AcudienteAtleta (codigoId, codigoAtleta_FK, nombreCompleto, tipoDocumento, numeroDocumento, telefono, parentesco, direccion) VALUES
(1,1,'Marta Mejia','CC','9001','3111111111','Madre','Ciudad del Rio 201'),
(2,6,'Luis Arango','CC','9002','3222222222','Padre','Ciudad del Rio 202');

INSERT INTO Trofeo (codigoId, nombre, puntos, codigoJuego_FK, descripcion) VALUES
(1,'Arranque Perfecto',40,1,'Trofeo inicial de practica'),
(2,'Macro Maestro',60,2,'Coordinacion tactica'),
(3,'Gol de Oro',50,3,'Precision ofensiva'),
(4,'Aereo Supremo',70,4,'Dominio mecanico'),
(5,'Ultimo Circulo',80,5,'Supervivencia y cierre');

INSERT INTO TrofeoUsuario (trofeoId_FK, usuarioId_FK) VALUES
(1,1),(2,2),(4,2),(5,6),(3,1);

INSERT INTO TrofeoEquipo (trofeoId_FK, equipoId_FK) VALUES
(1,1),(2,2),(3,3),(4,4),(5,5);

INSERT INTO Consola (codigoId, numeroSerie, nombre, cantidadDisponible, ip, macLan, macWifi, totalControles, codigoPlataforma_FK) VALUES
(1,'PS5-001','Play 1',3,'192.168.1.10','AA-BB-CC-10','AA-BB-CC-11',2,2),
(2,'XBX-001','Xbox 1',2,'192.168.1.20','AA-BB-CC-20','AA-BB-CC-21',2,3),
(3,'SWI-001','Switch 1',4,'192.168.1.30','AA-BB-CC-30','AA-BB-CC-31',4,4),
(4,'PC-001','Arena PC 1',10,'192.168.1.40','AA-BB-CC-40','AA-BB-CC-41',4,1),
(5,'PC-002','Arena PC 2',10,'192.168.1.41','AA-BB-CC-42','AA-BB-CC-43',4,1);

INSERT INTO Control (codigoId, numeroSerie, tipo, codigoPlataforma_FK) VALUES
(1,'CTRL-001','Gamepad',2),
(2,'CTRL-002','Gamepad',3),
(3,'CTRL-003','JoyCon',4),
(4,'CTRL-004','Teclado',1),
(5,'CTRL-005','Mouse',1);

INSERT INTO SesionEntrenamiento (codigoId, fechaAgendamiento, horaInicio, horaFinalizacion, estado, puntosExperiencia, codigoAtleta_FK, codigoEquipo_FK, codigoJuego_FK, codigoArbitro_FK) VALUES
(1,'2026-04-01','08:00','10:00','cerrada',60,1,NULL,1,3),
(2,'2026-04-02','10:00','11:30','cerrada',50,2,NULL,2,3),
(3,'2026-04-03','14:00','16:00','programada',0,NULL,1,1,7),
(4,'2026-04-04','09:00','10:30','en curso',0,NULL,2,2,7),
(5,'2026-04-05','15:00','17:00','cancelada',0,6,NULL,5,3);
GO
