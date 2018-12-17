
module.exports = (app) => {
 
  const controller = require('../controller/skill.controller.js')
  const auth = require('./verifyToken.js')

  // Create new
  app.post('/api/skills', auth.verifyToken, controller.create)

}
