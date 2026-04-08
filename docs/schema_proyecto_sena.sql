-- =============================================
-- CREACION DE BASE DE DATOS
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'proyecto_sena')
BEGIN
    CREATE DATABASE proyecto_sena;
END
GO

USE proyecto_sena;
GO

-- =============================================
-- 1. TABLA NUCLEO: USUARIO
-- =============================================
CREATE TABLE Usuario (
    codigoId INT PRIMARY KEY,
    tipoDocumento NVARCHAR(50),
    numeroDocumento NVARCHAR(50),
    nombreCompleto NVARCHAR(100),
    edad INT,
    sexo NVARCHAR(20),
    comuna NVARCHAR(50),
    barrio NVARCHAR(50),
    direccionDomicilio NVARCHAR(100),
    nickName NVARCHAR(50),
    contrasena NVARCHAR(100),
    tipoUsuario NVARCHAR(50),
    contactoTelefono NVARCHAR(20),
    redSocial NVARCHAR(50)
);

-- =============================================
-- 2. TABLAS DE CATALOGO (JUEGOS Y PLATAFORMAS)
-- =============================================
CREATE TABLE Juego (
    codigoId INT PRIMARY KEY,
    nombre NVARCHAR(100),
    calificacionESRB NVARCHAR(20),
    estudioDesarrollador NVARCHAR(100),
    numeroJugadores INT,
    tipo NVARCHAR(50),
    totalExistencias INT
);

CREATE TABLE Plataforma (
    codigoId INT PRIMARY KEY,
    nombre NVARCHAR(100),
    marca NVARCHAR(100)
);

-- =============================================
-- 3. GESTION DE EQUIPOS
-- =============================================
CREATE TABLE EquipoJuego (
    codigoId INT PRIMARY KEY,
    nombre NVARCHAR(100),
    horasJuego NVARCHAR(50),
    nivelEquipo INT,
    codigoJuego_FK INT,
    CONSTRAINT FK_Equipo_Juego FOREIGN KEY (codigoJuego_FK) REFERENCES Juego(codigoId)
);

-- =============================================
-- 4. ESPECIALIZACION DE USUARIOS
-- =============================================
CREATE TABLE Atleta (
    codigoId INT PRIMARY KEY,
    puntosExperiencia INT,
    codigoEquipo_FK INT,
    CONSTRAINT FK_Atleta_Usuario FOREIGN KEY (codigoId) REFERENCES Usuario(codigoId),
    CONSTRAINT FK_Atleta_Equipo FOREIGN KEY (codigoEquipo_FK) REFERENCES EquipoJuego(codigoId)
);

CREATE TABLE Arbitro (
    codigoId INT PRIMARY KEY,
    CONSTRAINT FK_Arbitro_Usuario FOREIGN KEY (codigoId) REFERENCES Usuario(codigoId)
);

-- =============================================
-- 5. TRANSACCIONES: SESIONES DE ENTRENAMIENTO
-- =============================================
CREATE TABLE SesionEntrenamiento (
    codigoId INT PRIMARY KEY,
    fechaAgendamiento DATE,
    horaInicio TIME,
    horaFinalizacion TIME,
    estado NVARCHAR(50),
    puntosExperiencia INT,
    codigoAtleta_FK INT,
    codigoEquipo_FK INT,
    codigoJuego_FK INT,
    codigoArbitro_FK INT,
    CONSTRAINT FK_Sesion_Atleta FOREIGN KEY (codigoAtleta_FK) REFERENCES Atleta(codigoId),
    CONSTRAINT FK_Sesion_Equipo FOREIGN KEY (codigoEquipo_FK) REFERENCES EquipoJuego(codigoId),
    CONSTRAINT FK_Sesion_Juego FOREIGN KEY (codigoJuego_FK) REFERENCES Juego(codigoId),
    CONSTRAINT FK_Sesion_Arbitro FOREIGN KEY (codigoArbitro_FK) REFERENCES Arbitro(codigoId)
);

-- =============================================
-- 6. LOGROS Y RECOMPENSAS
-- =============================================
CREATE TABLE Trofeo (
    codigoId INT PRIMARY KEY,
    nombre NVARCHAR(100),
    puntos INT,
    codigoJuego_FK INT,
    codigoEquipo_FK INT,
    CONSTRAINT FK_Trofeo_Juego FOREIGN KEY (codigoJuego_FK) REFERENCES Juego(codigoId),
    CONSTRAINT FK_Trofeo_Equipo FOREIGN KEY (codigoEquipo_FK) REFERENCES EquipoJuego(codigoId)
);
GO
