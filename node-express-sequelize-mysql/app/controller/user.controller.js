const db = require('../config/db.config.js')
const config = require('../config/env.js')
const User = db.users
const bcrypt = require('bcryptjs')
const jwt = require('jsonwebtoken')
 
exports.create = (req, res) => {	
	User.create({  
	  firstname: req.body.firstname,
	  lastname: req.body.lastname,
    email: req.body.email,
    password: bcrypt.hashSync(req.body.password, 8)
	}).then(user => {		
		res.send(user)
	})
}
 
exports.findAll = (req, res) => {
	User.findAll().then(users => {
	  res.send(users)
	})
}
 
exports.findByPk = (req, res) => {	
	User.findByPk(req.params.userId).then(user => {
		res.send(user)
	})
}
 
exports.update = (req, res) => {
  const id = req.params.userId
  
	User.update(
    { firstname: req.body.firstname,
      lastname: req.body.lastname,
      email: req.body.email,
			password: req.body.password
    },
	  { 
      where: {
        id: req.params.userId
      } 
    }
	).then(() => {
	  res.status(200).send("id " + id + " updated successfully")
	})
}
 
exports.delete = (req, res) => {
	const id = req.params.userId
	User.destroy({
	  where: { 
      id: id 
    }
	}).then(() => {
	  res.status(200).send("id " + id + " deleted successfully")
	})
}

exports.login = (req, res) => {
	User.findOne({
		where: {
			email: req.body.email
		}
	}).then(user => {
		if (!user) {
			return res.status(404).send('Email not found.');
		}

		let passwordIsValid = bcrypt.compareSync(req.body.password, user.password)
		if (!passwordIsValid) {
			return res.status(401).send({ auth: false, accessToken: null, reason: "Invalid Password!" })
		}

		let token = jwt.sign({ id: user.id }, config.JTW_SECRET, {
		  expiresIn: 86400 // expires in 24 hours
		})
		
		res.status(200).send({ auth: true, accessToken: token })
		
	}).catch(err => {
		res.status(500).send('Error: ' + err)
	})
}
