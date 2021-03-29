var ObjectID = require('mongodb').ObjectID

module.exports = function(app, collection) {
	app.get('/:id', (req, res) => {
		const id = req.params.id
		const details = {
			'_id' : new ObjectID(id)
		}
		collection.findOne(details, (err, item) => {
			if (err) {
				res.send({
					'error':'the following error has occured.\n' + err.toString()
				})
			} else {
				res.send(item)
			}
		})
	})

	app.post('/', (req, res) => {
		const item = {
			name: req.body.name,
			description: req.body.description
		}
		collection.insertOne(item, (err, success) => {
			if (err) {
				res.send({
					'error':'the following error has occured.\n' + err.toString()
				})
			} else {
				res.send(success.ops[0])
			}
		})
	})

	app.delete('/:id', (req, res) => {
		const id = req.params.id
		const details = {
			'_id' : new ObjectID(id)
		}
		collection.deleteOne(details, (err, item) => {
			if (err) {
				res.send({
					'error':'the following error has occured.\n' + err.toString()
				})
			} else {
				res.send('Item ' + id + ' was deleted.')
			}
		})
	})

	app.put('/:id', (req, res) => {
		const id = req.params.id
		const details = {
			'_id' : new ObjectID(id)
		}
		const changes = {
			name: req.body.name,
			description: req.body.description
		}
		collection.updateOne(details, {$set : changes}, (err, item) => {
			if (err) {
				res.send({
					'error':'the following error has occured.\n' + err.toString()
				})
			} else {
				res.send(item)
			}
		})
	})
}