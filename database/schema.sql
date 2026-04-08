IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'proyecto_sena')
BEGIN
    CREATE DATABASE proyecto_sena;
END
GO

USE proyecto_sena;
GO

CREATE TABLE Usuario (
    codigoId INT PRIMARY KEY,
    tipoDocumento NVARCHAR(50) NOT NULL,
    numeroDocumento NVARCHAR(50) NOT NULL UNIQUE,
    nombreCompleto NVARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    sexo NVARCHAR(20) NOT NULL,
    direccionDomicilio NVARCHAR(100) NOT NULL,
    nickName NVARCHAR(50) NOT NULL UNIQUE,
    contrasena NVARCHAR(255) NOT NULL,
    tipoUsuario NVARCHAR(50) NOT NULL,
    nivel INT NOT NULL DEFAULT 1
);

CREATE TABLE Telefono (
    id INT PRIMARY KEY,
    usuarioId_FK INT NOT NULL,
    numero NVARCHAR(20) NOT NULL,
    tipo NVARCHAR(20) NOT NULL,
    CONSTRAINT FK_Telefono_Usuario FOREIGN KEY (usuarioId_FK) REFERENCES Usuario(codigoId)
);

CREATE TABLE RedSocial (
    id INT PRIMARY KEY,
    usuarioId_FK INT NOT NULL,
    plataforma NVARCHAR(50) NOT NULL,
    usuarioRed NVARCHAR(100) NOT NULL,
    CONSTRAINT FK_RedSocial_Usuario FOREIGN KEY (usuarioId_FK) REFERENCES Usuario(codigoId)
);

CREATE TABLE Plataforma (
    codigoId INT PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    marca NVARCHAR(100) NOT NULL
);

CREATE TABLE Juego (
    codigoId INT PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    calificacionESRB NVARCHAR(20) NOT NULL,
    estudioDesarrollador NVARCHAR(100) NOT NULL,
    numeroJugadores INT NOT NULL,
    tipo NVARCHAR(50) NOT NULL,
    totalExistencias INT NOT NULL
);

CREATE TABLE JuegoPlataforma (
    juegoId_FK INT NOT NULL,
    plataformaId_FK INT NOT NULL,
    CONSTRAINT PK_JuegoPlataforma PRIMARY KEY (juegoId_FK, plataformaId_FK),
    CONSTRAINT FK_JuegoPlataforma_Juego FOREIGN KEY (juegoId_FK) REFERENCES Juego(codigoId),
    CONSTRAINT FK_JuegoPlataforma_Plataforma FOREIGN KEY (plataformaId_FK) REFERENCES Plataforma(codigoId)
);

CREATE TABLE EquipoJuego (
    codigoId INT PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    horasJuego NVARCHAR(50) NOT NULL,
    nivelEquipo INT NOT NULL DEFAULT 1,
    puntosExperiencia INT NOT NULL DEFAULT 0,
    codigoJuego_FK INT NULL,
    CONSTRAINT FK_Equipo_Juego FOREIGN KEY (codigoJuego_FK) REFERENCES Juego(codigoId)
);

CREATE TABLE Atleta (
    codigoId INT PRIMARY KEY,
    puntosExperiencia INT NOT NULL DEFAULT 0,
    codigoEquipo_FK INT NULL,
    CONSTRAINT FK_Atleta_Usuario FOREIGN KEY (codigoId) REFERENCES Usuario(codigoId),
    CONSTRAINT FK_Atleta_Equipo FOREIGN KEY (codigoEquipo_FK) REFERENCES EquipoJuego(codigoId)
);

CREATE TABLE Arbitro (
    codigoId INT PRIMARY KEY,
    CONSTRAINT FK_Arbitro_Usuario FOREIGN KEY (codigoId) REFERENCES Usuario(codigoId)
);

CREATE TABLE Administrativo (
    codigoId INT PRIMARY KEY,
    CONSTRAINT FK_Administrativo_Usuario FOREIGN KEY (codigoId) REFERENCES Usuario(codigoId)
);

CREATE TABLE Proveedor (
    codigoId INT PRIMARY KEY,
    CONSTRAINT FK_Proveedor_Usuario FOREIGN KEY (codigoId) REFERENCES Usuario(codigoId)
);

CREATE TABLE AcudienteAtleta (
    codigoId INT PRIMARY KEY,
    codigoAtleta_FK INT NOT NULL UNIQUE,
    nombreCompleto NVARCHAR(150) NOT NULL,
    tipoDocumento NVARCHAR(50) NOT NULL,
    numeroDocumento NVARCHAR(50) NOT NULL,
    telefono NVARCHAR(20) NOT NULL,
    parentesco NVARCHAR(50) NOT NULL,
    direccion NVARCHAR(100) NOT NULL,
    CONSTRAINT FK_Acudiente_Atleta FOREIGN KEY (codigoAtleta_FK) REFERENCES Atleta(codigoId)
);

CREATE TABLE Trofeo (
    codigoId INT PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    puntos INT NOT NULL,
    codigoJuego_FK INT NULL,
    descripcion NVARCHAR(255) NULL,
    CONSTRAINT FK_Trofeo_Juego FOREIGN KEY (codigoJuego_FK) REFERENCES Juego(codigoId)
);

CREATE TABLE TrofeoUsuario (
    trofeoId_FK INT NOT NULL,
    usuarioId_FK INT NOT NULL,
    CONSTRAINT PK_TrofeoUsuario PRIMARY KEY (trofeoId_FK, usuarioId_FK),
    CONSTRAINT FK_TrofeoUsuario_Trofeo FOREIGN KEY (trofeoId_FK) REFERENCES Trofeo(codigoId),
    CONSTRAINT FK_TrofeoUsuario_Usuario FOREIGN KEY (usuarioId_FK) REFERENCES Usuario(codigoId)
);

CREATE TABLE TrofeoEquipo (
    trofeoId_FK INT NOT NULL,
    equipoId_FK INT NOT NULL,
    CONSTRAINT PK_TrofeoEquipo PRIMARY KEY (trofeoId_FK, equipoId_FK),
    CONSTRAINT FK_TrofeoEquipo_Trofeo FOREIGN KEY (trofeoId_FK) REFERENCES Trofeo(codigoId),
    CONSTRAINT FK_TrofeoEquipo_Equipo FOREIGN KEY (equipoId_FK) REFERENCES EquipoJuego(codigoId)
);

CREATE TABLE Consola (
    codigoId INT PRIMARY KEY,
    numeroSerie NVARCHAR(100) NOT NULL,
    nombre NVARCHAR(100) NOT NULL,
    cantidadDisponible INT NOT NULL,
    ip NVARCHAR(50) NOT NULL,
    macLan NVARCHAR(50) NOT NULL,
    macWifi NVARCHAR(50) NOT NULL,
    totalControles INT NOT NULL,
    codigoPlataforma_FK INT NOT NULL,
    CONSTRAINT FK_Consola_Plataforma FOREIGN KEY (codigoPlataforma_FK) REFERENCES Plataforma(codigoId)
);

CREATE TABLE Control (
    codigoId INT PRIMARY KEY,
    numeroSerie NVARCHAR(100) NOT NULL,
    tipo NVARCHAR(50) NOT NULL,
    codigoPlataforma_FK INT NOT NULL,
    CONSTRAINT FK_Control_Plataforma FOREIGN KEY (codigoPlataforma_FK) REFERENCES Plataforma(codigoId)
);

CREATE TABLE SesionEntrenamiento (
    codigoId INT PRIMARY KEY,
    fechaAgendamiento DATE NOT NULL,
    horaInicio TIME NOT NULL,
    horaFinalizacion TIME NOT NULL,
    estado NVARCHAR(50) NOT NULL,
    puntosExperiencia INT NOT NULL DEFAULT 0,
    codigoAtleta_FK INT NULL,
    codigoEquipo_FK INT NULL,
    codigoJuego_FK INT NULL,
    codigoArbitro_FK INT NULL,
    CONSTRAINT FK_Sesion_Atleta FOREIGN KEY (codigoAtleta_FK) REFERENCES Atleta(codigoId),
    CONSTRAINT FK_Sesion_Equipo FOREIGN KEY (codigoEquipo_FK) REFERENCES EquipoJuego(codigoId),
    CONSTRAINT FK_Sesion_Juego FOREIGN KEY (codigoJuego_FK) REFERENCES Juego(codigoId),
    CONSTRAINT FK_Sesion_Arbitro FOREIGN KEY (codigoArbitro_FK) REFERENCES Arbitro(codigoId),
    CONSTRAINT CK_Sesion_Objetivo CHECK (
        (codigoAtleta_FK IS NOT NULL AND codigoEquipo_FK IS NULL) OR
        (codigoAtleta_FK IS NULL AND codigoEquipo_FK IS NOT NULL)
    )
);
GO
