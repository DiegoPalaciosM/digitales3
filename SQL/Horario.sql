-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-11-2019 a las 18:34:46
-- Versión del servidor: 10.4.6-MariaDB
-- Versión de PHP: 7.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `Horario`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `uno`
--

CREATE TABLE `uno` (
  `ID` int(11) NOT NULL,
  `Clase` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `Lunes` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `LFin` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `Martes` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `MaFin` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `Miercoles` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `MiFin` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `Jueves` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `JuFin` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `Viernes` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `ViFin` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `Sabado` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `SaFin` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `Laboratorio` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `uno`
--

INSERT INTO `uno` (`ID`, `Clase`, `Lunes`, `LFin`, `Martes`, `MaFin`, `Miercoles`, `MiFin`, `Jueves`, `JuFin`, `Viernes`, `ViFin`, `Sabado`, `SaFin`, `Laboratorio`) VALUES
(1, 'Introduccion a la ingenieria Electronica', '17:34', '17:35', '08:00', '09:30', '10:00', '11:30', '12:00', '13:30', '14:00', '15:30', '03:29', '03:30', 'L5-Telecomunicaciones'),
(8, 'Introduccion a la ingenieria Electronica', '06:00', '07:30', '08:00', '09:30', '10:00', '11:30', '12:00', '13:30', '14:00', '15:30', '03:48', '03:49', 'L2-Industrial');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `uno_1`
--

CREATE TABLE `uno_1` (
  `ID` int(11) NOT NULL,
  `Clase` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'UwU',
  `Lunes` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Martes` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Miercoles` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Jueves` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Viernes` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Sabado` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Laboratorio` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `user` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `pass` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `apellido` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Edit` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `NFC` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No',
  `Super` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'No'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`ID`, `user`, `pass`, `nombre`, `apellido`, `Edit`, `NFC`, `Super`) VALUES
(4, 'adminn', 'adminn', 'Nadminn', 'Aadminn', 'No', 'Si', 'No'),
(5, 'adming', 'adming', 'Nadming', 'Aadming', 'Si', 'No', 'No'),
(6, 'mon', 'mon', 'Nmon', 'Amon', 'No', 'No', 'No'),
(7, 'admin', 'admin', 'Gintoki', 'Sataka', 'No', 'No', 'Si');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `uno`
--
ALTER TABLE `uno`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `uno_1`
--
ALTER TABLE `uno_1`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `uno`
--
ALTER TABLE `uno`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `uno_1`
--
ALTER TABLE `uno_1`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
