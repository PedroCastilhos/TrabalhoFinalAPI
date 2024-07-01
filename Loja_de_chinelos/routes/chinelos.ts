import { PrismaClient } from "@prisma/client"
import { Router } from "express"

import { verificaToken } from "../middlewares/verificaToken"

const prisma = new PrismaClient()

async function main() {
  prisma.$use(async (params, next) => {
    if (params.model == 'Chinelo') {
      if (params.action == 'delete') {
        params.action = 'update'
        params.args['data'] = { deleted: true }
      }
    }
    return next(params)
  })
}
main()

const router = Router()

router.get("/", async (req, res) => {
  try {
    const chinelos = await prisma.chinelo.findMany({
      where: { deleted: false }
    })
    res.status(200).json(chinelos)
  } catch (error) {
    res.status(400).json(error)
  }
})

router.post("/", verificaToken, async (req: any, res) => {
  const { marca, cor, tamanho, preco } = req.body
  const { userLogadoId } = req

  if (!marca || !cor || !tamanho || !preco) {
    res.status(400).json({ erro: "Informe marca, cor, tamanho e preco" })
    return
  }

  try {
    const chinelo = await prisma.chinelo.create({
      data: { marca, cor, tamanho, preco, usuarioId: userLogadoId }
    })

    await prisma.log.create({
      data: {
        descricao: "Chinelo criado",
        complemento: `Chinelo: ${marca} - ${cor}`,
        usuarioId: userLogadoId
      }
    })

    res.status(201).json(chinelo)
  } catch (error) {
    res.status(400).json(error)
  }
})

router.delete("/:id", verificaToken, async (req, res) => {
  const { id } = req.params
  const { userLogadoId } = req

  try {
    const chinelo = await prisma.chinelo.delete({
      where: { id: Number(id) }
    })

    await prisma.log.create({
      data: {
        descricao: "Chinelo excluído",
        complemento: `Chinelo ID: ${id}`,
        usuarioId: userLogadoId
      }
    })

    res.status(200).json(chinelo)
  } catch (error) {
    res.status(400).json(error)
  }
})

router.put("/:id", verificaToken, async (req, res) => {
  const { id } = req.params
  const { marca, cor, tamanho, preco } = req.body
  const { userLogadoId } = req

  if (!marca || !cor || !tamanho || !preco) {
    res.status(400).json({ erro: "Informe marca, cor, tamanho e preco" })
    return
  }

  try {
    const chinelo = await prisma.chinelo.update({
      where: { id: Number(id) },
      data: { marca, cor, tamanho, preco }
    })

    await prisma.log.create({
      data: {
        descricao: "Chinelo atualizado",
        complemento: `Chinelo ID: ${id}`,
        usuarioId: userLogadoId
      }
    })

    res.status(200).json(chinelo)
  } catch (error) {
    res.status(400).json(error)
  }
})

export default router
