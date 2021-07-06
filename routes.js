//Require the express package and use express.Router()
const express = require('express');
const router = express.Router();

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
    res.locals.game_id = req.cookies.sy_client_token;;
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
    multiplayer.createRoom(token, name).then(() => res.redirect(308, "/lobby"));
});

router.post('/lobby', (req, res) => {
    let name = req.body.player_name;
    if (name == "" || name === undefined) {
        res.redirect("/?error=empty_name");
        return;
    }

    let game_id = req.body.game_id;
    if (!multiplayer.gameExists(game_id)) {
        res.redirect("/?error=invalid_room_code");
        return;
    }

    let token = res.locals.token = req.cookies.sy_client_token;

    multiplayer.joinRoom(token, name, game_id)
    .then(() => res.render("lobby"))
    .catch((err) => {
        console.log(err);
        res.redirect("/?error=can't_join_room");
        return;
    });
});

router.get('/play', (req, res) => {
    res.locals.token = req.cookies.token;
    res.render("game");
});

router.get('/:game_id', (req, res) => {
    if (!multiplayer.gameExists(req.params.game_id)) {
        res.status(404);
        res.render('404', {url: req.url});
        return;
    }
    res.locals.token = req.cookies.sy_client_token;
    res.locals.action = "/lobby";
    res.locals.game_id = req.params.game_id;
    res.locals.isJoining = true;
    res.render("index");
});

module.exports = router;