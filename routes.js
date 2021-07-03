//Require the express package and use express.Router()
const express = require('express');
const router = express.Router();
// const crypto = require('crypto');
const { v4: uuidv4 } = require('uuid');

const multiplayer = require('./multiplayerHandler');

router.use(express.urlencoded({ extended: true }));
router.use(express.json());

/**
 * available routes:
 * /new
 * /:game_id
 * /lobby
 * /play
 */

router.get('/', (req, res) => {
    res.locals.action = "/new";
    res.locals.game_id = "";
    res.locals.isJoining = false;
    res.render("index");
});

router.post("/new", (req, res) => {
    let name = req.body.player_name;
    if (name == "") {
        res.redirect("/");
        return;
    }
    let token = req.cookies.sy_client_token;
    req.body.game_id = token;

    multiplayer.createRoom(token, name);
    res.redirect(307, "/lobby");
});

router.post('/lobby', (req, res) => {
    let name = req.body.player_name;
    if (name == "") {
        res.redirect("/");
        return;
    }
    let game_id = req.body.game_id;
    if (game_id == "") {
        res.status(400);
        res.end();
        return;
    }
    let token = res.locals.token = req.cookies.sy_client_token;

    let result = multiplayer.joinRoom(token, name, game_id);
    if(!result) {
        // invalid token
        res.redirect("/?error=invalid_room_code");
    }

    res.render("lobby");
});

router.get('/play', (req, res) => {
    res.locals.token = res.cookies.token;
    res.render("game");
});

router.get('/:game_id', (req, res) => {
    let token = req.cookies.sy_client_token;
    res.locals.action = "/lobby";
    res.locals.game_id = req.params.game_id;
    res.locals.isJoining = true;
    res.render("index");
});

module.exports = router;