//Require the express package and use express.Router()
const express = require('express');
const router = express.Router();

const multiplayer = require('../multiplayerHandler');

router.use(express.urlencoded({ extended: true }));
router.use(express.json());

router.get('/', (req, res) => {
    res.locals.action = "/new";
    res.locals.game_id = req.cookies.sy_client_ID;;
    res.locals.isJoining = false;
    res.render("index");
});

router.post("/new", (req, res) => {
    let name = req.body.player_name;
    if (name === undefined || name === "") {
        res.redirect("/?error=empty_name");
        return;
    }
    let ID = req.cookies.sy_client_ID;
    multiplayer.createRoom(ID, name).then(() => res.redirect(308, "/lobby"));
});

router.get('/lobby', (req, res) => {
    let ID = res.locals.player_id = req.cookies.sy_client_ID;
    let game = multiplayer.getGameByPlayer(ID);
    if (game === undefined) {
        res.redirect("/?error=not_in_game");
        return;
    }
    let player = multiplayer.getAllPlayersInGame(game).find(p => p.player_id === ID);
    res.locals.color = player.color;
    res.locals.isMrX = player.isMrX;
    res.render("lobby");
});

router.post('/lobby', (req, res) => {
    // TODO retrieve previously connected players
    console.log(req.body);
    let name = res.locals.name = req.body.player_name;
    if (name == "" || name === undefined) {
        res.redirect("/?error=empty_name");
        return;
    }

    let player_id = res.locals.player_id = req.cookies.sy_client_ID;
    let game_id = res.locals.game_id = req.body.game_id;


    if (multiplayer.gameExists(game_id)) {
        let player = multiplayer.getAllPlayersInGame(game_id).find(player => player.player_id === player_id);
        if (player !== undefined) {
            res.locals.color = player.color;
            res.locals.isMrX = player.isMrX;
            res.render("lobby");
        } else {
            // game exists, but player not in it
            multiplayer.joinRoom(player_id, name, game_id)
                .then((result) => {
                    res.locals.color = result.color;
                    res.locals.isMrX = result.isMrX;
                    res.render("lobby");
                })
                .catch((err) => {
                    console.log(err);
                    res.redirect("/?error=can't_join_room&errmsg=" + encodeURIComponent(err));
                    return;
                });
        }
    } else {
        res.redirect("/?error=invalid_room_code");
        return;
    }
});

router.get('/play', (req, res) => {
    let ID = req.cookies.sy_client_ID;
    multiplayer.startGame(multiplayer.getGameWithPlayer(ID));
    res.locals.player_id = ID;
    res.locals.api_key = process.env.GOOGLE_API_KEY;
    res.render("game");
});

router.get('/:game_id', (req, res) => {
    if (!multiplayer.gameExists(req.params.game_id)) {
        res.status(404);
        res.render('404', { url: req.url });
        return;
    }
    res.locals.ID = req.cookies.sy_client_ID;
    res.locals.action = "/lobby";
    res.locals.game_id = req.params.game_id;
    res.locals.isJoining = true;
    res.render("index");
});

module.exports = router;