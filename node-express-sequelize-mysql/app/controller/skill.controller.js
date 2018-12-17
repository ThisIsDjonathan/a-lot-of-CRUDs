const db = require('../config/db.config.js')
const Skill = db.skills
 
exports.create = (req, res) => {
	Skill.create({  
	  skill: req.body.skill,
	  level: req.body.level,
    startDate: req.body.startDate,
    userId: req.body.userId
	}).then(skill => {		
		res.send(skill)
  })
}
