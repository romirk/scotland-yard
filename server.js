const express = require('express');
const websocket = require("ws");
const http = require("http");
const logger = require('morgan');
const fs = require('fs');
const path = require('path');
const cookieParser = require('cookie-parser');

const game = require('./routes/games');

const app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/games', game);

const port = 80;
const host = '0.0.0.0';
// 127.0.0.1 
// 192.168.1.38
// 106.201.61.11

const server = http.createServer(app);

server.listen(port, host, () => {
    console.log(`Starting the server at ${host}:${port}`);
});

module.exports = app;