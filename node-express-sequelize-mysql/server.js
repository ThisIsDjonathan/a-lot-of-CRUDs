const express = require ('express')
const bodyParser = require('body-parser')
const db = require('./app/config/db.config.js')

const app = express()
app.use(bodyParser.urlencoded({ extended: true }))

// force: true will drop the table if it already exists
db.sequelize.sync({force: true}).then(() => {
  console.log('Drop and Resync with { force: true }')
})

require('./app/route/user.route.js')(app)
require('./app/route/skill.route.js')(app)

// Start server
let server = app.listen(8081, function () { 
  let host = server.address().address
  let port = server.address().port
 
  console.log("Server is running and listening at http://%s:%s", host, port)
})
