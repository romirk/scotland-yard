const express = require('express');
const http = require("http");
const logger = require('morgan');
const path = require('path');
const cookieParser = require('cookie-parser');
const { v4: uuidv4 } = require('uuid');

const routes = require('./routes');
const wsRoutes = require('./websocketRoutes');

const app = express();

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
    next();
});

app.use(express.static(path.join(__dirname, 'public')));
app.use('/', routes);


const port = 80;
const host = '0.0.0.0';

const server = http.createServer(app);
const io = wsRoutes(require("socket.io")(server));

server.listen(port, host, () => {
    console.log(`Starting the server at ${host}:${port}`);
});

module.exports = app;