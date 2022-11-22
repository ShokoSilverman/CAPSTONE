const { ObjectID } = require("bson");
const {MongoClient, ObjectId} = require("mongodb");

//const url = 'mongodb://localhost:27017'; //local
const url = 'mongodb+srv://ShokoCapstone:U5bjze5RVZsHiLn5@capstone.qawfukq.mongodb.net/?retryWrites=true&w=majority'
const client = new MongoClient(url);

const dbName = 'Capstone';
const db = client.db(dbName);
const modelCollection = db.collection('ModelFiles');
const userCollection = db.collection('Users');

exports.root = async(req, res) => {
    res.send('test');
}

exports.getAllModels = async(req, res) => {
    await client.connect();
    const findResult = await modelCollection.find({"is_private":false}).toArray();
    // const findResult = await modelCollection.project({ name: 1 }).toArray();
    let results = [];
    findResult.forEach((item) => {results.push({"id" : item._id, "name" : item.name, "createdBy" : item.user, 'description':item.description, 'dateCreated':item.dateCreated})});
    client.close();
    res.send(results);
}

exports.createUser = async(req, res) => {
    // console.log(req.body);
    await client.connect();
    let response = 1;
    try {
    const insertResult = await userCollection.insertOne({"_id": req.body._id, "username": req.body.username ,"password": req.body.password});
    } catch (duplicateError) {
        response = "User already exists!";
    }
    client.close();
    res.send(response);
}

exports.login = async(req, res) => {
    await client.connect();
    const findResult = await userCollection.findOne({"_id": req.body.email, "password": req.body.password});
    client.close();
    if(findResult == null) {
        res.send("Incorrect email or password");
    } else {
        res.send(findResult);
    }
}

exports.getById = async(req, res) => {
    await client.connect();
    const findResult = await modelCollection.findOne({"_id":  ObjectID(req.params.id)});
    // const findResult = await modelCollection.findOne({'name':'musicGenre'})
    client.close();
    res.send(findResult);
}

exports.getAllByEmail = async(req, res) => {
    await client.connect();
    const findResult = await modelCollection.find({"user_mail": req.params.email}).toArray();
    client.close();
    res.send(findResult);
}