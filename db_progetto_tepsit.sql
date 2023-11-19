-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Nov 19, 2023 alle 20:56
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `progetto_tepsit`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `dipendenti`
--

CREATE TABLE `dipendenti` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `cognome` varchar(100) NOT NULL,
  `posizione_lavorativa` varchar(100) NOT NULL,
  `data_ass` date NOT NULL,
  `stipendio` float NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `dipendenti`
--

INSERT INTO `dipendenti` (`id`, `nome`, `cognome`, `posizione_lavorativa`, `data_ass`, `stipendio`, `email`) VALUES
(1, 'baggio', 'few', 'feefwf', '2005-05-31', 0, 'fewf'),
(7, 'baggios', 'il10', '', '0000-00-00', 0, '');

-- --------------------------------------------------------

--
-- Struttura della tabella `zone_di_lavoro`
--

CREATE TABLE `zone_di_lavoro` (
  `id_zona` int(11) NOT NULL,
  `nome_zona` varchar(100) NOT NULL,
  `numero_clienti` int(100) NOT NULL,
  `superficie` float NOT NULL,
  `id_dipendente` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `zone_di_lavoro`
--

INSERT INTO `zone_di_lavoro` (`id_zona`, `nome_zona`, `numero_clienti`, `superficie`, `id_dipendente`) VALUES
(1, 'nord', 22, 100, NULL);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `dipendenti`
--
ALTER TABLE `dipendenti`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `zone_di_lavoro`
--
ALTER TABLE `zone_di_lavoro`
  ADD PRIMARY KEY (`id_zona`),
  ADD KEY `id_dipendente` (`id_dipendente`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `dipendenti`
--
ALTER TABLE `dipendenti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT per la tabella `zone_di_lavoro`
--
ALTER TABLE `zone_di_lavoro`
  MODIFY `id_zona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `zone_di_lavoro`
--
ALTER TABLE `zone_di_lavoro`
  ADD CONSTRAINT `zone_di_lavoro_ibfk_1` FOREIGN KEY (`id_dipendente`) REFERENCES `dipendenti` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
