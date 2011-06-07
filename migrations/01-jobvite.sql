BEGIN;
CREATE TABLE `django_jobvite_category` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(100) NOT NULL,
    `slug` varchar(100) NOT NULL UNIQUE,
    `description` longtext NOT NULL
)
;
CREATE TABLE `django_jobvite_position_category` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `position_id` integer NOT NULL,
    `category_id` integer NOT NULL,
    UNIQUE (`position_id`, `category_id`)
)
;
ALTER TABLE `django_jobvite_position_category` ADD CONSTRAINT `category_id_refs_id_a673f532` FOREIGN KEY (`category_id`) REFERENCES `django_jobvite_category` (`id`);
CREATE TABLE `django_jobvite_position` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `job_id` varchar(25) NOT NULL,
    `title` varchar(100) NOT NULL,
    `requisition_id` integer UNSIGNED NOT NULL,
    `job_type` varchar(10) NOT NULL,
    `location` varchar(150) NOT NULL,
    `date` varchar(100) NOT NULL,
    `detail_url` varchar(200) NOT NULL,
    `apply_url` varchar(200) NOT NULL,
    `description` longtext NOT NULL,
    `brief_description` longtext
)
;
ALTER TABLE `django_jobvite_position_category` ADD CONSTRAINT `position_id_refs_id_bdc7c0e1` FOREIGN KEY (`position_id`) REFERENCES `django_jobvite_position` (`id`);
COMMIT;
