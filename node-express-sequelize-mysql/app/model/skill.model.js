
module.exports = (sequelize, Sequelize) => {
	const Skill = sequelize.define('skill', {
	  skill: {
      type: Sequelize.STRING,
      allowNull: false
    },

    level: {
      type: Sequelize.INTEGER,
      allowNull: false
    },

    startDate: {
      type: Sequelize.DATE,
      allowNull: true
    }
  })

	return Skill
}
