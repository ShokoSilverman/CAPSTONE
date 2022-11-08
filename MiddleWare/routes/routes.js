const { ObjectID } = require("bson");
const {MongoClient, ObjectId} = require("mongodb");

//const url = 'mongodb://localhost:27017'; //local
const url = 'mongodb+srv://ShokoCapstone:U5bjze5RVZsHiLn5@capstone.qawfukq.mongodb.net/?retryWrites=true&w=majority'
const client = new MongoClient(url);

const dbName = 'Capstone';
const db = client.db(dbName);
const modelCollection = db.collection('ModelFiles');

exports.root = async(req, res) => {
    res.send('test');
}

exports.getAllModels = async(req, res) => {
    await client.connect();
    const findResult = await modelCollection.find({}).toArray();
    // const findResult = await modelCollection.project({ name: 1 }).toArray();
    let results = [];
    // for (let i = 0; i < findResult.length; i++) {
    //     names.push({"id" : findResult[i] "name" : findResult[i].name});
    // }
    findResult.forEach((item) => {results.push({"id" : item._id, "name" : item.name})});
    client.close();
    res.send(results);
}