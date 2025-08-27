/*
  Warnings:

  - You are about to drop the column `mode` on the `Draft` table. All the data in the column will be lost.
  - You are about to drop the column `style` on the `Draft` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "Draft" DROP COLUMN "mode",
DROP COLUMN "style";
