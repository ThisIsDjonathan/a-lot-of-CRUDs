module.exports = (sequelize, Sequelize) => {
	const User = sequelize.define('user', {
	  firstname: {
      type: Sequelize.STRING,
      allowNull: false,
      validate: {
        len: {
          args: [0, 50], 
          msg: 'This field cannot exceed 50 characters.'
        }
      }
    },
    
	  lastname: {
      type: Sequelize.STRING,
      allowNull: false,
      validate: {
        len: {
          args: [0, 50], 
          msg: 'This field cannot exceed 50 characters.'
        }
      }
    },
    
	  email: {
      type: Sequelize.STRING,
      allowNull: false,
      unique: {
        args: true,
        msg: 'Email already exists.'
      },
      validate: {
        isEmail: {
          msg: 'This field has to be an email.'
        }
      }
    },

    password: {
      type: Sequelize.STRING,
      allowNull: false
    }
  })

	return User
}
