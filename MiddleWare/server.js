// const express = require('express');
const routes = require('./routes/routes.js');

// const app = express();

// // const urlencodedParser = express.urlencoded({
// //     extended: false
// // })

// app.get('/', routes.root);

// app.listen(3000);

const express = require('express');
const app = express();
const port = process.env.PORT || 5000;
const cors = require('cors');
const path = require('path');
app.use(cors());

app.use(express.static('public'));

const urlencodedParser = express.urlencoded({
   extended: false
})

app.use(express.json());


app.get('/', routes.root);
app.get('/getAllModels', routes.getAllModels);
app.post('/createUser', routes.createUser);
app.post('/login', routes.login);






app.listen(port, () => {
   console.log(`Server is up at port ${port}`);
});