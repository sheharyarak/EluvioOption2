const express = require('express')
const MongoClient = require('mongodb').MongoClient
const db = require('./config/db')
const bodyParser = require('body-parser')
const cluster = require('cluster')
// const numCPUs = require('os').cpus().length
const numCPUs = 4 // we want to use 2 cpus to respond

const app = express()

const port = 8000

app.use(bodyParser.urlencoded({extended: true}))

const uri = db.url

const client = new MongoClient(uri, {
	useNewUrlParser: true,
	useUnifiedTopology: true
})

if (cluster.isMaster) {

	var activeProcesses = 0
	function messageHandler(msg) {
		if (msg.cmd && msg.cmd === 'notifyRequest') {
		  activeProcesses += 1;
		  console.log(`new process:  activeProcesses = ${activeProcesses}`);
		}
	}


	console.log(`Master process ${process.pid} is running`)

	for (let i = 0; i < numCPUs; i++){
		cluster.fork()
	}

	for (const id in cluster.workers){
		cluster.workers[id].on('exit', ()=>{
			activeProcesses -= 1
			console.log(`exited process:  activeProcesses = ${activeProcesses}`);
		})
		cluster.workers[id].on('message', messageHandler);
	}

	cluster.on('exit', (worker, code, signal) => {
		console.log(`worker ${worker.process.pid} died`)
	})
} else {
	client.connect(err => {
		if (err) return console.error(err)
		const collection = client.db('testdb').collection('eluvio')
		require('./app/routes')(app, collection)
		app.listen(port, ()=> {
			process.send({ cmd: 'notifyRequest' });
			console.log(`${process.pid} is live on port ${port}`)
		})
	})
}

