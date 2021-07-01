//Require the express package and use express.Router()
const express = require('express');
const router = express.Router();
// const crypto = require('crypto');
import { v4 as uuidv4 } from 'uuid';

const multiplayer = require('../multiplayerHandler');

router.use(express.urlencoded({ extended: true }));
router.use(express.json());


router.get('/', (req, res) => {
    console.log("game route");
    res.sendStatus(200);
});

router.post("/new", (req, res) => {
    let name = req.body.player_name;
    console.log(req.body);
    if (typeof req.body.create !== 'undefined') {
        let token = uuidv4();
        multiplayer.createRoom(token);
        res.render('createRoom');
    } else if (typeof req.body.join !== 'undefined') {
        res.render('joinRoom');
    } else {
        res.status(400);
        res.end();
    }
});

module.exports = router;