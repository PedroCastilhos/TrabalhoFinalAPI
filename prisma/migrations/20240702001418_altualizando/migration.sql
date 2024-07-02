/*
  Warnings:

  - Added the required column `nome` to the `usuarios` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE `usuarios` ADD COLUMN `nome` VARCHAR(60) NOT NULL;
