
module.exports = (app) => {
 
  const users = require('../controller/user.controller.js')

  // Create new
  app.post('/api/users', users.create)

  // Retrieve all
  app.get('/api/users', users.findAll)

  // Retrieve by Id
  app.get('/api/users/:userId', users.findByPk)

  // Update
  app.put('/api/users/:userId', users.update)

  // Delete
  app.delete('/api/users/:userId', users.delete)

  // Login
  app.post('/api/users/login', users.login)
}
