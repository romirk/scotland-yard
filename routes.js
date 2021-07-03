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
 * /games/new
 * /games/:game_id
 * /games/play
 */
router.post("/new", (req, res) => {
    let name = req.body.player_name;
    console.log(req.body);
    let token = req.cookies.sy_client_token;

    multiplayer.createRoom(token, name);
    res.redirect("/lobby");
});

router.get('/lobby', (req, res) => {
    res.locals.token = res.cookies.token;
    res.render("lobby");
});
router.get('/play', (req, res) => {
    res.locals.token = res.cookies.token;
    res.render("game");
});

module.exports = router;