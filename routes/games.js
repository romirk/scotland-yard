//Require the express package and use express.Router()
const express = require('express');
const router = express.Router();
// const crypto = require('crypto');
const { v4: uuidv4 } = require('uuid');

const multiplayer = require('../multiplayerHandler');

router.use(express.urlencoded({ extended: true }));
router.use(express.json());

router.post("/new", (req, res) => {
    let name = req.body.player_name;
    console.log(req.body);
    let token = req.cookies.sy_client_token;

    if (typeof req.body.create !== 'undefined') {
        if (multiplayer.getGameWithPlayer(token) !== undefined)
            multiplayer.disconnect(token);
        multiplayer.createRoom(token, name);
        res.locals.token = token;
        res.render('createRoom');
    } else if (typeof req.body.join !== 'undefined') {
        res.locals.token = token;
        res.render('joinRoom');
    } else {
        res.status(405);
        res.end();
    }
});

router.get("/:game_id", (req, res, next) => {
    let token = req.cookies.sy_client_token;
    let name = req.body.player_name;
    let game_id = req.params.game_id;

    if (token === game_id) {
        // host joined, start the game
        try {
            multiplayer.startGame(game_id)
            res.locals.token = token;
            res.render('game');
        } catch (e) {
            res.redirect("/");
            next(e);
        }
    } else {
        multiplayer.joinRoom(token, name, req.params.game_id);
        res.locals.token = token;
        res.render('game');
    }
});

module.exports = router;