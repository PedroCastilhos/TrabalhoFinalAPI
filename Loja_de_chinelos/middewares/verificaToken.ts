import jwt from "jsonwebtoken"
import { Request, Response, NextFunction } from 'express'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

interface TokenI {
  userLogadoId: number
  userLogadoNome: string
}

export function verificaToken(req: Request & { userLogadoId?: number, userLogadoNome?: string }, res: Response, next: NextFunction) {
  const { authorization } = req.headers

  if (!authorization) {
    res.status(401).json({ error: "Token não informado" })
    return
  }

  const token = authorization.split(" ")[1]

  try {
    const decode = jwt.verify(token, process.env.JWT_KEY as string) as TokenI
    const { userLogadoId, userLogadoNome } = decode

    req.userLogadoId = userLogadoId
    req.userLogadoNome = userLogadoNome

    next()
  } catch (error) {
    res.status(401).json({ error: "Token inválido" })
  }
}
