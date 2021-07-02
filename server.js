const express = require('express');
const http = require("http");
const logger = require('morgan');
const path = require('path');
const cookieParser = require('cookie-parser');
const { v4: uuidv4 } = require('uuid');
// const { socketServer } = require("socket.io");

const games = require('./routes/games');
const wsRoutes = require('./websocketRoutes');

const app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use((req, res, next) => {
    if (req.cookies.sy_client_token === undefined) {
        let token = uuidv4();
        req.cookies.sy_client_token = token;
        res.cookie('sy_client_token', token, { httpOnly: true });
    }
    // console.log("token:" + req.cookies.sy_client_token);
    next();
});

app.use(express.static(path.join(__dirname, 'public')));


app.use('/games', games);

const port = 80;
const host = '0.0.0.0';

const server = http.createServer(app);
const io = wsRoutes(require("socket.io")(server));

// const wss = require('./websocketRoutes');

server.listen(port, host, () => {
    console.log(`Starting the server at ${host}:${port}`);
});

module.exports = app;