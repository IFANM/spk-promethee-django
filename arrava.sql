-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 25, 2022 at 06:06 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `arrava`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_candidate`
--

CREATE TABLE `account_candidate` (
  `id_candidate` varchar(3) NOT NULL,
  `nama_depan` varchar(25) DEFAULT NULL,
  `nama_belakang` varchar(25) DEFAULT NULL,
  `jenis_kelamin` varchar(25) NOT NULL,
  `tgl_lahir` date DEFAULT NULL,
  `no_telp` varchar(13) DEFAULT NULL,
  `alamat` longtext DEFAULT NULL,
  `foto_profil` varchar(100) NOT NULL,
  `cv` varchar(100) NOT NULL,
  `status` varchar(25) NOT NULL,
  `cand_mail_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `account_candidate`
--

INSERT INTO `account_candidate` (`id_candidate`, `nama_depan`, `nama_belakang`, `jenis_kelamin`, `tgl_lahir`, `no_telp`, `alamat`, `foto_profil`, `cv`, `status`, `cand_mail_id`) VALUES
('a01', 'Novi', 'Ekasari', 'laki-laki', '1991-01-04', '0987654321', 'Desa Rowo Indah, Kec. Ajung, Kab. Jember', 'a1_glCZCed.jpg', 'cv_SvuBkNp.pdf', 'seleksi', 8),
('a02', 'Miftahul', 'Arifin', 'laki-laki', '2003-02-15', '0987654321', 'rt.01/rw.01', 'a2_Mem5XXV.jpg', 'cv_TMvgUpi.pdf', 'seleksi', 9),
('a03', 'Nur', 'Khotimah', 'laki-laki', '2005-02-16', '0987654321', 'Desa Rowo Indah, Kec. Ajung, Kab. Jember', 'a3_Y1eHe4x.jpg', 'cv_4auMcHd.pdf', 'seleksi', 10),
('a04', 'Hendra', 'Setiawan', 'laki-laki', '2000-09-11', '0987654321', 'Desa Tegal Besar, Kec. Kaliwates, Kab. Jember', 'a4_JZu7Frt.jpg', 'cv_fZ9wf6Z.pdf', 'seleksi', 11),
('a05', 'Nurul', 'Azizah', 'laki-laki', '2004-04-15', '0987654321', 'Desa Tegal Besar, Kec. Kaliwates, Kab. Jember', 'a5_Bpic4ID.jpg', 'cv_SPE0R5Z.pdf', 'seleksi', 12);

-- --------------------------------------------------------

--
-- Table structure for table `account_users`
--

CREATE TABLE `account_users` (
  `id_user` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(25) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_leader` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `date_joined` datetime(6) DEFAULT NULL,
  `last_login` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `account_users`
--

INSERT INTO `account_users` (`id_user`, `password`, `email`, `is_active`, `is_leader`, `is_staff`, `is_superuser`, `date_joined`, `last_login`) VALUES
(1, 'pbkdf2_sha256$150000$kpU3I0UgJg3N$1M8smpSIx14SqOEVJa0Z09WuznQ4cevhr4YlaWEkogs=', 'admin@gmail.com', 1, 0, 1, 1, '2022-03-16 11:12:38.487003', '2022-07-10 08:18:38.123812'),
(2, 'pbkdf2_sha256$150000$HAyL7vGkq8Ei$35mUrdM/wI0VCQHTCDsKtaJu+qbAMtFWHZ6ell4ge+Y=', 'pimpinan@gmail.com', 1, 1, 0, 0, '2022-03-16 11:26:48.943584', '2022-07-10 08:18:54.057604'),
(8, 'pbkdf2_sha256$150000$bvOCjBNTL3LU$HIPKrVG0gskRyrXmkVxwMF9/QObFjkz4lIK5815HgPI=', 'pelamar1@gmail.com', 1, 0, 0, 0, '2022-06-30 06:11:59.064352', '2022-07-06 05:31:33.429029'),
(9, 'pbkdf2_sha256$150000$Iaad2Qp4FCvl$nP1Q8zKWGtcnCXRKdtEEEroD40fLqSaR/FOoPgDVzJA=', 'pelamar2@gmail.com', 1, 0, 0, 0, '2022-06-30 06:13:00.040478', '2022-06-30 06:13:00.040478'),
(10, 'pbkdf2_sha256$150000$PNlr14kP8s2P$scovfXZYRldSdcjiOswx9XvJs73Yvy3nlYPu+Frt4v0=', 'pelamar3@gmail.com', 1, 0, 0, 0, '2022-06-30 06:14:18.253909', '2022-06-30 06:14:18.253909'),
(11, 'pbkdf2_sha256$150000$ZbI5RQliAM4a$Hzfqq4RvKJZQyC2h6g/FWOZHskyHUqGq7mRHYLKjhLs=', 'pelamar4@gmail.com', 1, 0, 0, 0, '2022-06-30 06:15:12.738505', '2022-06-30 06:15:12.738505'),
(12, 'pbkdf2_sha256$150000$8csneqL8FZlq$uDruAMFrcn92IPe4cXeNVjsS7gOy41R8RvvE2GkiI7w=', 'pelamar5@gmail.com', 1, 0, 0, 0, '2022-06-30 06:30:55.678078', '2022-06-30 06:38:35.739707');

-- --------------------------------------------------------

--
-- Table structure for table `account_users_groups`
--

CREATE TABLE `account_users_groups` (
  `id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `account_users_user_permissions`
--

CREATE TABLE `account_users_user_permissions` (
  `id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add users', 6, 'add_users'),
(22, 'Can change users', 6, 'change_users'),
(23, 'Can delete users', 6, 'delete_users'),
(24, 'Can view users', 6, 'view_users'),
(25, 'Can add candidate', 7, 'add_candidate'),
(26, 'Can change candidate', 7, 'change_candidate'),
(27, 'Can delete candidate', 7, 'delete_candidate'),
(28, 'Can view candidate', 7, 'view_candidate'),
(29, 'Can add verify', 8, 'add_verify'),
(30, 'Can change verify', 8, 'change_verify'),
(31, 'Can delete verify', 8, 'delete_verify'),
(32, 'Can view verify', 8, 'view_verify'),
(33, 'Can add peringkat', 9, 'add_peringkat'),
(34, 'Can change peringkat', 9, 'change_peringkat'),
(35, 'Can delete peringkat', 9, 'delete_peringkat'),
(36, 'Can view peringkat', 9, 'view_peringkat'),
(37, 'Can add lowongan', 10, 'add_lowongan'),
(38, 'Can change lowongan', 10, 'change_lowongan'),
(39, 'Can delete lowongan', 10, 'delete_lowongan'),
(40, 'Can view lowongan', 10, 'view_lowongan'),
(41, 'Can add kriteria', 11, 'add_kriteria'),
(42, 'Can change kriteria', 11, 'change_kriteria'),
(43, 'Can delete kriteria', 11, 'delete_kriteria'),
(44, 'Can view kriteria', 11, 'view_kriteria'),
(45, 'Can add nilai', 12, 'add_nilai'),
(46, 'Can change nilai', 12, 'change_nilai'),
(47, 'Can delete nilai', 12, 'delete_nilai'),
(48, 'Can view nilai', 12, 'view_nilai');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2022-03-16 11:26:48.977789', '2', 'pimpinan@gmail.com', 1, '[{\"added\": {}}]', 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(7, 'account', 'candidate'),
(6, 'account', 'users'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(9, 'dss', 'peringkat'),
(8, 'dss', 'verify'),
(11, 'kriteria', 'kriteria'),
(10, 'lowongan', 'lowongan'),
(12, 'nilai', 'nilai'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2022-03-16 11:10:47.701995'),
(2, 'contenttypes', '0002_remove_content_type_name', '2022-03-16 11:10:49.139396'),
(3, 'auth', '0001_initial', '2022-03-16 11:10:50.686126'),
(4, 'auth', '0002_alter_permission_name_max_length', '2022-03-16 11:10:58.232457'),
(5, 'auth', '0003_alter_user_email_max_length', '2022-03-16 11:10:58.295011'),
(6, 'auth', '0004_alter_user_username_opts', '2022-03-16 11:10:58.451193'),
(7, 'auth', '0005_alter_user_last_login_null', '2022-03-16 11:10:58.529316'),
(8, 'auth', '0006_require_contenttypes_0002', '2022-03-16 11:10:58.591866'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2022-03-16 11:10:58.669948'),
(10, 'auth', '0008_alter_user_username_max_length', '2022-03-16 11:10:58.748068'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2022-03-16 11:10:58.794976'),
(12, 'auth', '0010_alter_group_name_max_length', '2022-03-16 11:10:59.044959'),
(13, 'auth', '0011_update_proxy_permissions', '2022-03-16 11:10:59.107455'),
(14, 'account', '0001_initial', '2022-03-16 11:11:02.388420'),
(15, 'admin', '0001_initial', '2022-03-16 11:11:15.684431'),
(16, 'admin', '0002_logentry_remove_auto_add', '2022-03-16 11:11:21.324612'),
(17, 'admin', '0003_logentry_add_action_flag_choices', '2022-03-16 11:11:21.496490'),
(18, 'admin', '0004_auto_20211224_1725', '2022-03-16 11:11:23.652572'),
(19, 'admin', '0005_auto_20211224_1731', '2022-03-16 11:11:25.886789'),
(20, 'dss', '0001_initial', '2022-03-16 11:11:28.059792'),
(21, 'kriteria', '0001_initial', '2022-03-16 11:11:32.106386'),
(22, 'lowongan', '0001_initial', '2022-03-16 11:11:32.825033'),
(23, 'nilai', '0001_initial', '2022-03-16 11:11:34.199954'),
(24, 'sessions', '0001_initial', '2022-03-16 11:11:38.918414');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('fp1dlqe4eg6d19o31lkt06u9lk97qhbp', 'M2M5YjNlMjMwYTY0OGJiNzdkZjA4YWY5OTFlN2JiYTQwYjdiYzczMzp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNTcyYWVhMTY1MWZlNDkwY2MzMDVlYWQxMDcwZDA4NzRhNDY5MzVlIn0=', '2022-04-01 06:41:56.531321');

-- --------------------------------------------------------

--
-- Table structure for table `dss_peringkat`
--

CREATE TABLE `dss_peringkat` (
  `id_peringkat` int(11) NOT NULL,
  `nilai_akhir` double DEFAULT NULL,
  `urutan` int(11) DEFAULT NULL,
  `nama_lengkap_id` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dss_peringkat`
--

INSERT INTO `dss_peringkat` (`id_peringkat`, `nilai_akhir`, `urutan`, `nama_lengkap_id`) VALUES
(31, 0.49, 1, 'a01'),
(32, 0.49, 2, 'a02'),
(33, -0.093333, 3, 'a03'),
(34, -0.229653, 4, 'a04'),
(35, -0.657014, 5, 'a05');

-- --------------------------------------------------------

--
-- Table structure for table `dss_verify`
--

CREATE TABLE `dss_verify` (
  `id_verify` int(11) NOT NULL,
  `verifikasi` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dss_verify`
--

INSERT INTO `dss_verify` (`id_verify`, `verifikasi`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `kriteria_kriteria`
--

CREATE TABLE `kriteria_kriteria` (
  `id_kriteria` varchar(3) NOT NULL,
  `nama_kriteria` varchar(25) DEFAULT NULL,
  `kaidah` varchar(10) DEFAULT NULL,
  `tipe_preferensi` varchar(25) DEFAULT NULL,
  `parameter_p` double DEFAULT NULL,
  `parameter_q` double DEFAULT NULL,
  `keterangan` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `kriteria_kriteria`
--

INSERT INTO `kriteria_kriteria` (`id_kriteria`, `nama_kriteria`, `kaidah`, `tipe_preferensi`, `parameter_p`, `parameter_q`, `keterangan`) VALUES
('k01', 'Nilai IPK', 'maksimasi', 'quasi', 0, 0.07, 'Nilai berkisar antara 0 hingga 100'),
('k02', 'Pengalaman Mengajar', 'maksimasi', 'quasi', 0, 2, 'Aturan kedua'),
('k03', 'Ujian Tulis', 'maksimasi', 'linear', 16, 0, 'Aturan ketiga'),
('k04', 'Ujian Wawancara', 'maksimasi', 'linear', 10, 0, 'Aturan keempat'),
('k05', 'Praktek Mengajar', 'maksimasi', 'linear', 9, 0, 'Aturan kelima');

-- --------------------------------------------------------

--
-- Table structure for table `lowongan_lowongan`
--

CREATE TABLE `lowongan_lowongan` (
  `id_lowongan` int(11) NOT NULL,
  `mata_pelajaran` varchar(25) NOT NULL,
  `jenjang` varchar(10) NOT NULL,
  `status` varchar(10) NOT NULL,
  `tgl_buka` date DEFAULT NULL,
  `tgl_tutup` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lowongan_lowongan`
--

INSERT INTO `lowongan_lowongan` (`id_lowongan`, `mata_pelajaran`, `jenjang`, `status`, `tgl_buka`, `tgl_tutup`) VALUES
(2, 'matematika', 'sd', 'dibuka', '2022-06-15', '2022-07-30');

-- --------------------------------------------------------

--
-- Table structure for table `nilai_nilai`
--

CREATE TABLE `nilai_nilai` (
  `id_nilai` int(11) NOT NULL,
  `nilai` double DEFAULT NULL,
  `nama_alternatif_id` varchar(3) NOT NULL,
  `nama_kriteria_id` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `nilai_nilai`
--

INSERT INTO `nilai_nilai` (`id_nilai`, `nilai`, `nama_alternatif_id`, `nama_kriteria_id`) VALUES
(40, 4, 'a01', 'k01'),
(41, 12, 'a01', 'k02'),
(42, 100, 'a01', 'k03'),
(43, 100, 'a01', 'k04'),
(44, 100, 'a01', 'k05'),
(45, 4, 'a02', 'k01'),
(46, 12, 'a02', 'k02'),
(47, 100, 'a02', 'k03'),
(48, 100, 'a02', 'k04'),
(49, 100, 'a02', 'k05'),
(50, 3.35, 'a03', 'k01'),
(51, 17, 'a03', 'k02'),
(52, 70, 'a03', 'k03'),
(53, 92, 'a03', 'k04'),
(54, 86, 'a03', 'k05'),
(55, 3.27, 'a04', 'k01'),
(56, 20, 'a04', 'k02'),
(57, 65, 'a04', 'k03'),
(58, 87, 'a04', 'k04'),
(59, 90, 'a04', 'k05'),
(60, 3.21, 'a05', 'k01'),
(61, 14, 'a05', 'k02'),
(62, 75, 'a05', 'k03'),
(63, 83, 'a05', 'k04'),
(64, 79, 'a05', 'k05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account_candidate`
--
ALTER TABLE `account_candidate`
  ADD PRIMARY KEY (`id_candidate`),
  ADD UNIQUE KEY `cand_mail_id` (`cand_mail_id`);

--
-- Indexes for table `account_users`
--
ALTER TABLE `account_users`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `account_users_groups`
--
ALTER TABLE `account_users_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_users_groups_users_id_group_id_64a581b4_uniq` (`users_id`,`group_id`),
  ADD KEY `account_users_groups_group_id_f8baf675_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `account_users_user_permissions`
--
ALTER TABLE `account_users_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_users_user_permi_users_id_permission_id_7816e12b_uniq` (`users_id`,`permission_id`),
  ADD KEY `account_users_user_p_permission_id_93dcf8b3_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_account_users_id_user` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `dss_peringkat`
--
ALTER TABLE `dss_peringkat`
  ADD PRIMARY KEY (`id_peringkat`),
  ADD KEY `dss_peringkat_nama_lengkap_id_99316b45_fk_account_c` (`nama_lengkap_id`);

--
-- Indexes for table `dss_verify`
--
ALTER TABLE `dss_verify`
  ADD PRIMARY KEY (`id_verify`);

--
-- Indexes for table `kriteria_kriteria`
--
ALTER TABLE `kriteria_kriteria`
  ADD PRIMARY KEY (`id_kriteria`);

--
-- Indexes for table `lowongan_lowongan`
--
ALTER TABLE `lowongan_lowongan`
  ADD PRIMARY KEY (`id_lowongan`);

--
-- Indexes for table `nilai_nilai`
--
ALTER TABLE `nilai_nilai`
  ADD PRIMARY KEY (`id_nilai`),
  ADD KEY `nilai_nilai_nama_alternatif_id_241fe2f7_fk_account_c` (`nama_alternatif_id`),
  ADD KEY `nilai_nilai_nama_kriteria_id_8f057fcb_fk_kriteria_` (`nama_kriteria_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account_users`
--
ALTER TABLE `account_users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `account_users_groups`
--
ALTER TABLE `account_users_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_users_user_permissions`
--
ALTER TABLE `account_users_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `dss_peringkat`
--
ALTER TABLE `dss_peringkat`
  MODIFY `id_peringkat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `dss_verify`
--
ALTER TABLE `dss_verify`
  MODIFY `id_verify` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `lowongan_lowongan`
--
ALTER TABLE `lowongan_lowongan`
  MODIFY `id_lowongan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `nilai_nilai`
--
ALTER TABLE `nilai_nilai`
  MODIFY `id_nilai` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account_candidate`
--
ALTER TABLE `account_candidate`
  ADD CONSTRAINT `account_candidate_cand_mail_id_915bbc1d_fk_account_users_id_user` FOREIGN KEY (`cand_mail_id`) REFERENCES `account_users` (`id_user`);

--
-- Constraints for table `account_users_groups`
--
ALTER TABLE `account_users_groups`
  ADD CONSTRAINT `account_users_groups_group_id_f8baf675_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `account_users_groups_users_id_42c8f507_fk_account_users_id_user` FOREIGN KEY (`users_id`) REFERENCES `account_users` (`id_user`);

--
-- Constraints for table `account_users_user_permissions`
--
ALTER TABLE `account_users_user_permissions`
  ADD CONSTRAINT `account_users_user_p_permission_id_93dcf8b3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `account_users_user_p_users_id_7136507e_fk_account_u` FOREIGN KEY (`users_id`) REFERENCES `account_users` (`id_user`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_account_users_id_user` FOREIGN KEY (`user_id`) REFERENCES `account_users` (`id_user`);

--
-- Constraints for table `dss_peringkat`
--
ALTER TABLE `dss_peringkat`
  ADD CONSTRAINT `dss_peringkat_nama_lengkap_id_99316b45_fk_account_c` FOREIGN KEY (`nama_lengkap_id`) REFERENCES `account_candidate` (`id_candidate`);

--
-- Constraints for table `nilai_nilai`
--
ALTER TABLE `nilai_nilai`
  ADD CONSTRAINT `nilai_nilai_nama_alternatif_id_241fe2f7_fk_account_c` FOREIGN KEY (`nama_alternatif_id`) REFERENCES `account_candidate` (`id_candidate`),
  ADD CONSTRAINT `nilai_nilai_nama_kriteria_id_8f057fcb_fk_kriteria_` FOREIGN KEY (`nama_kriteria_id`) REFERENCES `kriteria_kriteria` (`id_kriteria`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
