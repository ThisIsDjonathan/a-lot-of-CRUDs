
const env = {
  database: 'cruddb',
  username: 'root',
  password: '',
  host: '127.0.0.1',
  dialect: 'mysql',
  pool: {
	  max: 5,
	  min: 0,
	  acquire: 30000,
	  idle: 10000
  },

  JTW_SECRET: 'jtw_super_key_secret_123456'
}
 
module.exports = env
