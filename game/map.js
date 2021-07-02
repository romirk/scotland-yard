const Station = require('./station');

function Map(map_data) {
    const N = map_data.length;
    const stations = [];

    for (let i = 0; i < N; i++) {
        let station = new Station(i);
        for (let j = 0; j < map_data[i].length; j++) {
            station.addNeighbour(j, map_data[i][j] - 1); // subtract 1 to account for the fact that the map data is 1-indexed
        }
        Object.freeze(station.getAllNeighbours());
        Object.freeze(station);
        stations.push(station);
    }

    this.getStation = (n) => stations[n];
    this.N = () => N;
}

module.exports = Map;