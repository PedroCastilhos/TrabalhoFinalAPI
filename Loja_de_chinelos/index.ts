// index.ts
import express from 'express'
import cors from 'cors'

import chinelosRoutes from './routes/chinelos'
import usuariosRoutes from './routes/usuarios'
import loginRoutes from './routes/login'

const app = express()
const port = 3000

app.use(express.json())
app.use(cors())

app.use("/chinelos", chinelosRoutes)
app.use("/usuarios", usuariosRoutes)
app.use("/login", loginRoutes)

app.get('/', (req, res) => {
  res.send('API da Loja de Chinelos: Controle de Chinelos')
})

app.listen(port, () => {
  console.log(`Servidor rodando na porta: ${port}`)
})
