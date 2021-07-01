//Require the express package and use express.Router()
const express = require('express');
const router = express.Router();

router.use(express.urlencoded());
router.use(express.json());

router.get('/', (req, res) => {
    console.log("game route");
    res.sendStatus(200);
});

module.exports = router